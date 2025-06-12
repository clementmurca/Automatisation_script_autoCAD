import csv
import winreg
import os
from pathlib import Path

class AutoCADScriptGenerator:
    def __init__(self, txt_file, separator=';'):
        self.txt_file = txt_file
        self.separator = separator
        self.csv_data = []
        self.load_txt_data()
    
    def load_txt_data(self):
        """Load CSV-formatted data from TXT file"""
        try:
            with open(self.txt_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=self.separator)
                self.csv_data = list(reader)
                print(f"✅ TXT file loaded: {len(self.csv_data)} rows")
                
                # Debug: show first few rows
                for i, row in enumerate(self.csv_data[:3]):
                    print(f"Row {i+1}: {row}")
                    
        except Exception as e:
            print(f"❌ TXT file reading error: {e}")
            raise
    
    def read_windows_registry(self, registry_key):
        """Read a value from Windows registry""" 
        try:
            base_path = r"Software\appdatalow\software\Autodes\AutoCAD LT\R30\CoreUser\BlockPreviewUser\FixedProfile\General"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_path) as key:
                value, _ = winreg.QueryValueEx(key, registry_key)
                print(f"✅ Registry {registry_key}: {value}")
                return str(value)
        except FileNotFoundError:
            print(f"⚠️  Registry key not found: {registry_key}")
            return f"[{registry_key}_NOT_FOUND]"
        except Exception as e:
            print(f"❌ Registry reading error {registry_key}: {e}")
            return f"[ERROR_{registry_key}]"
    
    def get_system_variables(self):
        """Retrieve variables from Windows registry"""
        variables = {}
        variables['CBER_DATE'] = self.read_windows_registry('CBER_DATE')
        variables['CBER_NR'] = self.read_windows_registry('CBER_NR')
        return variables
    
    def clean_csv_value(self, value):
        """Clean CSV value by removing quotes and whitespace"""
        if isinstance(value, str):
            return value.strip().strip('"').strip()
        return str(value).strip()
    
    def generate_script_with_template(self, template_file, output_file):
        """Generate AutoCAD script by replacing variables"""
        
        # Read template
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                template = f.read()
                print(f"✅ Template loaded: {template_file}")
        except Exception as e:
            print(f"❌ Template reading error: {e}")
            raise
        
        # Get system variables from registry
        system_variables = self.get_system_variables()
        
        # Generate script for each row in TXT file
        with open(output_file, 'w', encoding='utf-8') as script_file:
            for i, csv_row in enumerate(self.csv_data, 1):
                print(f"Processing row {i}/{len(self.csv_data)}")
                
                # Extract only field 5 (CBER_REF) from the row
                if len(csv_row) >= 5:
                    cber_ref = self.clean_csv_value(csv_row[4])  # Field 5 (index 4)
                    print(f"  CBER_REF: {cber_ref}")
                else:
                    print(f"⚠️  Row {i} has insufficient columns: {len(csv_row)}")
                    cber_ref = "[MISSING_REF]"
                
                # Copy template for this row
                commands = template
                
                # Replace variables in template
                commands = commands.replace('{CBER_REF}', cber_ref)
                commands = commands.replace('{CBER_DATE}', system_variables['CBER_DATE'])
                commands = commands.replace('{CBER_NR}', system_variables['CBER_NR'])
                
                # Write commands to file
                script_file.write(commands)
                script_file.write(f"\n; --- End of {cber_ref} ---\n")
        
        print(f"✅ Script generated: {output_file}")
        return output_file

# Main function
def generate_autocad_script(txt_file, template_file, output_file):
    """Main function to generate AutoCAD script from TXT file"""
    
    print("🚀 Starting AutoCAD script generation from TXT file")
    print(f"📁 TXT file: {txt_file}")
    print(f"📄 Template: {template_file}")
    print(f"💾 Output: {output_file}")
    
    try:
        generator = AutoCADScriptGenerator(txt_file)
        generated_script = generator.generate_script_with_template(
            template_file, 
            output_file
        )
        
        print("✅ Generation completed successfully!")
        return generated_script
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        raise

# Usage
if __name__ == "__main__":
    # Configuration
    txt_file = "Extract_data_csv/extract.txt"
    template_file = "Template/gabarit_autoCAD.txt"
    output_file = "Output_folder/script_autocad.scr"
    
    # Generate script
    generate_autocad_script(txt_file, template_file, output_file)