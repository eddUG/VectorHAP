import os

def check_directory_exists(directory_path):
    """Check if a directory exists."""
    if not os.path.isdir(directory_path):
        print(f"Error: Directory {directory_path} does not exist.")
        return False
    return True

def check_zarr_structure(zarr_path, contig):
    """Check the structure of the Zarr directory."""
    expected_folders = [
        'calldata/GT',
        'variants/AC', 'variants/AF', 'variants/ALT',
        'variants/CM', 'variants/POS', 'variants/REF'
    ]
    for folder in expected_folders:
        full_path = os.path.join(zarr_path, folder)
        if not check_directory_exists(full_path):
            print(f"Error: Zarr directory {zarr_path} is missing {folder}.")
            return False
    return True

def validate_cohort_vcf_to_zarr(contig, zarr_directory):
    """Validate the output of the cohort VCF to Zarr conversion."""
    zarr_output = os.path.join(zarr_directory, f"validation_{contig}.zarr", contig)

    if not check_directory_exists(zarr_output):
        return False

    if not check_zarr_structure(zarr_output, contig):
        return False

    print(f"Success: The Zarr directory {zarr_output} is correctly formatted and valid.")
    return True

def validate_multiple_files(contigs, zarr_directory):
    """Validate multiple files processed by cohort_vcf_to_zarr.py."""
    for contig in contigs:
        print(f"Validating contig {contig}...")
        if validate_cohort_vcf_to_zarr(contig, zarr_directory):
            print(f"Validation passed for contig {contig}.")
        else:
            print(f"Validation failed for contig {contig}.")

# Define the directories
contigs = ['2R', '2L', '3R', '3L', 'X']
zarr_directory = '../vector_hap/results/cohort_phasing/ligate/outputs/'

# Run validation on multiple files
validate_multiple_files(contigs, zarr_directory)

