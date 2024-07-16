import csv
import os

# Path to the input manifest file
input_manifest = '../vector_hap/wgs_snp_testdata.tsv'

# Required columns
required_columns = ['sample_id', 'bam_path', 'bai_path', 'vcf_path', 'zarr_path']

def validate_manifest(manifest_path):
    """
    Validate the input manifest file for required columns and non-empty values.
    
    Args:
    manifest_path (str): Path to the manifest file.
    
    Returns:
    bool: True if validation passes, False otherwise.
    """
    try:
        with open(manifest_path, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            
            # Check if all required columns are present
            if not all(column in reader.fieldnames for column in required_columns):
                print(f"Error: Manifest file is missing required columns. Required columns are: {required_columns}")
                return False
            
            # Check each row for non-empty values
            for row in reader:
                for column in required_columns:
                    if not row[column].strip():
                        print(f"Error: Missing value for column '{column}' in row: {row}")
                        return False
                        
            print("Success: Manifest file is correctly formatted and contains all required fields.")
            return True
    
    except Exception as e:
        print(f"Error: An exception occurred while validating the manifest file. {str(e)}")
        return False

# Run the validation
if __name__ == "__main__":
    if validate_manifest(input_manifest):
        print("Manifest file validation passed.")
    else:
        print("Manifest file validation failed.")

