SOW_QUERIES = {
    "client_company_name": [
        "Identify the name of the client company or recipient of services in the contract. The service provider is Next Wealth, so the other party is the client.",
        "What is the name of the recipient company? Next Wealth is the service provider name so extract the recipient company name."
    ],
    "currency": [
        "What is amount mentioned in the contract? Is it in USD($) OR INR(₹)?",
        "What is the currency unit in USD($) or INR(₹) paid for an FTE per month?"
    ],
    "start_date": [
        "What is the start date or effective date of the Statement of Work (SOW) as mentioned in the document? Look for terms such as 'SOW Effective Date' or any specific commencement date",
        "This Statement of Work no. 1 (“SOW”), effective as of 31st July 2023, is by and between Infostretch Corporation (India) Private Limited"
    ],
    "end_date": [
        "When does the term of the Statement of Work (SOW) end? Identify the exact end date or any expiration date mentioned in the document. Look for phrases such as 'continue to be in force until' or 'terminate'.",
        "What is the termination date of the SOW, including any specific conditions or notice period required for termination?"
    ],
    "cola": [
        "What is the cost of living adjustment (COLA) mentioned in the contract?"
    ],
    "credit_period": [
        "Invoice will be raised on the last day of the month and the payment to be made net 45 days of receiving invoice.",
        "Credit period is 45 days from the date of invoice. What is the credit period mentioned in the contract?"
    ],
    "inclusive_or_exclusive_gst": [
        "What are the terms regarding the inclusion or exclusion of GST in the pricing structure, as detailed in the amendment or Statement of Work (SOW)?",
        "Can you identify any clauses in the amendment or SOW that specify whether applicable taxes, including GST, are included or excluded in the quoted service rates?",
        "Does the document clarify if the fees or charges mentioned are inclusive or exclusive of GST? Look for relevant sections in the SOW or amendment."
    ],
    "sow_value": [
        "Can you extract the total monetary value or sow value specified for the services in the contract's Statement of Work (SOW) or any amendments?",
        "What is the final contract value as described in the SOW, including adjustments, if applicable, in the amendments?",
        "What is the total value of the Statement of Work (SOW), including all relevant costs or services, as outlined in the contract and amendments?"
    ],
    "sow_no": [
        "What is the Statement of Work (SOW) number mentioned in the document? Identify the unique identifier for the SOW, often found in the title or first section of the contract.",
        "Extract the Statement of Work Number (SOW No.) associated with the agreement or amendment, usually found at the beginning of the document.",
        "In which section is the Statement of Work number (SOW No.) mentioned? It's typically present in the opening paragraph or title of the agreement."
    ],
    "type_of_billing": [
        "What is the billing or project type mentioned in this contract? Identify if the payment model is based on 'per task,' 'per unit,' or 'per transaction' (e.g., 'per SKU,' 'per batch') or if it's based on 'per FTE' (Full-Time Equivalent), such as 'per FTE per hour' or 'per FTE per month'.",
        "Does the contract mention a billing structure based on 'per transaction' (e.g., 'per run,' 'per batch,' 'per unit') or a 'per FTE' model (e.g., 'per FTE per hour,' 'per FTE per month')? Extract the relevant details indicating whether the project is transaction-based or FTE-based.",
        "Identify the project or billing type in the contract. Is it based on 'per task,' 'per item,' 'per transaction' pricing (e.g., 'per SKU,' 'per batch') or 'FTE-based' pricing (e.g., 'per FTE per month' or 'per FTE per hour')? Extract the section that describes the billing model."
    ],
    "po_number": [
        "What is the Purchase Order (PO) number mentioned in the document? Look for fields labeled as 'PURCHASE ORDER #,' 'PO NUMBER,' or 'PURCHASE ORDER', typically accompanied by order dates or other related information.",
        "Can you extract the PO number from the contract? It might be listed under terms like 'PURCHASE ORDER #,' 'PO NUMBER,' or a similar identifier, often followed by a date or other order details.",
        "Identify the Purchase Order (PO) number in the contract. It could appear as 'PURCHASE ORDER #,' 'PO NUMBER,' or related terms and may be located alongside fields like 'ORDER DATE' or 'PAYMENT TERMS.'"
    ],
    "amendment_no": [
        "What is the Amendment Number mentioned in the document? Look for terms like 'Amendment #,' 'AMENDMENT NO,' or similar phrases, which typically appear alongside the Statement of Work Number or related contract details.",
        "Can you identify the Amendment Number in the contract? It may be found as 'Amendment #,' 'AMENDMENT NO,' or other variations, often associated with a Statement of Work Number or contract value adjustments.",
        "Extract the Amendment Number from the document. It might be indicated as 'Amendment #,' 'AMENDMENT NO,' or relevant terms and is usually linked to contract changes or the Statement of Work Number."
    ],
    "billing_unit_type_and_rate_cost": [
        "What is the unit type mentioned for billing in this contract? Look for terms like 'per FTE', 'per bag', 'per transaction' or per something. Your response should be the relevant unit type along with the cost or rate.",
        "Can you identify the unit type and cost or rate for billing in the contract? Look for terms like 'per FTE', 'per bag', 'per transaction' or per something and the associated cost or rate.",
        "Identify the unit type and cost or rate for billing in the contract. Is it 'per FTE' or 'per bag' or 'per transaction' or per something and the associated cost or rate? Extract the relevant details indicating the billing model and its associated cost or rate."
    ],
    "particular_role_rate": [
        "What is the rate for particular role mentioned in the contract? For example, 'What is the rate for Associates mentioned in the contract?' or 'What is the rate for Senior Associates mentioned in the contract?' or 'What is the rate for Team Lead or QA mentioned in the contract?' etc.",
        "Identify the rate for a specific role mentioned in the contract. For example, 'What is the rate for Associates mentioned in the contract?' or 'What is the rate for Senior Associates mentioned in the contract?' or 'What is the rate for Team Lead or QA mentioned in the contract?' etc.",
        "Extract the rate for a particular role from the contract. For example, 'What is the rate for Associates mentioned in the contract?' or 'What is the rate for Senior Associates mentioned in the contract?' or 'What is the rate for Team Lead or QA mentioned in the contract?' etc."
    ]
}

