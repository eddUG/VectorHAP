import os
import glob

def check_file_exists(file_path):
    """Check if a file exists."""
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        return False
    return True

def check_stats_format(stats_path):
    """Check the format and content of the WhatsHap stats file."""
    try:
        with open(stats_path, 'r') as file:
            header = file.readline().strip().split('\t')
            expected_header = ['#sample', 'chromosome', 'file_name', 'variants', 'phased', 'unphased', 'singletons', 'blocks', 'variant_per_block_median', 'variant_per_block_avg', 'variant_per_block_min', 'variant_per_block_max', 'variant_per_block_sum', 'bp_per_block_median', 'bp_per_block_avg', 'bp_per_block_min', 'bp_per_block_max', 'bp_per_block_sum', 'heterozygous_variants', 'heterozygous_snvs', 'phased_snvs', 'block_n50']
            if header != expected_header:
                print(f"Error: Stats file {stats_path} has an incorrect header: {header}")
                return False

            for line in file:
                columns = line.strip().split('\t')
                if len(columns) != 22:
                    print(f"Error: Stats file {stats_path} has an incorrect number of columns: {columns}")
                    return False
        return True
    except Exception as e:
        print(f"Error: An exception occurred while validating stats file format. {str(e)}")
        return False

def check_gtf_format(gtf_path):
    """Check if a GTF file is correctly formatted."""
    try:
        with open(gtf_path, 'r') as file:
            for line in file:
                columns = line.strip().split('\t')
                if len(columns) != 9:
                    print(f"Error: GTF file {gtf_path} has an incorrect number of columns: {columns}")
                    return False
                if columns[2] != "exon":
                    print(f"Error: GTF file {gtf_path} contains a non-exon entry: {columns}")
                    return False
        return True
    except Exception as e:
        print(f"Error: An exception occurred while validating GTF format. {str(e)}")
        return False

def validate_whats_hap_stats_output(vcf_gz_path, tbi_path, stats_path, gtf_path):
    """Validate the output of the WhatsHapStats module."""
    if not check_file_exists(vcf_gz_path):
        return False

    if not check_file_exists(tbi_path):
        return False

    if not check_file_exists(stats_path):
        return False

    if not check_file_exists(gtf_path):
        return False

    if not check_stats_format(stats_path):
        return False

    if not check_gtf_format(gtf_path):
        return False

    print(f"Success: The phased VCF file {vcf_gz_path}, its index, the stats file {stats_path}, and the GTF file {gtf_path} are correctly formatted and valid.")
    return True

def validate_multiple_files(vcf_directory, stats_directory):
    """Validate multiple VCF files and their associated files in the given directories."""
    vcf_files = glob.glob(os.path.join(vcf_directory, "*.vcf.gz"))
    for vcf_file in vcf_files:
        base_name = os.path.basename(vcf_file).replace('.subset.vcf.phased.vcf.gz', '')
        stats_file_name = f"{base_name}.stats.tsv"
        gtf_file_name = f"{base_name}.blocks.gtf"

        vcf_path = vcf_file
        tbi_path = f"{vcf_path}.tbi"
        stats_path = os.path.join(stats_directory, stats_file_name)
        gtf_path = os.path.join(stats_directory, gtf_file_name)

        print(f"Validating {vcf_path} with index {tbi_path}, stats {stats_path}, and GTF {gtf_path}...")
        if validate_whats_hap_stats_output(vcf_path, tbi_path, stats_path, gtf_path):
            print(f"Validation passed for {vcf_path}.")
        else:
            print(f"Validation failed for {vcf_path}.")

# Define the directories containing the VCF files, stats files, and GTF files
vcf_directory = '../vector_hap/results/sample_phasing/'
stats_directory = '../vector_hap/results/phasing_stats/'
#gtf_directory = '../vector_hap/results/phasing_gtf/'

# Run validation on multiple files
validate_multiple_files(vcf_directory, stats_directory)

