import sqlite3
import json
from typing import Dict, List, Any
from datetime import datetime
from database_schema import (
    SOW_DETAILED_SCHEMA,
    MSA_DETAILED_SCHEMA,
    SOW_SIMPLE_SCHEMA,
    MSA_SIMPLE_SCHEMA,
    SOW_FIELDS,
    MSA_FIELDS,
    get_create_table_sql,
    get_table_names,
    INDEX_DEFINITIONS,
    DETAILED_INDEX_DEFINITIONS,
    DOCUMENT_METADATA_SCHEMA
)

class ResultDatabase:
    def __init__(self, db_path: str = "contract_results.db"):
        """Initialize the database with separate tables for MSA and SOW results."""
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database with tables for both MSA and SOW."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Create metadata table first
            cursor.execute(get_create_table_sql('document_metadata', DOCUMENT_METADATA_SCHEMA))
            
            # Create MSA tables
            msa_tables = get_table_names('msa')
            cursor.execute(get_create_table_sql(msa_tables['detailed'], MSA_DETAILED_SCHEMA))
            cursor.execute(get_create_table_sql(msa_tables['simple'], MSA_SIMPLE_SCHEMA))

            # Create SOW tables
            sow_tables = get_table_names('sow')
            cursor.execute(get_create_table_sql(sow_tables['detailed'], SOW_DETAILED_SCHEMA))
            cursor.execute(get_create_table_sql(sow_tables['simple'], SOW_SIMPLE_SCHEMA))

            # Create indexes after all tables are created
            # Metadata table indexes
            cursor.execute(INDEX_DEFINITIONS['idx_doc_type'].format(table_name='document_metadata'))
            
            # MSA table indexes
            for table in [msa_tables['detailed'], msa_tables['simple']]:
                cursor.execute(INDEX_DEFINITIONS['idx_file_name'].format(table_name=table))
                cursor.execute(INDEX_DEFINITIONS['idx_created_at'].format(table_name=table))
            cursor.execute(DETAILED_INDEX_DEFINITIONS['idx_field_name'].format(table_name=msa_tables['detailed']))

            # SOW table indexes
            for table in [sow_tables['detailed'], sow_tables['simple']]:
                cursor.execute(INDEX_DEFINITIONS['idx_file_name'].format(table_name=table))
                cursor.execute(INDEX_DEFINITIONS['idx_created_at'].format(table_name=table))
            cursor.execute(DETAILED_INDEX_DEFINITIONS['idx_field_name'].format(table_name=sow_tables['detailed']))

            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error initializing database: {str(e)}")
            raise
        finally:
            conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _format_role_rate(self, value_dict: Dict) -> str:
        """Format role rate as a comma-separated string."""
        try:
            field_value = value_dict.get('field_value', [])
            if isinstance(field_value, str):
                try:
                    field_value = json.loads(field_value)
                except json.JSONDecodeError:
                    return str(field_value)
            if not isinstance(field_value, list):
                return str(field_value)

            # Format each role-rate pair
            formatted_pairs = []
            for item in field_value:
                if not isinstance(item, dict):
                    continue
                role = item.get('role', '').strip()
                rate = item.get('rate', 0)
                if role:  # Include even if rate is 0
                    formatted_pairs.append(f"{role}: {rate}")

            return ', '.join(formatted_pairs) if formatted_pairs else ''
        except Exception as e:
            print(f"Error formatting role rate: {str(e)}")
            return ''

    def _format_billing_unit(self, value_dict: Dict) -> str:
        """Format billing unit as a comma-separated string."""
        try:
            field_value = value_dict.get('field_value', {})
            if isinstance(field_value, str):
                try:
                    field_value = json.loads(field_value)
                except json.JSONDecodeError:
                    return str(field_value)
            if not isinstance(field_value, dict):
                return str(field_value)

            # Format each billing type-rate pair
            formatted_pairs = []
            for billing_type, rate in field_value.items():
                # Include all rates, even if 0
                formatted_type = billing_type.replace('_', ' ').title()
                formatted_pairs.append(f"{formatted_type}: {rate}")

            return ', '.join(formatted_pairs) if formatted_pairs else ''
        except Exception as e:
            print(f"Error formatting billing unit: {str(e)}")
            return ''

    def _format_insurance_field(self, value_dict: Dict) -> Dict[str, str]:
        """Format all insurance fields."""
        try:
            field_value = value_dict.get('field_value', {})
            if isinstance(field_value, str):
                try:
                    field_value = json.loads(field_value)
                except json.JSONDecodeError:
                    return self._get_default_insurance_values()

            if not isinstance(field_value, dict):
                return self._get_default_insurance_values()

            # Format insurance types
            insurance_types = []
            if isinstance(field_value.get('type_of_insurance_required'), list):
                insurance_types.extend(field_value['type_of_insurance_required'])

            # Format other insurance details
            other_insurance_types = []
            other_insurance_details = []
            
            if isinstance(field_value.get('other_insurance_required'), list):
                other_insurance_types = field_value['other_insurance_required']
            
            if isinstance(field_value.get('other_insurance_amount'), dict):
                details = field_value['other_insurance_amount'].get('insurance_details', [])
                if isinstance(details, list):
                    for detail in details:
                        if isinstance(detail, dict):
                            ins_type = detail.get('insurance_type', '')
                            amount = detail.get('amount', 0)
                            if ins_type and amount:
                                other_insurance_details.append(f"{ins_type}: ${amount:,}")

            # Combine all insurance types
            all_types = insurance_types + other_insurance_types
            all_types = [t.strip() for t in all_types if t.strip()]
            all_types = list(dict.fromkeys(all_types))  # Remove duplicates while preserving order

            # Return individual field values instead of a combined object
            return {
                'insurance_required': str(field_value.get('insurance_required', 'NO')),
                'type_of_insurance_required': ', '.join(all_types) if all_types else '',
                'is_cyber_insurance_required': str(field_value.get('is_cyber_insurance_required', 'NO')),
                'cyber_insurance_amount': str(field_value.get('cyber_insurance_amount', 0)),
                'is_workman_compensation_insurance_required': str(field_value.get('is_workman_compensation_insurance_required', 'NO')),
                'workman_compensation_insurance_amount': str(field_value.get('workman_compensation_insurance_amount', 0)),
                'other_insurance_required': ', '.join(other_insurance_types) if other_insurance_types else '',
                'other_insurance_amount': json.dumps({'insurance_details': details}) if details else ''
            }
        except Exception as e:
            print(f"Error formatting insurance field: {str(e)}")
            return self._get_default_insurance_values()

    def _get_default_insurance_values(self) -> Dict[str, str]:
        """Get default values for insurance fields."""
        return {
            'insurance_required': 'NO',
            'type_of_insurance_required': '',
            'is_cyber_insurance_required': 'NO',
            'cyber_insurance_amount': '0',
            'is_workman_compensation_insurance_required': 'NO',
            'workman_compensation_insurance_amount': '0',
            'other_insurance_required': '',
            'other_insurance_amount': ''
        }

    def store_results(self, results: List[Dict[str, Any]], doc_type: str, file_name: str) -> int:
        """Store extraction results in both detailed and simple format tables."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Get the next db_id
            cursor.execute("SELECT COALESCE(MAX(db_id), 0) + 1 FROM document_metadata")
            db_id = cursor.fetchone()[0]
            
            # Store document metadata
            cursor.execute(
                """
                INSERT INTO document_metadata (db_id, doc_type, file_name)
                VALUES (?, ?, ?)
                """,
                (db_id, doc_type.lower(), file_name)
            )

            # Get table names for the document type
            tables = get_table_names(doc_type)
            
            # Process results first to handle special fields
            processed_results = {}
            for result in results:
                field_name = result.get('field', '')
                value_dict = result.get('value', {})
                
                # Format special fields for SOW
                if doc_type.lower() == 'sow':
                    if field_name == 'particular_role_rate':
                        field_value = self._format_role_rate(value_dict)
                    elif field_name == 'billing_unit_type_and_rate_cost':
                        field_value = self._format_billing_unit(value_dict)
                    else:
                        field_value = str(value_dict.get('field_value', ''))
                # Format insurance fields for MSA
                elif doc_type.lower() == 'msa' and field_name == 'insurance_required':
                    insurance_data = self._format_insurance_field(value_dict)
                    # Create entries for all insurance fields
                    for ins_field, ins_value in insurance_data.items():
                        processed_results[ins_field] = {
                            'field_name': ins_field,
                            'field_value': ins_value,
                            'page_number': str(value_dict.get('page_number', '')),
                            'confidence': float(value_dict.get('confidence', 0)),
                            'reasoning': str(value_dict.get('reasoning', '')),
                            'proof': str(value_dict.get('proof', '')),
                        }
                    continue
                else:
                    field_value = str(value_dict.get('field_value', ''))

                processed_results[field_name] = {
                    'field_name': field_name,
                    'field_value': field_value,
                    'page_number': str(value_dict.get('page_number', '')),
                    'confidence': float(value_dict.get('confidence', 0)),
                    'reasoning': str(value_dict.get('reasoning', '')),
                    'proof': str(value_dict.get('proof', '')),
                }

            # Store in detailed format
            for result in processed_results.values():
                # Base fields for insertion
                values = {
                    'db_id': db_id,
                    'field_name': result['field_name'],
                    'field_value': result['field_value'],
                    'page_number': result['page_number'],
                    'confidence': result['confidence'],
                    'reasoning': result['reasoning'],
                    'proof': result['proof'],
                    'file_name': file_name
                }

                # Create placeholders and SQL for dynamic fields
                placeholders = ', '.join(['?' for _ in values])
                columns = ', '.join(values.keys())
                
                # Insert into detailed table
                cursor.execute(
                    f"""
                    INSERT INTO {tables['detailed']} ({columns})
                    VALUES ({placeholders})
                    """,
                    list(values.values())
                )

            # Store in simple format
            simple_values = {'file_name': file_name, 'db_id': db_id}
            fields = SOW_FIELDS if doc_type.lower() == 'sow' else MSA_FIELDS
            
            for field in fields:
                if field in processed_results:
                    simple_values[field] = processed_results[field]['field_value']
                else:
                    simple_values[field] = None

            # Insert into simple table
            placeholders = ', '.join(['?' for _ in simple_values])
            columns = ', '.join(simple_values.keys())
            cursor.execute(
                f"""
                INSERT INTO {tables['simple']} ({columns})
                VALUES ({placeholders})
                """,
                list(simple_values.values())
            )

            conn.commit()
            return db_id
            
        except Exception as e:
            conn.rollback()
            print(f"Error storing results: {str(e)}")
            raise
        finally:
            conn.close()

    def get_latest_results(self, doc_type: str, detailed: bool = True) -> List[Dict]:
        """Retrieve the latest results for a specific document type."""
        conn = self._get_connection()
        cursor = conn.cursor()

        tables = get_table_names(doc_type.lower())
        table = tables['detailed'] if detailed else tables['simple']

        try:
            cursor.execute(
                f"""
                SELECT * FROM {table}
                ORDER BY created_at DESC
                LIMIT 1
                """
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

        except Exception as e:
            print(f"Error retrieving results: {str(e)}")
            raise
        finally:
            conn.close()

    def get_document_history(self, doc_type: str) -> List[Dict]:
        """Get processing history for a document type."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM document_metadata
                WHERE doc_type = ?
                ORDER BY processed_at DESC
                """,
                (doc_type.lower(),)
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

        except Exception as e:
            print(f"Error retrieving document history: {str(e)}")
            raise
        finally:
            conn.close()

    def update_sow_msa_detailed_simple_table(self, db_id: int, field: str, value: str, page_number: str, doc_type: str) -> bool:
        """
        Update both detailed and simple tables for SOW/MSA documents.
        
        Args:
            db_id: The database ID of the document
            field: The field name to update
            value: The new value for the field
            page_number: The page number where the field is found
            doc_type: The type of document (SOW or MSA)
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Normalize doc_type
            doc_type = doc_type.lower()
            
            # Get table names based on doc_type
            detailed_table = f"{doc_type}_detailed_results"
            simple_table = f"{doc_type}_simple_results"
            
            # Update detailed table
            cursor.execute(
                f"""
                UPDATE {detailed_table}
                SET field_value = ?, page_number = ?
                WHERE db_id = ? AND field_name = ?
                """,
                (value, page_number, db_id, field)
            )
            
            # Update simple table
            # Note: We need to handle special fields differently
            if field == 'particular_role_rate' or field == 'billing_unit_type_and_rate_cost':
                # These fields require special formatting, so we'll skip them for now
                # They should be handled by the specific formatting functions in ResultDatabase
                pass
            else:
                cursor.execute(
                    f"""
                    UPDATE {simple_table}
                    SET {field} = ?
                    WHERE db_id = ?
                    """,
                    (value, db_id)
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error updating tables: {str(e)}")
            if conn:
                conn.rollback()
                conn.close()
            return False
