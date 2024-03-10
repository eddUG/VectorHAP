// BgzipAndTabix.nf

nextflow.enable.dsl = 2

params.results = "../results"

process BgzipAndTabix {
    /*
    * bgzip and index the input VCF file
    */

    publishDir file(params.results + '/select_variants'), mode: "copy"
    
    // Define input and output channels here
    input:
        tuple val(sample_id), file(input_vcf)

    output:
        file "*.vcf.gz"
        file "*.vcf.gz.tbi"
        //file "${input_vcf.baseName}.vcf.gz"
        //file "${input_vcf.baseName}.vcf.gz.tbi"


    script:
    """
    bgzip -c ${input_vcf} > ${input_vcf.baseName}.vcf.gz
    tabix ${input_vcf.baseName}.vcf.gz
    """
}
