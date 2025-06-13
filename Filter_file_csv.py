import csv
import re
import os

def parse_reference(ref):
    """Parse a reference like 'A02.G05.R6' and return sortable parts"""
    if not ref or ref.strip() == '':
        return ('', 0, 0, 0)
    
    parts = ref.split('.')
    if len(parts) != 3:
        return ('', 0, 0, 0)
    
    # First part: letter + digits (ex: A02)
    first_match = re.match(r'([A-Z])(\d+)', parts[0])
    if first_match:
        first_letter = first_match.group(1)
        first_number = int(first_match.group(2))
    else:
        first_letter = ''
        first_number = 0
    
    # Second part: G + digits (ex: G05)
    second_match = re.match(r'G(\d+)', parts[1])
    second_number = int(second_match.group(1)) if second_match else 0
    
    # Third part: R + digits (ex: R6)
    third_match = re.match(r'R(\d+)', parts[2])
    third_number = int(third_match.group(1)) if third_match else 0
    
    return (first_letter, first_number, third_number, second_number)

def sort_csv_file(input_path, output_path, reference_column=4):
    """Read a CSV file, sort it by references and save the result"""
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            print(f"Error: File {input_path} does not exist")
            return False
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Directory created: {output_dir}")
        
        # Read the file (even if it's a .txt, treat it as CSV)
        with open(input_path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)
        
        if not rows:
            print("The file is empty")
            return False
        
        print(f"File read: {len(rows)} lines found")
        
        # Sort function based on reference column
        def sort_key(row):
            if len(row) <= reference_column:
                return ('', 0, 0, 0)
            reference = row[reference_column].strip('"')  # Remove quotes
            return parse_reference(reference)
        
        # Sort the data
        sorted_rows = sorted(rows, key=sort_key)
        
        # Write the sorted file
        with open(output_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(sorted_rows)
        
        print(f"Sorted file saved: {output_path}")
        
        # Display sort preview
        print("\nSort preview (first 5 lines):")
        print("-" * 60)
        for i, row in enumerate(sorted_rows[:5], 1):
            if len(row) > reference_column:
                reference = row[reference_column].strip('"')
                parsed = parse_reference(reference)
                print(f"{i}. Reference: {reference} -> Sort: {parsed}")
        
        return True
        
    except Exception as e:
        print(f"Error during processing: {e}")
        return False

def main():
    """Main function adapted to your project structure"""
    # Paths based on your project structure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input file in Filter_csv
    input_path = os.path.join(script_dir, "Filter_csv", "Filter_csv.txt")
    
    # Output file in Extract_data_csv
    output_path = os.path.join(script_dir, "Extract_data_csv", "Extract.txt")
    
    print(f"Reading from: {input_path}")
    print(f"Writing to: {output_path}")
    print("-" * 60)
    
    # Execute sorting
    success = sort_csv_file(input_path, output_path)
    
    if success:
        print("\n✅ Sorting completed successfully!")
        print(f"Filtered data is now in: {output_path}")
    else:
        print("\n❌ Error during sorting")

# Execute the script
if __name__ == "__main__":
    main()