SOW_FIELDS_TO_EXTRACT = [
    "client_company_name", "currency", "start_date", "end_date",
    "cola", "credit_period", "inclusive_or_exclusive_gst", "sow_value",
    "sow_no", "type_of_billing", "po_number", "amendment_no",
    "billing_unit_type_and_rate_cost", "particular_role_rate"
]

SOW_QUERY_FOR_EACH_FIELD = {
    "client_company_name": "What is the name of the client company or recipient of services in the contract?",
    "currency": "What is amount mentioned in the contract? Is it in USD($) OR INR(₹)?.",
    "start_date": "What is the start date or effective date of the Statement of Work (SOW) as mentioned in the document?. It may be written as effective from.",
    "end_date": "When does the term of the Statement of Work (SOW) end? Identify the exact end date or any expiration date mentioned in the document.",
    "cola": "What is the cost of living adjustment (COLA) mentioned in the contract?",
    "credit_period": "Invoice will be raised on the last day of the month and the payment to be made net 45 days of receiving invoice. What is the credit period mentioned in the contract?",
    "inclusive_or_exclusive_gst": "What are the terms regarding the inclusion or exclusion of GST in the pricing structure, as detailed in the amendment or Statement of Work (SOW)?",
    "sow_value": "Can you extract the total monetary value or sow value specified for the services in the contract's Statement of Work (SOW) or any amendments?",
    "sow_no": "What is the Statement of Work (SOW) number mentioned in the document?",
    "type_of_billing": "What is the billing or project type mentioned in this contract?",
    "po_number": "What is the Purchase Order (PO) number mentioned in the document?",
    "amendment_no": "What is the Amendment Number mentioned in the document? Your response should be the Amendment Number.",
    "billing_unit_type_and_rate_cost": "What is the unit type mentioned for billing in this contract? Look for terms like 'per FTE', 'per bag', 'per transaction' or per something along with cost associated with it.",
    "particular_role_rate": "What is the rate for particular role mentioned in the contract? For example, 'What is the rate for Associates mentioned in the contract?' or 'What is the rate for Senior Associates mentioned in the contract?' or 'What is the rate for Team Lead or QA mentioned in the contract?' etc."
}

