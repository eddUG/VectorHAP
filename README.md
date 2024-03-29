# VectorHAP
A Nextflow pipeline for phasing SNP genotypes for a cohort of multiple samples

VectorHAP was built and tested on Nextflow version 22.04, and Singularity version 3.6.4. Assuming you already have Nextflow, and Singularity, clone the repository:  
`git clone https://github.com/eddUG/VectorHap.git`

If Singularity is not available, the pipeline assumes all dependencies with the correct versions are available in the execution environment.  
You can run the pipeline as follows:

```bash
nextflow /path/to/repository/main.nf \
        -c /path/to/repository/nextflow.config \ 
        -profile standard \
        -with-trace \
        -resume \
        --project_id XXXXXXXXXX \
        --input_manifest /path/to/input_manifest.tsv
```


## Authors and Acknowledgements

This pipeline has been implemented as part of my vector genomics fellowship rotation to the [Data Analysis and Engineering Team](https://www.sanger.ac.uk/group/data-analysis-and-engineering/) at the Wellcome Sanger Institute's [Genomic Surveillance Unit](https://www.sanger.ac.uk/collaboration/genomic-surveillance-unit/). The methodology implemented by early versions of the pipeline is described by [Alistair et. al](https://github.com/malariagen/pipelines/blob/master/docs/specs/phasing-vector.md).

The methods and approach continue to be actively developed by the GSU.


