import csv
from typing import List, Dict

class CSVWriter:
    @staticmethod
    def write_results(results: List[Dict], doc_type: str):
        """Write results to CSV file based on document type."""
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
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_headers)
            writer.writerows(csv_rows)
        
        print(f"\nResults have been saved to {output_file}")
        return output_file