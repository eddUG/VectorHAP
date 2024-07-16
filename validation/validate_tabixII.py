import os
import subprocess
import glob

def check_file_exists(file_path):
    """Check if the file exists."""
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        return False
    return True

def extract_region(vcf_gz_path):
    """Extract the region from the first and second entries in the VCF file."""
    try:
        result = subprocess.run(['bcftools', 'view', vcf_gz_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: Failed to read VCF file {vcf_gz_path}. bcftools output: {result.stderr}")
            return None
        lines = result.stdout.split('\n')
        positions = []
        for line in lines:
            if not line.startswith('#'):
                # Split the line into columns and extract the positions of the first two entries
                columns = line.split('\t')
                contig = columns[0]
                position = columns[1]
                positions.append(position)
                if len(positions) == 2:
                    break
        if len(positions) < 2:
            print(f"Error: Less than two data entries found in VCF file {vcf_gz_path}.")
            return None
        region = f"{contig}:{positions[0]}-{positions[1]}"
        return region
    except Exception as e:
        print(f"Error: An exception occurred while extracting region from VCF file. {str(e)}")
        return None

def check_tbi_association(vcf_gz_path, region):
    """Check if the .tbi index file is correctly associated with the .vcf.gz file using tabix."""
    try:
        result = subprocess.run(['tabix', vcf_gz_path, region], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: TBI file for {vcf_gz_path} is not correctly associated. Tabix output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error: An exception occurred while checking TBI association. {str(e)}")
        return False

def validate_tabix_output(vcf_gz_path):
    """Validate the output of the TabixII module."""
    if not check_file_exists(vcf_gz_path):
        return False

    tbi_path = vcf_gz_path + '.tbi'
    if not check_file_exists(tbi_path):
        return False

    region = extract_region(vcf_gz_path)
    if not region:
        return False

    if not check_tbi_association(vcf_gz_path, region):
        return False

    print(f"Success: The .tbi file for {vcf_gz_path} is correctly formatted and valid.")
    return True

def validate_multiple_files(directory):
    """Validate multiple .tbi files."""
    contigs = ['2R', '2L', '3R', '3L', 'X']
    for contig in contigs:
        #merged_vcf_pattern = os.path.join(vcf_directory, f"*{contig}_merged.vcf.gz")
        #merged_vcf_files = glob.glob(merged_vcf_pattern)
        #vcf_gz_files = glob.glob(os.path.join(directory, '*phased.vcf.gz'))
        vcf_gz_files_pattern = os.path.join(directory, f"*{contig}_phased.vcf.gz")
        vcf_gz_files = glob.glob(vcf_gz_files_pattern)

        all_valid = True
        for vcf_gz_path in vcf_gz_files:
            print(f"Validating {contig}...")
            if not validate_tabix_output(vcf_gz_path):
                all_valid = False

        if all_valid:
            print("All files validated successfully.")
        else:
            print("Some files failed validation.")

# Define the directory containing the .vcf.gz and .tbi files
directory = '../vector_hap/results/cohort_phasing/phased_chunks/'

validate_multiple_files(directory)

