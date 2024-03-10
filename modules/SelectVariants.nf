// SelectVariants.nf

nextflow.enable.dsl = 2

params.results = "../results"
params.contig = "3L"

// Define the Nextflow process for SelectVariants task
process SelectVariants {
    /*
    * Selects Variants based on phased and called sites 
    */
    publishDir file(params.results + '/select_variants'), mode: "copy"
	
    // Define input and output channels here
    input:
        tuple val(sample_id), file(zarr_path)
        file called_sites
	    file phased_sites
			
    output:
        tuple val(sample_id), file("*.vcf"), emit: subset_vcf
		 
    // Define the script to execute SelectVariants task
    script:
    """
    python /tools/sample_select_variants.py \\
      --sample-genotypes ${zarr_path} \\
      --sites-called ${called_sites} \\
      --sites-selected ${phased_sites} \\
      --output ${sample_id}_${params.contig}.subset.vcf \\
      --contig ${params.contig} \\
      --progress
    """
}
