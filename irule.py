import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment

def extract_irules(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Dictionary to store rule_name: content pairs
        rules = {}
        
        # Updated pattern to properly handle nested braces
        pattern = r'rule\s+([^\s{]+)\s*{((?:[^{}]|{(?:[^{}]|{[^{}]*})*})*?)}'
        
        # Find all matches in the content
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            rule_name = match.group(1)
            rule_content = match.group(2).strip()
            rules[rule_name] = rule_content
            
        return rules
            
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def export_to_excel(rules, output_file):
    try:
        # Create DataFrame from rules dictionary
        df = pd.DataFrame(list(rules.items()), columns=['Rule Name', 'Content'])
        
        # Create Excel writer object
        writer = pd.ExcelWriter(output_file, engine='openpyxl')
        
        # Write DataFrame to Excel
        df.to_excel(writer, index=False, sheet_name='iRules')
        
        # Get the workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['iRules']
        
        # Adjust column widths
        worksheet.column_dimensions['A'].width = 50  # Rule Name column
        worksheet.column_dimensions['B'].width = 100  # Content column
        
        # Set wrap text and alignment for all cells
        for row in worksheet.iter_rows(min_row=2, max_row=len(df) + 1, min_col=1, max_col=2):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='top')
        
        # Auto-adjust row heights
        for row in worksheet.rows:
            max_height = 0
            for cell in row:
                if cell.value:
                    text_lines = str(cell.value).count('\n') + 1
                    max_height = max(max_height, text_lines * 15)  # 15 points per line
            worksheet.row_dimensions[row[0].row].height = max_height
        
        # Save the Excel file
        writer.close()
        
        print(f"Successfully exported to {output_file}")
        
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")


def run_extract_irules(input_file):
    output_file = input_file.replace('.conf', '-f5-irules.xlsx')
    rules = extract_irules(input_file)
    
    if rules:
        # Export to Excel
        export_to_excel(rules, output_file)
