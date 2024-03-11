
//WhatsHapStats.nf

nextflow.enable.dsl = 2

params.resources_dir = "/home/elukyamuzi/vector_hap/resources"
params.ref_chr_lengths = "${params.resources_dir}/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP4.chr_lengths"
params.contig = "3L"
params.results = "/home/elukyamuzi/vector_hap/results"

// Define the Nextflow process for WhatsHapStats task
process WhatsHapStats  {
    /*
    *  Phasing statistics of a single VCF file
    */
    publishDir file(params.results + '/phasing_stats'), mode: "copy"
	
    // Define input and output channels here
    input:
	tuple val(sample_id), file(phased_vcf) 
        file(phased_vcf_index)		

    output:
        //tuple val(sample_id), file("*.tsv"), file("*.gtf")
        tuple val(sample_id), file("*.stats.tsv"), file ("*.blocks.gtf")
		
    // Define the script to execute WhatsHapStats task
	
    script:
    """
    whatshap stats \
      ${phased_vcf} \
      --chr-lengths=${params.ref_chr_lengths} \
      --tsv=${sample_id}_${params.contig}.stats.tsv \
      --gtf=${sample_id}_${params.contig}.blocks.gtf 
    """
}