SOW_POINTS_TO_REMEMBER = {
    "client_company_name": "The service provider is Next Wealth, so the other party is the client. Next Wealth is the service provider name so it is not the client company name.",
    "currency": "Your unit value should be in 'USD' OR 'INR'?",
    "start_date": "1. Make sure you do not return some unrelated date as the effective start date.\n2. The format should be YYYY-MM-DD.\n3. If date is not specified, then return 'null'.",
    "end_date": "1. Make sure you do not return some unrelated date as the end date.\n2. The format should be YYYY-MM-DD.\n3. If date is not specified, then return 'null'.",
    "cola": "Your response should be a numerical value. Its full form is Cost of Living Adjustment. It general in terms of percentage.",
    "credit_period": "1. Your response should be a numerical value.\n2. It is the number of days after the invoice is raised.\n3. It is present in the payment terms section in this manner: 'Invoice will be raised on the last day of the month and the payment to be made net 45 days of receiving invoice.'",
    "inclusive_or_exclusive_gst": "1. Your response should be 'Inclusive' or 'Exclusive'.\n2. Only if the content is not sufficient to determine the answer, return 'Exclusive'. But never return NULL for this field.",
    "sow_value": "Your response should be a numerical value. It is the total monetary value or sow value specified for the services in the contract's Statement of Work (SOW) or any amendments.",
    "sow_no": "1. Your response should be the SOW number.\n2. It is present in the title section of the contract.\n3. Do not mistakenly return the amendment number or some other number as the SOW number.",
    "type_of_billing": "1. Your response should be 'Transaction Based' or 'FTE Based'.\n2. In case of 'Transaction Based', the unit type is 'per transaction' or 'per run' or 'per batch' or 'per unit' or 'per SKU' or 'per batch' etc will be mentioned.\n3. In case of 'FTE Based', the unit type is 'per FTE' will be mentioned.",
    "po_number": "1. Your response should be the PO number.\n2. Do not mistakenly return the amendment number or some other number as the PO number.",
    "amendment_no": "1. Your response should be the Amendment Number.\n2. Do not mistakenly return the SOW number or some other number as the amendment number.",
    "billing_unit_type_and_rate_cost": "1. Your response should be the relevant unit type along with the cost or rate.\n2. The unit type is the value mentioned after the word 'per'.\n3. The cost or rate is the value mentioned after the unit type.\n4. If there are more than one unit type and cost or rate, then return them in the following manner: 'per sample - 1000, per item - 5000', etc.",
    "particular_role_rate": "1. Your response should be the rate for the particular role mentioned in the contract.\n2. The rate is the value mentioned after the word 'per'.\n3. If there are more than one rate, then return them in the following manner: 'Associate - 1000, Senior Associate - 5000', etc."
}

