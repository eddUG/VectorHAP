// BgzipAndTabix.nf

nextflow.enable.dsl = 2

params.results = "/home/elukyamuzi/vector_hap//results"

process BgzipAndTabixII {
    /*
    * bgzip and index the input VCF file
    */
	
    publishDir path: "${params.results}/cohort_phasing", mode: "copy"
	
    // Define input and output channels here
    input:
        //tuple val(sample_id), file(input_vcf)
        tuple val(key), file(merged_vcf)

    output:
        //file "*.vcf.gz"
        //file "*.vcf.gz.tbi"
        file "${merged_vcf.baseName}.vcf.gz"
        file "${merged_vcf.baseName}.vcf.gz.tbi"

    script:
    """
    bgzip -c ${merged_vcf} > ${merged_vcf.baseName}.vcf.gz
    tabix ${merged_vcf.baseName}.vcf.gz
    """
}
