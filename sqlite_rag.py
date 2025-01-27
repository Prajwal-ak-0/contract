import os
import asyncio
import sqlite3
import numpy as np
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import AsyncOpenAI
from chunking import CustomChunking
from batch_embedding import AsyncEmbeddingGenerator
from config import (
    SOW_FIELDS_TO_EXTRACT, 
    SOW_POINTS_TO_REMEMBER, 
    SOW_QUERIES, 
    SOW_QUERY_FOR_EACH_FIELD, 
    MSA_FIELDS_TO_EXTRACT, 
    MSA_POINTS_TO_REMEMBER, 
    MSA_QUERIES, 
    MSA_QUERY_FOR_EACH_FIELD
)
from schemas import (
    client_company_name_schema,
    currency_schema,
    start_date_schema,
    end_date_schema,
    info_security_schema,
    limitation_of_liability_schema,
    data_processing_agreement_schema,
    insurance_required_schema,
    cola_schema,
    credit_period_schema,
    inclusive_or_exclusive_gst_schema,
    sow_value_schema,
    sow_no_schema,
    type_of_billing_schema,
    po_number_schema,
    amendment_no_schema,
    billing_unit_type_and_rate_cost_schema,
    particular_role_rate_schema,
)

class SQLiteOpenAIRAG:
    def __init__(self, db_path: str = "vector_store.db"):
        load_dotenv()
        self.db_path = db_path
        self.class_name = "TestingClass"
        self._init_db()
        self.async_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=60.0,  # 60 second timeout
            max_retries=3  # Retry failed requests 3 times
        )
        
    def _init_db(self):
        """Initialize SQLite database with necessary tables."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Drop the table if it exists
        c.execute('DROP TABLE IF EXISTS document_chunks')
        
        # Create a new empty table for document chunks
        c.execute('''
            CREATE TABLE document_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk TEXT NOT NULL,
                page_number INTEGER NOT NULL,
                embedding BLOB NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    def store_chunked_docs(self, chunked_docs: List[Dict]) -> None:
        """Store document chunks and their embeddings in SQLite."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        for doc in chunked_docs:
            embedding_bytes = np.array(doc["embedding"], dtype=np.float32).tobytes()
            c.execute(
                'INSERT INTO document_chunks (chunk, page_number, embedding) VALUES (?, ?, ?)',
                (doc["chunk"], doc["page_number"], embedding_bytes)
            )
        
        conn.commit()
        conn.close()
        print(f"Stored {len(chunked_docs)} chunks in SQLite database.")

    def _cosine_similarity(self, query_embedding: List[float], doc_embedding: np.ndarray) -> float:
        """Calculate cosine similarity between query and document embeddings."""
        a = np.array(query_embedding)
        b = doc_embedding
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    async def get_relevant_chunks(self, query: str, k: int = 3) -> List[Dict]:
        """Get top-k relevant chunks for a query using cosine similarity."""
        # Get query embedding
        try:
            query_embedding = await self.async_client.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            )
            query_embedding = query_embedding.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding for query '{query}': {str(e)}")
            return []

        # Retrieve all chunks and their embeddings
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('SELECT chunk, page_number, embedding FROM document_chunks')
            chunks = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error retrieving chunks from database: {str(e)}")
            return []

        # Calculate similarities
        try:
            similarities = []
            for chunk, page_number, embedding_bytes in chunks:
                doc_embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                similarities.append((similarity, chunk, page_number))

            # Sort by similarity and get top-k
            similarities.sort(reverse=True)
            top_k = similarities[:k]

            return [
                {
                    "chunk": chunk,
                    "page_number": page_number,
                    "score": float(score)
                }
                for score, chunk, page_number in top_k
            ]
        except Exception as e:
            print(f"Error calculating similarities: {str(e)}")
            return []

    def format_chunks_to_xml(self, chunks: List[Dict]) -> str:
        """Format chunks into XML structure for better LLM processing."""
        xml_parts = ['<CONTENT>']
        
        for i, chunk in enumerate(chunks, 1):
            xml_parts.extend([
                f'<CHUNK_{i}>',
                '<PAGE_NUMBER>',
                str(chunk['page_number']),
                '</PAGE_NUMBER>',
                '<CHUNK_CONTENT>',
                chunk['chunk'].strip(),
                '</CHUNK_CONTENT>',
                f'</CHUNK_{i}>'
            ])
        
        xml_parts.append('</CONTENT>')
        return '\n'.join(xml_parts)

    async def extract_field_value(self, field: str, chunks: List[Dict], doc_type: str = "MSA") -> Dict[str, Any]:
        """Extract field value from chunks using gpt-4."""
        try:
            if not chunks:
                return {
                    "field_value": "",
                    "page_number": "",
                    "confidence": 0,
                    "reasoning": "No relevant chunks found",
                    "proof": ""
                }

            # Format chunks into XML structure
            chunks_content = self.format_chunks_to_xml(chunks)
            
            # Select configuration based on document type
            queries = MSA_QUERIES if doc_type == "MSA" else SOW_QUERIES
            query_for_field = MSA_QUERY_FOR_EACH_FIELD if doc_type == "MSA" else SOW_QUERY_FOR_EACH_FIELD
            points_to_remember = MSA_POINTS_TO_REMEMBER if doc_type == "MSA" else SOW_POINTS_TO_REMEMBER
            
            # Get field-specific configurations
            field_query = query_for_field.get(field, queries.get(field, [f"Extract the {field} from the contract"])[0])
            field_points = points_to_remember.get(field, "")
            
            # Get the corresponding schema
            schema_name = f"{field}_schema"
            if schema_name in globals():
                schema = globals()[schema_name]
            else:
                print(f"Warning: No schema found for field {field}, using default schema")
                schema = {
                    "type": "object",
                    "properties": {
                        "field_value": {"type": "string"},
                        "page_number": {"type": "string"},
                        "confidence": {"type": "number"},
                        "reasoning": {"type": "string"},
                        "proof": {"type": "string"}
                    },
                    "required": ["field_value", "page_number", "confidence", "reasoning", "proof"]
                }

            # Prepare the prompt
            context = f"""
                You are a contract analysis expert. Extract information accurately and provide confidence levels and reasoning.
                Always return your response in the exact JSON format specified, with all required fields.

                Extract the {field} from the following contract text.

                The response must include:
                1. field_value: The extracted value
                2. page_number: The page where the information was found
                3. confidence: A number between 1-10 indicating confidence level
                4. reasoning: Clear explanation of why this value was extracted
                5. proof: The exact text from the contract supporting this extraction

                Contract Text:
                {chunks_content}
            """
            
            # Make API call with JSON mode
            response = await self.async_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are a contract analysis expert. Extract information accurately and provide confidence levels and reasoning.
                    Always return your response in the exact JSON format specified, with all required fields."""},
                    {"role": "user", "content": context}
                ],
                response_format={"type": "json_schema", "json_schema": schema},
            )
            
            # Parse and validate the response
            try:
                result = json.loads(response.choices[0].message.content)
                
                # Ensure all required fields are present with correct types
                if "field_value" not in result:
                    result["field_value"] = ""
                if "page_number" not in result:
                    result["page_number"] = ""
                if "confidence" not in result:
                    result["confidence"] = 1
                if "reasoning" not in result:
                    result["reasoning"] = "No reasoning provided"
                if "proof" not in result:
                    result["proof"] = ""
                
                # Convert old confidence format (high/medium/low) to numeric if needed
                if isinstance(result["confidence"], str):
                    confidence_map = {"high": 9, "medium": 6, "low": 3}
                    result["confidence"] = confidence_map.get(result["confidence"].lower(), 1)

                # make a clean separator, then for each field print field_value, page_number, confidence, reasoning, proof
                if field == "insurance_required":
                    insurance_data = result['field_value']
                    print("\n\nInsurance Details:")
                    print(f"Insurance Required: {insurance_data['insurance_required']}")
                    print(f"Types of Insurance: {', '.join(insurance_data['type_of_insurance_required']) if insurance_data['type_of_insurance_required'] else 'None'}")
                    print(f"Cyber Insurance Required: {insurance_data['is_cyber_insurance_required']}")
                    print(f"Cyber Insurance Amount: ${insurance_data['cyber_insurance_amount']}")
                    print(f"Workman's Compensation Insurance Required: {insurance_data['is_workman_compensation_insurance_required']}")
                    print(f"Workman's Compensation Insurance Amount: ${insurance_data['workman_compensation_insurance_amount']}")
                    print(f"Other Insurance Required: {', '.join(insurance_data['other_insurance_required']) if insurance_data['other_insurance_required'] else 'None'}")
                    if insurance_data['other_insurance_amount']['insurance_details']:
                        print("Other Insurance Details:")
                        for detail in insurance_data['other_insurance_amount']['insurance_details']:
                            print(f"  - {detail['insurance_type']}: ${detail['amount']}")
                    else:
                        print("No Other Insurance Details")
                                

                print(f"\n\n--- {field} ---")
                print(f"field_value: {result['field_value']}, \npage_number: {result['page_number']}, \nconfidence: {result['confidence']}, \nreasoning: {result['reasoning']}, \nproof: {result['proof']}")
                print(f"\n\n")
                
                return result
                
            except json.JSONDecodeError as e:
                print(f"Error parsing GPT response for field {field}: {str(e)}")
                return {
                    "field_value": "",
                    "page_number": "",
                    "confidence": 1,
                    "reasoning": f"Error: Failed to parse GPT response - {str(e)}",
                    "proof": ""
                }
                
        except Exception as e:
            print(f"Error during extraction for field {field}: {str(e)}")
            return {
                "field_value": "",
                "page_number": "",
                "confidence": 1,
                "reasoning": f"Error during extraction: {str(e)}",
                "proof": ""
            }

    async def process_field(self, field: str, doc_type: str = "MSA") -> Dict[str, Any]:
        """Process a single field by getting relevant chunks and extracting value."""
        try:
            # Get relevant chunks for all queries for this field
            queries = MSA_QUERIES if doc_type == "MSA" else SOW_QUERIES
            field_queries = queries.get(field, [f"Extract the {field} from the contract"])
            
            chunk_tasks = []
            for query in field_queries:
                chunk_tasks.append(self.get_relevant_chunks(query))
            
            # Get all chunks in parallel
            chunks_results = await asyncio.gather(*chunk_tasks)
            
            # Combine and deduplicate chunks
            all_chunks = []
            seen_chunks = set()
            for chunks in chunks_results:
                for chunk in chunks:
                    chunk_text = chunk["chunk"]
                    if chunk_text not in seen_chunks:
                        seen_chunks.add(chunk_text)
                        all_chunks.append(chunk)
            
            # Extract value from chunks
            try:
                value = await self.extract_field_value(field, all_chunks, doc_type)
                if not isinstance(value, dict) or "field_value" not in value:
                    value = {
                        "field_value": "",
                        "page_number": "",
                        "confidence": 1,
                        "reasoning": "Error: Invalid response format",
                        "proof": ""
                    }
            except Exception as e:
                print(f"Error extracting value for field {field}: {str(e)}")
                value = {
                    "field_value": "",
                    "page_number": "",
                    "confidence": 1,
                    "reasoning": f"Error during extraction: {str(e)}",
                    "proof": ""
                }
            
            return {
                "field": field,
                "value": value,
                "chunks": all_chunks
            }
        except Exception as e:
            print(f"Error processing field '{field}': {str(e)}")
            return {
                "field": field,
                "value": {
                    "field_value": "",
                    "page_number": "",
                    "confidence": 1,
                    "reasoning": f"Error: {str(e)}",
                    "proof": ""
                },
                "chunks": []
            }

    async def extract_all_fields(self, doc_type: str = "MSA") -> List[Dict[str, Any]]:
        """Extract all fields in parallel."""
        # Select fields based on document type
        fields_to_extract = MSA_FIELDS_TO_EXTRACT if doc_type == "MSA" else SOW_FIELDS_TO_EXTRACT
        
        # Process all fields in parallel
        tasks = [self.process_field(field, doc_type) for field in fields_to_extract]
        return await asyncio.gather(*tasks)

async def main():
    # Initialize the chunking system
    chunker = CustomChunking(overlap_words=50)

    doc_type = "SOW"  # Can be "MSA" or "SOW"
    pdf_path = "contract_file/Stream.pdf"

    print("-" * 30 + f"Loading {doc_type} document from '{pdf_path}'" + "-" * 30)
    
    # Load and chunk the document
    chunked_docs = chunker.load_documents(pdf_path)
    
    # Initialize the RAG system
    rag_system = SQLiteOpenAIRAG()
    
    # Check if we need to store new documents
    conn = sqlite3.connect(rag_system.db_path)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM document_chunks')
    count = c.fetchone()[0]
    conn.close()
    
    if count == 0 and chunked_docs:
        # Generate embeddings
        embedding_generator = AsyncEmbeddingGenerator()
        embedded_docs = await embedding_generator.embed_chunks(chunked_docs)
        
        # Store documents
        rag_system.store_chunked_docs(embedded_docs)
    
    # Extract all fields in parallel
    results = await rag_system.extract_all_fields(doc_type)
    
    # Prepare data for CSV
    csv_rows = []
    
    if doc_type == "MSA":
        csv_headers = ["Field Name", "Field Value", "Page Number", "Confidence", "Reasoning", "Proof"]
        output_file = 'msa_output.csv'
        
        for result in results:
            field = result['field']
            value = result['value']
            
            # Handle insurance field specially due to nested structure
            if field == 'insurance_required' and isinstance(value['field_value'], dict):
                insurance_data = value['field_value']
                
                # Add main insurance required field
                csv_rows.append([
                    'insurance_required',
                    insurance_data['insurance_required'],
                    value.get('page_number', ''),
                    value.get('confidence', ''),
                    value.get('reasoning', ''),
                    value.get('proof', '')
                ])
                
                # Add type of insurance required
                if insurance_data.get('type_of_insurance_required'):
                    for insurance_type in insurance_data['type_of_insurance_required']:
                        csv_rows.append([
                            'insurance_type',
                            insurance_type,
                            value.get('page_number', ''),
                            value.get('confidence', ''),
                            'Type of insurance required',
                            value.get('proof', '')
                        ])
                
                # Add cyber insurance details
                csv_rows.append([
                    'cyber_insurance_required',
                    insurance_data['is_cyber_insurance_required'],
                    value.get('page_number', ''),
                    value.get('confidence', ''),
                    'Cyber insurance requirement',
                    value.get('proof', '')
                ])
                
                if insurance_data['cyber_insurance_amount'] is not None:
                    csv_rows.append([
                        'cyber_insurance_amount',
                        str(insurance_data['cyber_insurance_amount']),
                        value.get('page_number', ''),
                        value.get('confidence', ''),
                        'Cyber insurance amount',
                        value.get('proof', '')
                    ])
                
                # Add workman's compensation insurance details
                csv_rows.append([
                    'workman_compensation_insurance_required',
                    insurance_data['is_workman_compensation_insurance_required'],
                    value.get('page_number', ''),
                    value.get('confidence', ''),
                    'Workman compensation insurance requirement',
                    value.get('proof', '')
                ])
                
                if insurance_data['workman_compensation_insurance_amount'] is not None:
                    csv_rows.append([
                        'workman_compensation_insurance_amount',
                        str(insurance_data['workman_compensation_insurance_amount']),
                        value.get('page_number', ''),
                        value.get('confidence', ''),
                        'Workman compensation insurance amount',
                        value.get('proof', '')
                    ])
                
                # Add other insurance details
                if insurance_data.get('other_insurance_required'):
                    for other_insurance in insurance_data['other_insurance_required']:
                        csv_rows.append([
                            'other_insurance_required',
                            other_insurance,
                            value.get('page_number', ''),
                            value.get('confidence', ''),
                            'Other insurance requirement',
                            value.get('proof', '')
                        ])
            else:
                # Handle all other fields normally
                csv_rows.append([
                    field,
                    str(value['field_value']),
                    value.get('page_number', ''),
                    value.get('confidence', ''),
                    value.get('reasoning', ''),
                    value.get('proof', '')
                ])
    else:  # SOW document
        csv_headers = ["Field Name", "Field Value", "Page Number", "Confidence", "Reasoning", "Proof"]
        output_file = 'sow_output.csv'
        
        # SOW fields don't have nested structures, except for particular_role_rate and billing_unit_type_and_rate_cost
        for result in results:
            field = result['field']
            value = result['value']
            
            # Handle particular_role_rate specially
            if field == 'particular_role_rate' and isinstance(value['field_value'], list):
                for role_info in value['field_value']:
                    csv_rows.append([
                        f"role_rate_{role_info['role'].lower().replace(' ', '_')}",
                        str(role_info['rate']),
                        value.get('page_number', ''),
                        value.get('confidence', ''),
                        f"Rate for role: {role_info['role']}",
                        value.get('proof', '')
                    ])
            
            # Handle billing_unit_type_and_rate_cost specially
            elif field == 'billing_unit_type_and_rate_cost' and isinstance(value['field_value'], dict):
                for unit_type, rate in value['field_value'].items():
                    csv_rows.append([
                        f"billing_rate_{unit_type}",
                        str(rate),
                        value.get('page_number', ''),
                        value.get('confidence', ''),
                        f"Billing rate for {unit_type}",
                        value.get('proof', '')
                    ])
            
            # Handle all other fields normally
            else:
                csv_rows.append([
                    field,
                    str(value['field_value']),
                    value.get('page_number', ''),
                    value.get('confidence', ''),
                    value.get('reasoning', ''),
                    value.get('proof', '')
                ])
    
    # Write to CSV file
    import csv
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)
        writer.writerows(csv_rows)
    
    print(f"\nResults have been saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())