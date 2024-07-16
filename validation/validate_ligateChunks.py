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

def list_phased_chunks(contig, phased_vcf_directory):
    """List all phased chunk files for a given contig."""
    phased_files_pattern = os.path.join(phased_vcf_directory, f"*{contig}_phased.vcf.gz")
    phased_files = glob.glob(phased_files_pattern)
    return phased_files

def extract_chrom_entries_with_grep(vcf_path):
    """Extract chrom entries from a VCF file using grep."""
    try:
        result = subprocess.run(['zgrep', '-v', '^#', vcf_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: Failed to extract chrom entries from {vcf_path}. grep output: {result.stderr}")
            return None
        entries = [line.split('\t')[0:2] for line in result.stdout.splitlines()]
        return entries
    except Exception as e:
        print(f"Error: An exception occurred while extracting chrom entries. {str(e)}")
        return None

def validate_concatenated_file(contig, phased_files, concatenated_file_path):
    """Validate that all phased chunk files are concatenated into one file."""
    if not check_file_exists(concatenated_file_path):
        print(f"Error: Concatenated VCF file {concatenated_file_path} does not exist.")
        return False

    if not check_vcf_format(concatenated_file_path):
        return False

    concatenated_entries = extract_chrom_entries_with_grep(concatenated_file_path)
    if concatenated_entries is None:
        return False
    concatenated_set = set(tuple(entry) for entry in concatenated_entries)

    for phased_file in phased_files:
        phased_entries = extract_chrom_entries_with_grep(phased_file)
        if phased_entries is None:
            return False

        for entry in phased_entries:
            if tuple(entry) not in concatenated_set:
                print(f"Error: Chrom entry {entry} from {phased_file} is not found in {concatenated_file_path}.")
                return False

    return True

def validate_ligate_regions(vcf_directory, phased_vcf_directory):
    """Validate that all phased chunks per contig are concatenated into one file per contig."""
    contigs = ['2R', '2L', '3R', '3L', 'X']
    for contig in contigs:
        concatenated_file_pattern = os.path.join(vcf_directory, f"*{contig}_phased.vcf.gz")
        concatenated_files = glob.glob(concatenated_file_pattern)

        if not concatenated_files:
            print(f"Error: No concatenated VCF file found for contig {contig}.")
            continue

        concatenated_file_path = concatenated_files[0]  # Use the first match
        phased_files = list_phased_chunks(contig, phased_vcf_directory)
        
        if not phased_files:
            print(f"Error: No phased chunk files found for contig {contig}.")
            continue
        
        print(f"Validating {contig} with concatenated VCF {concatenated_file_path}...")
        if validate_concatenated_file(contig, phased_files, concatenated_file_path):
            print(f"Validation passed for contig {contig}.")
        else:
            print(f"Validation failed for contig {contig}.")

# Define the directories
vcf_directory = '../vector_hap/results/cohort_phasing/ligate/'
phased_vcf_directory = '../vector_hap/results/cohort_phasing/phased_chunks/'

# Run validation
validate_ligate_regions(vcf_directory, phased_vcf_directory)

