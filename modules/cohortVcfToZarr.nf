// SelectVariants.nf

nextflow.enable.dsl = 2

params.results = "/home/mars/VectorHAP/results"
params.contig = "3L"

// Define the Nextflow process for SelectVariants task
process cohortVcfToZarr {
    /*
    * convert the final VCF to Zarr via the scikit-allel vcf_to_zarr function.
    */
	
    publishDir file(params.results + '/cohort_phasing'), mode: "copy"
	
    // Define input and output channels here
	
    input:
        file "${params.project_id}_phased.vcf.gz"
			
    output:
        file "${params.project_id}" 
        file "*.log"
		 
    // Define the script to execute cohortVcfToZarr task
    script:
    """
    mkdir ${params.project_id}
    python /tools/cohort_vcf_to_zarr.py \
    --input ${params.project_id}_phased.vcf.gz \
    --output ${params.project_id} \
    --contig ${params.contig} \
    --field variants/POS \
    --field variants/REF:S1 \
    --field variants/ALT:S1 \
    --field variants/AC \
    --field variants/AF \
    --field variants/CM \
    --field calldata/GT \
    --log ${params.project_id}.log 
    """
}
