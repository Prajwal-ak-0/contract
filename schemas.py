client_company_name_schema = {
  "name": "client_company_name_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "The extracted client company name."
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the client company name was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why the client company name was extracted."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  },
  "strict": True
}

currency_schema = {
  "name": "currency_type_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "The currency type mentioned in the contract."
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the currency type was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why the currency type was extracted."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  },
  "strict": True
}

start_date_schema = {
  "name": "start_date_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "The date when the contract was signed. The date format should be YYYY-MM-DD",
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the start date was extracted.",
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10.",
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why the start date was extracted.",
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction.",
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

end_date_schema = {
  "name": "end_date_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "The termination date of the contract. The date format should be YYYY-MM-DD. If the date is not specified, return 'NULL'.",
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the end date was extracted.",
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10.",
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why the end date was extracted.",
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction.",
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

info_security_schema = {
  "name": "info_security_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "Yes if any type of insurance or insurance clause mentioned. No if it does not exist",
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the Information Security was extracted.",
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10.",
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why the Information Security was extracted.",
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction.",
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

limitation_of_liability_schema = {
  "name": "limitation_of_liability_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "Yes if limitation of liability mentioned. No if it does not exist",
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the limitation of liability was extracted.",
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10.",
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why the limitation of liability was extracted.",
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction.",
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

data_processing_agreement_schema = {
  "name": "data_processing_agreement_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "Yes if any type of insurance or insurance clause mentioned. No if it does not exist",
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the limitation of liability was extracted.",
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10.",
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why the limitation of liability was extracted.",
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction.",
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

insurance_required_schema = {
  "name": "insurance_field_extraction",
  "strict": True,
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "object",
        "properties": {
          "insurance_required": {
            "type": "string",
            "description": "Yes if any type of insurance or insurance clause mentioned. No if it does not exist",
            "enum": [
              "YES",
              "NO"
            ]
          },
          "type_of_insurance_required": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "is_cyber_insurance_required": {
            "type": "string",
            "enum": [
              "YES",
              "NO"
            ]
          },
          "cyber_insurance_amount": {
            "type": "number"
          },
          "is_workman_compensation_insurance_required": {
            "type": "string",
            "enum": [
              "YES",
              "NO"
            ]
          },
          "workman_compensation_insurance_amount": {
            "type": "number"
          },
          "other_insurance_required": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "other_insurance_amount": {
            "type": "object",
            "properties": {
              "insurance_details": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "insurance_type": {
                      "type": "string",
                      "description": "Name of the insurance type"
                    },
                    "amount": {
                      "type": "number",
                      "description": "Monetary amount associated with insurance type"
                    }
                  },
                  "required": [
                    "insurance_type",
                    "amount"
                  ],
                  "additionalProperties": False
                }
              }
            },
            "required": [
              "insurance_details"
            ],
            "additionalProperties": False
          }
        },
        "required": [
          "insurance_required",
          "type_of_insurance_required",
          "is_cyber_insurance_required",
          "cyber_insurance_amount",
          "is_workman_compensation_insurance_required",
          "workman_compensation_insurance_amount",
          "other_insurance_required",
          "other_insurance_amount"
        ],
        "additionalProperties": False
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the insurance details were extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why the insurance details were extracted."
      },
      "proof": {
        "type": "array",
        "items": {
          "type": "string",
          "description": "Exact content from the contract chunk used as proof for the extraction."
        }
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

cola_schema = {
  "name": "cola_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "number",
        "description": "The Cost of Living Adjustment percentage value. Must be a number between 0 and 100.",
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the COLA was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why this percentage was identified as the COLA value."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

credit_period_schema = {
  "name": "credit_period_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "number",
        "description": "Number of days after invoice for payment. Must be a positive integer.",
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the credit period was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why this number was identified as the credit period."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

inclusive_or_exclusive_gst_schema = {
  "name": "gst_inclusion_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "Whether GST is included in the price. Must be either 'Inclusive' or 'Exclusive'.",
        "enum": ["Inclusive", "Exclusive"]
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the GST inclusion status was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why this GST status was determined."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

sow_value_schema = {
  "name": "sow_value_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "number",
        "description": "Total monetary value specified in the SOW or amendments. Must be a positive number.",
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the SOW value was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why this value was identified as the SOW value."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

sow_no_schema = {
  "name": "sow_number_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "The SOW number from the title section of the contract."
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the SOW number was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why this number was identified as the SOW number."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

type_of_billing_schema = {
  "name": "billing_type_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "The type of billing model used. Must be either 'Transaction Based' or 'FTE Based'.",
        "enum": ["Transaction Based", "FTE Based"]
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the billing type was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why this billing type was determined."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

po_number_schema = {
  "name": "po_number_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "The Purchase Order (PO) number from the contract."
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the PO number was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why this number was identified as the PO number."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

amendment_no_schema = {
  "name": "amendment_number_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "string",
        "description": "The amendment number from the contract."
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the amendment number was extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for why this number was identified as the amendment number."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  }
}

billing_unit_type_and_rate_cost_schema = {
  "name": "billing_unit_rate_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "object",
        "description": "Mapping of billing units to their corresponding rates",
        "properties": {
          "per_sample": {
            "type": "number",
            "description": "Rate for the billing unit per sample"
          },
          "per_item": {
            "type": "number",
            "description": "Rate for the billing unit per item"
          }
        },
        "required": [
          "per_sample",
          "per_item"
        ],
        "additionalProperties": False
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the billing unit rates were extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for the extracted billing unit rates."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  },
  "strict": True
}

particular_role_rate_schema = {
  "name": "role_rate_extraction",
  "schema": {
    "type": "object",
    "properties": {
      "field_value": {
        "type": "array",
        "description": "Mapping of roles such as Manager, Associate Manager, etc to their corresponding rates",
        "items": {
          "type": "object",
          "properties": {
            "role": {
              "type": "string",
              "description": "The name of the role"
            },
            "rate": {
              "type": "number",
              "description": "The rate corresponding to the role. If multiple rates are mentioned, consider the highest rate. If no rate is mentioned, return 0."
            }
          },
          "required": [
            "role",
            "rate"
          ],
          "additionalProperties": False
        }
      },
      "page_number": {
        "type": "string",
        "description": "The page number from which the role rates were extracted."
      },
      "confidence": {
        "type": "number",
        "description": "The confidence level of the extraction, ranging from 1 to 10."
      },
      "reasoning": {
        "type": "string",
        "description": "Justification for the extracted role rates."
      },
      "proof": {
        "type": "string",
        "description": "Exact content from the contract chunk used as proof for the extraction."
      }
    },
    "required": [
      "field_value",
      "page_number",
      "confidence",
      "reasoning",
      "proof"
    ],
    "additionalProperties": False
  },
  "strict": True
}