
nextflow.enable.dsl = 2

params.results = "/home/elukyamuzi/vector_hap//results"
params.project_id = "test"
params.contig = "3L"

// Define the Nextflow process for Tabix task
process TabixII {
    /*
    * index the phased VCF file
    */
    publishDir file(params.results + '/cohort_phasing/SHAPEIT'), mode: "copy" 
	
    // Define input and output channels here
    input:	
	    //tuple val(sample_id), file(phased_vcf)
        tuple val(region), file(region_phased_vcf)

    output:
        file "*_phased.vcf.gz.tbi"

    script:
    """
    tabix ${region}_${params.project_id}_${params.contig}_phased.vcf.gz
    """
}
