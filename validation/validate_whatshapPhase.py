import os
import subprocess
import glob
import vcf

def check_file_exists(file_path):
    """Check if a file exists."""
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        return False
    return True

def check_vcf_format(vcf_path):
    """Check if a VCF file is correctly formatted using bcftools."""
    try:
        result = subprocess.run(['bcftools', 'view', vcf_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: VCF file {vcf_path} is not correctly formatted. bcftools output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error: An exception occurred while validating VCF format. {str(e)}")
        return False

def check_phased_genotype_consistency(vcf_path):
    """Check if phased genotypes in a VCF file are consistent."""
    try:
        vcf_reader = vcf.Reader(filename=vcf_path)
        for record in vcf_reader:
            for sample in record.samples:
                if sample.phased:
                    gt = sample['GT']
                    if "|" not in gt:
                        print(f"Error: Found unphased genotype in phased sample in file {vcf_path} at position {record.POS}.")
                        return False
        return True
    except Exception as e:
        print(f"Error: An exception occurred while checking phased genotype consistency. {str(e)}")
        return False

def validate_whats_hap_phase_output(vcf_path):
    """Validate the output of the WhatsHapPhase module."""
    if not check_file_exists(vcf_path):
        return False

    if not check_vcf_format(vcf_path):
        return False

    if not check_phased_genotype_consistency(vcf_path):
        return False

    print(f"Success: The phased VCF file {vcf_path} is correctly formatted and contains consistent phased genotypes.")
    return True

def validate_multiple_files(directory):
    """Validate multiple VCF files in a given directory."""
    vcf_files = glob.glob(os.path.join(directory, '*.vcf.gz'))

    all_valid = True
    for vcf_path in vcf_files:
        if not validate_whats_hap_phase_output(vcf_path):
            all_valid = False

    if all_valid:
        print("All files validated successfully.")
    else:
        print("Some files failed validation.")

# Define the directory containing the VCF files
directory = '../vector_hap/results/sample_phasing/'

validate_multiple_files(directory)

