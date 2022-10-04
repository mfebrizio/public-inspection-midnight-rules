# Initialize
from pathlib import Path
from shutil import copyfile

p = Path(__file__)
processed_dir = p.parents[1].joinpath("data", "processed")
analysis_dir = p.parents[1].joinpath("data", "analysis")
sharing_dir = p.parents[1].joinpath("data", "for_sharing")
if sharing_dir.exists():
    pass
else:
    try:
        sharing_dir.mkdir(parents=True, exist_ok=True)
    except:
        print("Cannot create data directory.")

# point to files to copy
dir_list = [processed_dir, analysis_dir]
file_list = ["public_inspection_midnight_documents_all.csv", 
             "documents_by_agency_year.csv", 
             "documents_by_year_type.csv", 
             "documents_withdrawn_archived_checked.csv",
             "nprm_data.csv", 
             "rules_withdrawn_priority.csv", 
             "midnight_rules_by_president_year_month.csv"
             ]

# copy files to sharing_dir
print(f"Attempting to copy {len(file_list)} files...")
for d in dir_list:
    for f in file_list:
        check_file = d / f
        if Path.is_file(check_file):
            new_file = sharing_dir / f
            copyfile(check_file, new_file)
            print(f"Copied {f}")
        else:
            continue

