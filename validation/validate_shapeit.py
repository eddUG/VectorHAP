import os
import glob
import subprocess

def check_file_exists(file_path):
    """Check if the file exists."""
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        return False
    return True

def check_vcf_format(vcf_path):
    """Check if the VCF file is correctly formatted using bcftools."""
    try:
        result = subprocess.run(['bcftools', 'view', vcf_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: VCF file {vcf_path} is not correctly formatted. bcftools output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error: An exception occurred while validating VCF format. {str(e)}")
        return False

def count_intervals(interval_list_path):
    """Count the number of intervals in the interval list file."""
    try:
        with open(interval_list_path, 'r') as file:
            intervals = file.readlines()
        return len(intervals)
    except Exception as e:
        print(f"Error: An exception occurred while reading interval list file. {str(e)}")
        return 0

def validate_phased_chunks(contig, interval_count, phased_vcf_directory):
    """Validate that the number of phased chunk files matches the number of intervals and their formats."""
    phased_files_pattern = os.path.join(phased_vcf_directory, f"*{contig}_phased.vcf.gz")
    phased_files = glob.glob(phased_files_pattern)
    
    if len(phased_files) != interval_count:
        print(f"Error: Number of phased chunk files ({len(phased_files)}) does not match the number of intervals ({interval_count}) for contig {contig}.")
        return False
    
    for phased_file in phased_files:
        if not check_vcf_format(phased_file):
            return False
    
    return True

def validate_shapeit_phasing(vcf_directory, interval_directory, phased_vcf_directory):
    """Validate that each contig's merged VCF file has been phased into the correct number of chunks."""
    contigs = ['2R', '2L', '3R', '3L', 'X']
    for contig in contigs:
        merged_vcf_pattern = os.path.join(vcf_directory, f"*{contig}_merged.vcf.gz")
        merged_vcf_files = glob.glob(merged_vcf_pattern)
        
        if not merged_vcf_files:
            print(f"Error: No merged VCF file found for contig {contig}.")
            continue
        
        merged_vcf_path = merged_vcf_files[0]  # Use the first match
        interval_list_path = os.path.join(interval_directory, f"intervals_gamb_colu_arab_{contig}_200000_40000.txt")
        
        if not check_file_exists(merged_vcf_path):
            continue
        
        interval_count = count_intervals(interval_list_path)
        if interval_count == 0:
            continue
        
        print(f"Validating {contig} with merged VCF {merged_vcf_path}...")
        if validate_phased_chunks(contig, interval_count, phased_vcf_directory):
            print(f"Validation passed for contig {contig}.")
        else:
            print(f"Validation failed for contig {contig}.")

# Define the directories
vcf_directory = '../vector_hap/results/cohort_phasing/'
interval_directory = '../vector_hap/resources/'
phased_vcf_directory = '../vector_hap/results/cohort_phasing/phased_chunks/'

# Run validation
validate_shapeit_phasing(vcf_directory, interval_directory, phased_vcf_directory)

