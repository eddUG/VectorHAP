# VectorHAP
 A Nextflow pipeline for phasing SNP genotypes for a cohort of multiple samples


 VectorHAP was built and tested on Nextflow version 22.04, and Singularity version 3.6.4. Assuming you already have Nextflow, and Singularity, clone the repository:
git clone https://gitlab.com/malariagen/VectorHap.git

If Singularity is not available, the pipeline assumes all dependencies with the correct versions are available in the execution environment.
You can run the pipeline as follows:
nextflow /path/to/repository/main.nf \
        -c /path/to/repository/nextflow.config \ 
        -profile standard \
        -with-trace \
        -resume \
        --project_id XXXXXXXXXX \
        --input_manifest /path/to/input_manifest.tsv

