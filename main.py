from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys
import asyncio
import logging
from sqlite_rag import SQLiteOpenAIRAG
from chunking import CustomChunking
from batch_embedding import AsyncEmbeddingGenerator
from result_database import ResultDatabase
from rag_chatbot import RAGChatbot
import sqlite3
import glob

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EditValueRequest(BaseModel):
    doc_type: str
    field_name: str
    updated_value: str

class ChatRequest(BaseModel):
    query: str
    session_id: str

# Initialize logger
logging.basicConfig(level=logging.INFO)

def sow_transform_response(response: list) -> list:
    field_mapping = {
        'start_date': 'sow_start_date',
        'end_date': 'sow_end_date'
    }
    
    transformed = []
    for entry in response:
        original_field = entry['field']
        # Rename fields
        field = field_mapping.get(original_field, original_field)

        # We'll gather all these for the new dictionary
        value = entry['value']
        page_num = entry['page_num'] if entry['page_num'] not in ['', None] else 0

        # Also preserve the confidence, reasoning, and proof
        confidence = entry.get('confidence', None)
        reasoning = entry.get('reasoning', None)
        proof = entry.get('proof', None)

        # -- Perform your custom transformations on `value` --
        if field == 'currency' and value == 'Rs':
            value = 'INR'
        elif field == 'billing_unit_type_and_rate_cost':
            # First convert to string if it's not already
            if isinstance(value, dict) and isinstance(value.get('field_value'), dict):
                field_value = value['field_value']
                per_sample = field_value.get('per_sample', 0)
                per_item = field_value.get('per_item', 0)
                value = f"per_sample - {per_sample}, per_item - {per_item}"
            else:
                value = str(value) if value is not None else 'null'
        elif field == 'particular_role_rate' and isinstance(value, list):
            roles = [f"{r['role'].split('/')[0].strip()} - {r['rate']}" for r in value]
            value = ', '.join(roles)
        elif value in ['', None]:
            value = 'null'

        # Convert numeric to string
        if isinstance(value, (int, float)):
            value = str(value)

        # Final check to ensure value is ALWAYS a string
        if not isinstance(value, str):
            value = str(value)

        # Build the final dictionary
        transformed.append({
            'field': field,
            'value': value,
            'page_num': page_num,
            'confidence': confidence,
            'reasoning': reasoning,
            'proof': proof
        })
    return transformed
    
def transform_insurance_data(insurance_data: dict) -> list:
    """Flatten nested insurance structure into individual fields for MSA."""
    return [
        {'field': 'insurance_required', 'value': insurance_data.get('insurance_required', 'null'), 'page_num': 13},
        {'field': 'type_of_insurance_required', 'value': 'null', 'page_num': 0},
        {'field': 'is_cyber_insurance_required', 'value': insurance_data.get('is_cyber_insurance_required', 'null'), 'page_num': 0},
        {'field': 'cyber_insurance_amount', 'value': 'null', 'page_num': 0},
        {'field': 'is_workman_compensation_insurance_required', 'value': 'null', 'page_num': 0},
        {'field': 'workman_compensation_insurance_amount', 'value': 'null', 'page_num': 0},
        {'field': 'other_insurance_required', 'value': 'null', 'page_num': 0},
        {'field': 'other_insurance_amount', 'value': 'null', 'page_num': 0}
    ]

