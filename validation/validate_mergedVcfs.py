
import os
import subprocess
import glob

def check_file_exists(file_path):
    """Check if the file exists."""
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        return False
    return True


def check_mergedvcf_format(vcf_path):
    """Check if the _merged.vcf.gz file is correctly formatted using bcftools."""
    try:
        result = subprocess.run(['bcftools', 'view', vcf_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: Merged VCF file {vcf_path} is not correctly formatted. bcftools output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error: An exception occurred while validating VCF format. {str(e)}")
        return False

def validate_mergedvcf_output(vcf_path):
    """Validate the output of the MergedVCF module."""
    if not check_file_exists(vcf_path):
        return False

    if not check_mergedvcf_format(vcf_path):
        return False

    print(f"Success: The Merged VCF file {vcf_path} is correctly formatted and valid.")
    return True

def validate_multiple_files(vcf_directory):
    """Validate multiple _merged.vcf.gz files in the given directory."""
    vcf_files = glob.glob(os.path.join(vcf_directory, "*_merged.vcf"))

    all_valid = True
    for vcf_path in vcf_files:
        print(f"Validating {vcf_path}...")
        if not validate_mergedvcf_output(vcf_path):
            all_valid = False

    if all_valid:
        print("All files validated successfully.")
    else:
        print("Some files failed validation.")

# Define the directory containing the merged VCF files
vcf_directory = '../vector_hap/results/cohort_phasing/'

# Run validation on multiple files
validate_multiple_files(vcf_directory)

