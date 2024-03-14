//LigateRegions.nf

nextflow.enable.dsl = 2

params.resources_dir = "/home/elukyamuzi/vector_hap//resources"
params.genetic_map = "${params.resources_dir}/3L.gmap"
params.interval_list = "${params.resources_dir}/intervals_gamb_colu_arab_3L_200000_40000.txt"
params.results = "/home/elukyamuzi/vector_hap//results"
params.project_id = "test"

// Define the Nextflow process for WhatsHapStats task
process LigateRegions {
    /*
    *  ligate the regions back together
    */
    publishDir file(params.results + '/cohort_phasing'), mode: "copy"
	
    // Define input and output channels here
    input:
        region_phased_vcfs
        region_phased_vcfs_indices
		
    output:
        file "*_phased.vcf.gz"
    
		
    // Define the script to execute shapeit task
	
    script:
    """	  
    set -e pipefail

    python3 <<CODE

    //input_files = [ "~{sep='", "' region_phased_vcfs}" ]
    input_files = glob.glob(f"{params.results}/cohort_phasing/SHAPEIT/*.phased.vcf.gz")
    with open("${params.interval_list}") as f:
        intervals = [i.replace(":", "_").strip("\n") for i in f]
    ordered_files = []

    for i in intervals:
        for f in input_files:
            if i in f:
                ordered_files.append(f)

    with open("phased_vcf_list.txt", "w") as f:
        f.write("\n".join(ordered_files))
    CODE

    bcftools concat \
        --file-list "phased_vcf_list.txt" \
        --ligate \
        --output ${params.project_id}_phased.vcf.gz \
        --output-type z

    tabix ${params.project_id}_phased.vcf.gz
    """
}
