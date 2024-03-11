// WhatsHapPhase.nf

nextflow.enable.dsl = 2

params.resources_dir = "/home/elukyamuzi/vector_hap/resources"
params.reference = "${params.resources_dir}/refs/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP4.fa"
params.results = "/home/elukyamuzi/vector_hap/results"
params.contig = "3L"

process WhatsHapPhase {
    /*
    *  Phase genotypes at sample-level
    */
    publishDir file(params.results + '/sample_phasing'), mode: "copy"

    // Define input and output channels here
    input:
	    tuple val(sample_id), file(bam_path), file(bai_path)
	    file subset_vcf 
        file subset_vcf_index 

    output:
        tuple val(sample_id), file("*.phased.vcf.gz"), emit: phased_vcf

    // Define the script to execute WhatsHapPhase task
    script:
    """
    whatshap phase \
      -o ${sample_id}_${params.contig}.phased.vcf.gz \
      --reference ${params.reference} \
      --internal-downsampling=15 \
      ${subset_vcf} ${bam_path}
    """
}
