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
## Validation

This repository includes a set of validation scripts to ensure the integrity and correctness of the pipeline.

### Validation Scripts

The `validation` directory contains the following scripts:

- `validate_manifest.py`: Validates the input manifest.
- `validate_selectvariants_output.sh`: Validates the output of the SelectVariants module.
- `validate_bgziptabix.py`: Validates the output of the BgzipAndTabix module.
- `validate_whatshapPhase.py`: Validates the output of the WhatsHapPhase module.
- `validate_whatshapStats.py`: Validates the output of the WhatsHapStats module.
- `validate_mergeVcfs.py`: Validates the output of the MergeVcfs module.
- `validate_bgziptabixii.py`: Validates the output of the BgzipAndTabixII module.
- `validate_shapeit.py`: Validates the output of the SHAPEIT module.
- `validate_tabixii.py`: Validates the output of the TabixII module.
- `validate_ligateChunks.py`: Validates the output of the LigateRegions module.
- `validate_cohortvcf2zarr.py`: Validates the output of the cohortVcfToZarr module.

### Running the Validation Scripts

####Interactive approach
To run the validation scripts, navigate to the `validation` directory and execute the desired script. For example:

```bash
cd validation
./validate_selectvariants_output.sh
```

```bash
cd validation
python3 validate_ligateregions.py
```

####Non-interactive approach
To submit all validation tasks in a single batch, make use of the all_in_one_validation script.

```bash
cd validation
python3 all_in_one_validation.py
```

Ensure that the necessary dependencies (e.g., bcftools, zarr, pyVCF) are installed and available in your PATH.


## Authors and Acknowledgements

This pipeline has been implemented as part of my vector genomics fellowship rotation to the [Data Analysis and Engineering Team](https://www.sanger.ac.uk/group/data-analysis-and-engineering/) at the Wellcome Sanger Institute's [Genomic Surveillance Unit](https://www.sanger.ac.uk/collaboration/genomic-surveillance-unit/). The methodology implemented by early versions of the pipeline is described by [Alistair et. al](https://github.com/malariagen/pipelines/blob/master/docs/specs/phasing-vector.md).

The methods and approach continue to be actively developed by the GSU.