def msa_transform_response(response: list) -> list:
    field_mapping = {
        'start_date': 'msa_start_date',
        'end_date': 'msa_end_date'
    }
    
    transformed = []
    
    for entry in response:
        original_field = entry['field']
        value = entry['value']
        page_num = entry['page_num'] if entry['page_num'] else 0

        # -- ADDITIONAL FIELDS --:
        confidence = entry.get('confidence', None)
        reasoning = entry.get('reasoning', None)
        proof = entry.get('proof', None)

        # Handle special insurance_required case first
        if original_field == 'insurance_required':
            # transform_insurance_data just returns 
            # a list of {field, value, page_num} w/o confidence 
            # but you can also add them if needed. 
            transformed += transform_insurance_data(value if isinstance(value, dict) else {})
            continue
        
        # Standard MSA field mapping
        new_field = field_mapping.get(original_field, original_field)
        
        # Convert known values
        if new_field == 'client_company_name':
            value = value.upper()
        elif new_field == 'currency' and value == '$':
            value = 'USD'
        elif value == 'NULL':
            value = 'null'
            
        # Page number forcing for certain fields
        if new_field in ['msa_end_date', 'info_security']:
            page_num = 0
            
        # Type normalization
        if isinstance(value, (int, float, bool)):
            value = str(value).lower() if isinstance(value, bool) else str(value)
            
        # *** NOW, PRESERVE confidence, reasoning, proof ***
        transformed.append({
            'field': new_field,
            'value': value,
            'page_num': page_num,
            'confidence': confidence,
            'reasoning': reasoning,
            'proof': proof
        })
    
    # Add any missing frontend-specific fields
    expected_fields = ['limitation_of_liability', 'data_processing_agreement']
    existing_fields = [e['field'] for e in transformed]
    
    for f in expected_fields:
        if f not in existing_fields:
            transformed.append({
                'field': f,
                'value': 'null',
                'page_num': 0,
                'confidence': None,
                'reasoning': None,
                'proof': None
            })
    
    return transformed


