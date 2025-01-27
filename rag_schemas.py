query_rewrite_schema = {
  "name": "query_schema",
  "schema": {
    "type": "object",
    "properties": {
      "rag_search_query": {
        "type": "string",
        "description": "Rewritten query optimized for similarity search"
      },
      "llm_query": {
        "type": "string",
        "description": "Rewritten query optimized for LLM response generation"
      }
    },
    "required": [
      "rag_search_query",
      "llm_query"
    ],
    "additionalProperties": False
  },
  "strict": True
}

llm_response_schema = {
  "name": "response_schema",
  "schema": {
    "type": "object",
    "properties": {
      "answer": {
        "type": "string",
        "description": "Detailed answer based on the provided context chunks."
      },
      "confidence": {
        "type": "number",
        "description": "Confidence score between 0 and 1."
      },
      "reasoning": {
        "type": "string",
        "description": "Explanation of how the answer was derived from the context."
      }
    },
    "required": [
      "answer",
      "confidence",
      "reasoning"
    ],
    "additionalProperties": False
  },
  "strict": True
}

context_summary_schema = {
  "name": "conversation_summary",
  "schema": {
    "type": "object",
    "properties": {
      "summary": {
        "type": "string",
        "description": "Updated conversation summary including the latest interaction"
      },
      "key_points": {
        "type": "array",
        "description": "Key points from the conversation history",
        "items": {
          "type": "string"
        }
      }
    },
    "required": [
      "summary",
      "key_points"
    ],
    "additionalProperties": False
  },
  "strict": True
}