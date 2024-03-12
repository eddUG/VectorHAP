nextflow.enable.dsl = 2

params.phased_vcfs = "/home/elukyamuzi/vector_hap/results/sample_phasing/*.gz"
params.results = "/home/elukyamuzi/vector_hap/results"
params.project_id = "test"
params.contig = "3L"

process MergeVcfs {
  /*
  *  Merge the outputs from the WhatsHap phase step into a single multi-sample VCF
  */
  publishDir file(params.results + '/cohort_phasing'), mode: "copy"

  // Define input and output channels here

  input:
      tuple val(key), file(phased_vcfs)

  output:
      tuple val(key), file("*merged.vcf"), emit: merged_vcf

  script:
  """
  bcftools merge -o ${params.project_id}_${params.contig}_merged.vcf ${params.phased_vcfs}
  """
} 
