#!/bin/bash

# Function to validate a single VCF file
validate_vcf() {
    local vcf_path=$1
    if bcftools view "$vcf_path" &> /dev/null; then
        echo "VCF file $vcf_path is valid."
        return 0
    else
        echo "VCF file $vcf_path is not valid."
        return 1
    fi
}

# Directory containing subset VCF files
VCF_DIR="../vector_hap/results/select_variants"

# Initialize all VCF files in the directory
VCF_FILES=("$VCF_DIR"/*.vcf)

# Run validation for each VCF file
all_valid=true
for vcf_path in "${VCF_FILES[@]}"; do
    validate_vcf "$vcf_path"
    if [[ $? -ne 0 ]]; then
        all_valid=false
    fi
done

# Report overall validation result
if $all_valid; then
    echo "All subset VCF files are valid."
else
    echo "Some subset VCF files failed validation."
    exit 1
fi

