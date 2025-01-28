from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import numpy as np
import sqlite3
import uuid

from rag_schemas import (
    query_rewrite_schema,
    llm_response_schema,
    context_summary_schema
)

class RAGChatbot:
    def __init__(self, vector_db_path: str = "vector_store.db", conversation_db_path: str = "conversation.db"):
        """Initialize RAG Chatbot with vector store and conversation management."""
        load_dotenv()
        self.vector_db_path = vector_db_path
        self.conversation_db_path = conversation_db_path
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self._init_conversation_db()

    def _init_conversation_db(self):
        """Initialize the conversation database if it doesn't exist."""
        conn = sqlite3.connect(self.conversation_db_path)
        cursor = conn.cursor()
        
        # Create table only if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message TEXT NOT NULL,
                sent_by TEXT NOT NULL,
                context_summary TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _get_conversation_summary(self, session_id: str) -> str:
        """Retrieve the latest conversation summary for a session."""
        conn = sqlite3.connect(self.conversation_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT context_summary 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (session_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else ""

    def _store_conversation(self, session_id: str, message: str, sent_by: str, context_summary: str):
        """Store a conversation entry in the database."""
        conn = sqlite3.connect(self.conversation_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (session_id, message, sent_by, context_summary)
            VALUES (?, ?, ?, ?)
        """, (session_id, message, sent_by, context_summary))
        
        conn.commit()
        conn.close()

    def _rewrite_query(self, query: str, context_summary: str = "") -> Dict[str, str]:
        """Rewrite the query for RAG search and LLM response."""
        prompt = f"""Given the user query and conversation context, rewrite it into two optimized queries:
        1. A query sentence for similarity search to find relevant document chunks, capturing the context.
        2. A query for the LLM to generate a response based on retrieved chunks
        
        User Query: {query}
        Previous Context: {context_summary}
        
        Return the rewritten queries in the specified JSON format."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a query optimization expert. Rewrite queries to improve search and response quality."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_schema", "json_schema": query_rewrite_schema},
        )
        
        return json.loads(response.choices[0].message.content)

    def _query_embedding(self, query: str) -> List[float]:
        """Get embedding for a query string."""
        embedding = self.client.embeddings.create(
            input=query,
            model="text-embedding-3-small"
        )
        return embedding.data[0].embedding

    def _cosine_similarity(self, query_embedding: List[float], doc_embedding: np.ndarray) -> float:
        """Calculate cosine similarity between query and document embeddings."""
        a = np.array(query_embedding)
        b = doc_embedding
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def _format_chunks_to_xml(self, chunks: List[Dict]) -> str:
        """Format chunks into XML structure for better LLM processing."""
        xml_parts = ['<CONTENT>']
        
        for i, chunk in enumerate(chunks, 1):
            # Handle both dictionary and tuple formats
            if isinstance(chunk, tuple):
                chunk_text, page_number, _ = chunk
            else:
                chunk_text = chunk['chunk']
                page_number = chunk['page_number']
            
            xml_parts.extend([
                f'<CHUNK_{i}>',
                '<PAGE_NUMBER>',
                str(page_number),
                '</PAGE_NUMBER>',
                '<CHUNK_CONTENT>',
                str(chunk_text).strip(),
                '</CHUNK_CONTENT>',
                f'</CHUNK_{i}>'
            ])
        
        xml_parts.append('</CONTENT>')
        return '\n'.join(xml_parts)

    def _get_top_k_chunks(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Get top-k relevant chunks for a query using cosine similarity."""
        try:
            conn = sqlite3.connect(self.vector_db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT chunk, page_number, embedding FROM document_chunks')
            chunks = cursor.fetchall()
            conn.close()

            similarities = []
            query_embedding = self._query_embedding(query)

            for chunk, page_number, embedding in chunks:
                doc_embedding = np.frombuffer(embedding, dtype=np.float32)
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                similarities.append((similarity, page_number, chunk))

            similarities.sort(reverse=True)
            top_chunks = similarities[:k]

            return [
                {
                    "chunk": chunk,
                    "page_number": page_number,
                    "score": float(score)
                }
                for score, page_number, chunk in top_chunks
            ]

        except Exception as e:
            print(f"Error getting top k chunks: {str(e)}")
            return []

    def _generate_response(self, query: str, chunks: List[Dict], context_summary: str) -> Dict[str, Any]:
        """Generate LLM response based on query and retrieved chunks."""
        chunks_xml = self._format_chunks_to_xml(chunks)
        
        prompt = f"""Answer the user's query based ONLY on the provided context chunks.
        Do not use any external knowledge.
        
        User Query: {query}
        Previous Context: {context_summary}
        
        Reference Chunks:
        {chunks_xml}
        
        Provide a detailed answer with confidence score and reasoning."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a contract analysis expert. Answer questions accurately based only on provided context."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_schema", "json_schema": llm_response_schema},
        )
        
        return json.loads(response.choices[0].message.content)

    def _update_context_summary(self, query: str, response: str, previous_summary: str) -> Dict[str, Any]:
        """Update the conversation context summary."""
        prompt = f"""Update the context summary based on the user query and response.
        
        User Query: {query}
        Response: {response}
        Previous Summary: {previous_summary}
        
        Update the summary to include new information and remove redundant or irrelevant details.
        Provide a concise and accurate summary. Make it kind of reported speech. 
        Conversationally, make it sound like a reported speech but very concise. 
        Keeping track of the conversation. Concentrate on very high level of conversation summary."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a conversation summarizer. Create concise and informative summaries."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_schema", "json_schema": context_summary_schema},
        )
        
        return json.loads(response.choices[0].message.content)

    def chat(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """Process a user query and return a response with conversation management."""
        # Generate session_id if not provided
        if session_id is None:
            session_id = str(uuid.uuid4())

            print(f"New session started with ID: {session_id}")
            # Clear previous conversations for new sessions
            conn = sqlite3.connect(self.conversation_db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
            conn.commit()
            conn.close()

        try:
            # Get current conversation context
            print(f"User Query: {query}")
            context_summary = self._get_conversation_summary(session_id)
            print(f"Current Context Summary: {context_summary}")
            
            # Step 1: Rewrite queries
            rewritten_queries = self._rewrite_query(query, context_summary)
            
            # Step 2: Get relevant chunks
            top_chunks = self._get_top_k_chunks(rewritten_queries['rag_search_query'])
            
            # Step 3: Generate response
            response = self._generate_response(rewritten_queries['llm_query'], top_chunks, context_summary)
            
            # Step 4: Update context summary
            updated_context = self._update_context_summary(query, response['answer'], context_summary)
            
            # Step 5: Store conversation
            self._store_conversation(session_id, query, "user", updated_context['summary'])
            self._store_conversation(session_id, response['answer'], "bot", updated_context['summary'])
            
            return {
                "session_id": session_id,
                "answer": response['answer'],
                "confidence": response['confidence'],
                "reasoning": response['reasoning'],
                "context_summary": updated_context['summary'],
                "key_points": updated_context['key_points']
            }

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            raise

# Example usage:
if __name__ == "__main__":
    # Initialize chatbot
    chatbot = RAGChatbot()
    
    # Start conversation
    query = "What is the scope of the contract?"
    followup_query = "Could you please ellaborate bit more?"
    
    # simulate a conversation
    print("\nFirst Query:", query)
    response = chatbot.chat(query)
    print(f"Bot: {response['answer']}")
    print(f"Context Summary: {response['context_summary']}\n")
    
    print("Follow-up Query:", followup_query)
    response = chatbot.chat(followup_query, response['session_id'])
    print(f"Bot: {response['answer']}")
    print(f"Context Summary: {response['context_summary']}")