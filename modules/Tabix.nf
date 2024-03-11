
nextflow.enable.dsl = 2

params.results = "/home/elukyamuzi/vector_hap/results"
params.contig = "3L"

// Define the Nextflow process for Tabix task
process Tabix {
    /*
    * index the phased VCF file
    */
    publishDir file(params.results + '/sample_phasing'), mode: "copy" 
	
    // Define input and output channels here
    input:	
	tuple val(sample_id), file(phased_vcf)

    output:
        file "*vcf.gz.tbi"

    script:
    """
    tabix ${phased_vcf}
    """
}
