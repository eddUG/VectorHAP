import subprocess

# List of validation scripts and their descriptions
validations = [
    ("validate_manifest.py", "Validate Input Manifest"),
    ("validate_selectvariants_output.sh", "Validate SelectVariants Output"),
    ("validate_bgziptabix.py", "Validate Bgzip and Tabix"),
    ("validate_whatshapPhase.py", "Validate WhatsHap Phase"),
    #("validate_whatshapStats.py", "Validate WhatsHap Stats"),
    #("validate_mergeVcfs.py", "Validate MergeVcfs"),
    #("validate_bgziptabixII.py", "Validate BgzipAndTabixII"),
    #("validate_shapeit.py", "Validate SHAPEIT"),
    #("validate_tabixII.py", "Validate TabixII"),
    #("validate_ligateChunks.py", "Validate LigateRegions"),
    #("validate_cohortvcf2zarr.py", "Validate cohortVcfToZarr")
]

# Function to run a script and return the result
def run_script(script):
    try:
        result = subprocess.run(["python", script] if script.endswith(".py") else ["bash", script], capture_output=True, text=True)
        success = result.returncode == 0
        details = result.stderr if not success else result.stdout
        return success, details.strip()
    except Exception as e:
        return False, str(e)

# Run all validation scripts and collect results
results = {}
for script, description in validations:
    success, details = run_script(script)
    results[description] = {"status": success, "details": details}

# Generate checklist report
def generate_validation_report(results):
    report = []
    report.append("Validation Checklist Report")
    report.append("==============================")

    for step, result in results.items():
        if result['status']:
            report.append(f"{step}: \033[92mSuccess\033[0m")
        else:
            report.append(f"{step}: \033[91mFailed\033[0m")
            if 'details' in result:
                report.append(f"  Details: {result['details']}")
        report.append("------------------------------")

    return "\n".join(report)

# Generate and print the report
report = generate_validation_report(results)
print(report)

# Save the report to a file
with open("validation_report.txt", "w") as report_file:
    report_file.write(report)