@app.get("/")
async def root():
    return {"message": "Contract Extraction API is running"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    pdfType: str = Form(...)
):
    """
    Upload a PDF file, parse it, chunk it, embed it, extract fields,
    store the results in a database, and return transformed data
    (including confidence, reasoning, proof if available).
    """
    try:
        # Log the incoming request
        logging.info("Received file upload request")
        print(f"Received file upload request for {pdfType} document")

        # ---------------------------
        # 1. Save uploaded file locally
        # ---------------------------
        content = await file.read()
        file_name = "Contract.pdf"
        file_location = f"contract_file/{file_name}"
        os.makedirs("contract_file", exist_ok=True)

        # if file already exists, delete it
        if os.path.exists(file_location):
            os.remove(file_location)
        
        with open(file_location, "wb") as f:
            f.write(content)

        doc_type = pdfType.upper()
        print("-" * 30 + f"Loading {doc_type} document from '{file_location}'" + "-" * 30)

        # ---------------------------
        # 2. Initialize required classes
        # ---------------------------
        chunker = CustomChunking(overlap_words=50)
        db = ResultDatabase()
        rag_system = SQLiteOpenAIRAG()  # IMPORTANT: define rag_system before usage

        # ---------------------------
        # 3. Load and chunk the document
        # ---------------------------
        chunked_docs = chunker.load_documents(file_location)
        if not chunked_docs:
            print(f"Failed to load document: {file_location}")
            return {"success": False, "error": "Failed to load document"}

        print(f"Generated {len(chunked_docs)} chunks")

        # ---------------------------
        # 4. Check if we need to store new docs
        # ---------------------------
        conn = sqlite3.connect(rag_system.db_path)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM document_chunks')
        count = c.fetchone()[0]
        conn.close()
        
        if count == 0 or chunked_docs:
            print("-" * 30 + "Generating embeddings" + "-" * 30)
            embedding_generator = AsyncEmbeddingGenerator()
            embedded_docs = await embedding_generator.embed_chunks(chunked_docs)
            
            print("-" * 30 + "Storing chunks in database" + "-" * 30)
            rag_system.db_handler.store_chunked_docs(embedded_docs)
        
        # ---------------------------
        # 5. Extract fields
        # ---------------------------
        print("-" * 30 + "Extracting fields" + "-" * 30)
        results = await rag_system.extract_all_fields(doc_type)
        print("Extracted fields: ", results)

        if not results:
            print("No fields extracted")
            return {"success": False, "error": "No fields extracted"}

        print(f"Got {len(results)} fields")
        
        # ---------------------------
        # 6. Store results in database
        # ---------------------------
        doc_id = db.store_results(results, doc_type=doc_type, file_name=file_name)
        print(f"Stored results with doc_id: {doc_id}")

        # ---------------------------
        # 7. Transform results for frontend
        # ---------------------------
        extracted_fields = []
        for entry in results:
            field_name = entry.get('field', '')
            value_dict = entry.get('value', {})

            # Defaults
            page_num = "1"
            confidence = None
            reasoning = None
            proof = None

            # If 'value' is a dictionary with nested fields
            if isinstance(value_dict, dict):
                field_value = value_dict.get('field_value', None)
                page_num = value_dict.get('page_number', '1')
                confidence = value_dict.get('confidence', None)
                reasoning = value_dict.get('reasoning', None)
                proof = value_dict.get('proof', None)
            else:
                # If it's not a dict, store as string
                field_value = str(value_dict)

            extracted_fields.append({
                "field": field_name,
                "value": field_value,   # Not forcing to string if dict
                "page_num": page_num,
                "confidence": confidence,
                "reasoning": reasoning,
                "proof": proof
            })

        print("-" * 30 + "Finished processing" + "-" * 30)

        # Transform insurance fields for MSA
        if doc_type.upper() == "MSA":
            for field in extracted_fields:
                if field["field"] == "insurance_required":
                    value = field.get("value", {})
                    if isinstance(value, dict) and "field_value" in value:
                        insurance_data = value["field_value"]
                        
                        # Update main insurance_required field
                        field["value"] = insurance_data.get("insurance_required", "NO")
                        field["page_num"] = value.get("page_number", "0")
                        field["confidence"] = value.get("confidence", 0)
                        field["reasoning"] = value.get("reasoning", "")
                        field["proof"] = value.get("proof", [])[0] if value.get("proof") else ""

                        # Handle type_of_insurance_required
                        insurance_types = insurance_data.get("type_of_insurance_required", [])
                        if isinstance(insurance_types, list) and insurance_types:
                            type_value = ", ".join(insurance_types)
                        else:
                            type_value = "null"
                        
                        # Add or update other insurance fields
                        insurance_fields = [
                            {"field": "type_of_insurance_required", "value": type_value},
                            {"field": "is_cyber_insurance_required", "value": insurance_data.get("is_cyber_insurance_required", "NO")},
                            {"field": "cyber_insurance_amount", "value": str(insurance_data.get("cyber_insurance_amount", 0))},
                            {"field": "is_workman_compensation_insurance_required", "value": insurance_data.get("is_workman_compensation_insurance_required", "NO")},
                            {"field": "workman_compensation_insurance_amount", "value": str(insurance_data.get("workman_compensation_insurance_amount", 0))},
                        ]

                        # Handle other insurance
                        other_insurance = insurance_data.get("other_insurance_required", [])
                        other_insurance_value = ", ".join(other_insurance) if other_insurance else "null"
                        insurance_fields.extend([
                            {"field": "other_insurance_required", "value": other_insurance_value},
                            {"field": "other_insurance_amount", "value": "null"}  # Keep as null as per requirement
                        ])

                        # Add page number, confidence, reasoning, and proof from parent
                        for ins_field in insurance_fields:
                            ins_field["page_num"] = value.get("page_number", "0")
                            ins_field["confidence"] = value.get("confidence", 0)
                            ins_field["reasoning"] = value.get("reasoning", "")
                            ins_field["proof"] = value.get("proof", [])[0] if value.get("proof") else ""

                        # Add these fields to extracted_fields
                        extracted_fields.extend(insurance_fields)
                        break

        # ---------------------------
        # 8. Apply doc-type-specific transformations (MSA / SOW)
        # ---------------------------
        if doc_type.lower() == "msa":
            transformed_result = msa_transform_response(extracted_fields)
        elif doc_type.lower() == "sow":
            transformed_result = sow_transform_response(extracted_fields)

        print("Extracted data: ", transformed_result)

        # ---------------------------
        # 9. Return final JSON
        # ---------------------------
        return JSONResponse({"extracted_data": transformed_result})

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
        
# @app.post("/upload/edit-value")
# async def edit_value(request: EditValueRequest):
#     try:
#         rag = SQLiteOpenAIRAG()
#         await rag.update_field_value(request.doc_type, request.field_name, request.updated_value)
#         return {"success": True}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag-chat")
async def rag_chat(request: ChatRequest):
    try:
        query = request.query
        session_id = request.session_id

        if session_id == "first_session":
            session_id = None

        print(f"Received chat query for session {session_id}: {query}")
        
        chatbot = RAGChatbot()

        response = chatbot.chat(query)

        final_response = {
            "response": response,
            "session_id": session_id
        }

        print("Final response: ", final_response)

        return final_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
