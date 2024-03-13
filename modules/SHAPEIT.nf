
//SHAPEIT.nf

nextflow.enable.dsl = 2

params.resources_dir = "/home/elukyamuzi/vector_hap/resources"
params.genetic_map = "${params.resources_dir}/3L.gmap"
params.interval_list = "${params.resources_dir}/intervals_gamb_colu_arab_3L_200000_40000.txt"
params.haplotype_reference_panel = "${params.resources_dir}/ag3_gamb_colu_arab_3L_phased.vcf.gz"
params.results = "/home/elukyamuzi/vector_hap/results"
params.project_id = "test"


// Define the Nextflow process for WhatsHapStats task
process SHAPEIT {
    /*
    *  Run SHAPEIT4 on the merged VCF by genome region
    */
    publishDir file(params.results + '/cohort_phasing/SHAPEIT'), mode: "copy"
	
    // Define input and output channels here
    input:
        val region 
        file merged_vcf
	    file merged_vcf_index
		
    output:
        tuple val(region), file(region_phased_vcf), emit: region_phased_vcf
	
    // Define the script to execute shapeit task
    script:
    """	 
    shapeit4 \
        --input ${merged_vcf} \
        --map ${params.genetic_map} \
        --region ${region} \
        --window 2.5 \
        --thread 16 \
        --mcmc-iterations 5b,1p,1b,1p,1b,1p,5m \
        --pbwt-depth 4 \
        --sequencing \
        --use-PS 0.0001 \
        --log phased.log \
        --output ${region}_${params.project_id}_${params.contig}_phased.vcf.gz \
        --reference ${params.haplotype_reference_panel}
    """
}