MSA_QUERIES = {
    "client_company_name": [
        "Identify the name of the client company or recipient of services in the contract. The service provider is Next Wealth, so the other party is the client.",
        "What is the name of the recipient company? Next Wealth is the service provider name so extract the recipient company name."
    ],
    "currency": [
        "What is amount mentioned in the contract? Is it in USD($) OR INR(₹)?",
        "What is the currency unit in USD($) or INR(₹) paid for an FTE per month?"
    ],
    "start_date": [
        "What is the start date or effective date of the Master Service Agreement (MSA) as mentioned in the document? Look for terms such as 'MSA Effective Date' or any specific commencement date",
        "What is the start date of the Master Service Agreement (MSA)?"
    ],
    "end_date": [
        "When does the term of the Master Service Agreement (MSA) end? Identify the exact end date or any expiration date mentioned in the document. Look for phrases such as 'continue to be in force until' or 'terminate'.",
        "What is the termination date of the MSA, including any specific conditions or notice period required for termination?"
    ],
    "info_security": [
        "Is there any information security clause or requirement mentioned in the contract?",
        "Can you identify any clauses related to information security in the contract? If so, provide the details."
    ],
    "insurance_required": [
        "What are the details regarding insurance specified in the contract?",
        "What specific insurance policies and coverage amounts are required by the agreement?"
    ],
    "limitation_of_liability": [
        "What is the limit of liability mentioned in the contract?",
        "Can you identify the maximum liability amount specified in the contract terms?"
    ],
    "data_processing_agreement": [
        "Is there a Data Processing Agreement (DPA) mentioned in the contract? If yes, extract the relevant details.",
        "Can you identify any clauses related to Data Processing Agreement (DPA) in the contract? If so, provide the details."
    ]
}

MSA_FIELDS_TO_EXTRACT = [
    "client_company_name",
    "currency",
    "start_date",
    "end_date",
    "info_security",
    "insurance_required",
    "limitation_of_liability",
    "data_processing_agreement"
]

MSA_QUERY_FOR_EACH_FIELD = {
    "client_company_name": "What is the name of the client company or recipient of services in the contract?",
    "currency": "What is amount mentioned in the contract? Is it in USD($) OR INR(₹)?.",
    "start_date": "What is the start date or effective date of the Master Service Agreement (MSA) as mentioned in the document?. It may be written as effective from.",
    "end_date": "When does the term of the Master Service Agreement (MSA) end? Identify the exact end date or any expiration date mentioned in the document.",
    "info_security": "Is there any information security clause or requirement mentioned in the contract?",
    "insurance_required": "What are the specific insurance requirements including policy types, coverage amounts, and special conditions specified in the contract?",
    "limitation_of_liability": "What is the limit of liability mentioned in the contract?",
    "data_processing_agreement": "Is there a Data Processing Agreement (DPA) mentioned in the contract? If yes, extract the relevant details."
}

MSA_POINTS_TO_REMEMBER = {
    "client_company_name": "1. Next Wealth is the service provider - extract the counterparty name\n2. Look for terms like 'Client', 'Company', or 'Customer' in definitions section",
    "currency": "1. Return only 'USD' or 'INR' based on currency symbols ($/₹) or explicit mentions\n2. Ignore amounts - focus only on currency type",
    "start_date": "1. Validate against context - avoid unrelated dates\n2. Format as YYYY-MM-DD\n3. Return null if not found",
    "end_date": "1. Look for termination clauses and renewal terms\n2. Format as YYYY-MM-DD\n3. Return null for evergreen contracts",
    "info_security": "1. Return 'Specified' only if explicit infosec obligations exist\n2. Look for data protection/compliance requirements\n3. Return 'Not Specified' if no infosec requirements exist",
    "insurance_required": "1. Extract multiple sub-fields: types, coverage amounts, cyber/workman compensation requirements\n2. Return 'null' for unspecified amounts\n3. Identify certificate of insurance requirements",
    "limitation_of_liability": "1. Check for liability caps in monetary terms\n2. Look for exclusion clauses\n3. Return 'Yes' even if liability is limited to fees paid\n 4. Return 'No' if no liability is specified",
    "data_processing_agreement": "1. Verify if GDPR/compliance appendix exists\n2. Look for references to Exhibit/Attachment containing DPA\n 3. Just return 'Yes' or 'No' "
}

