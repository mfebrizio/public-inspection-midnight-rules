"""
Mark Febrizio
Last revised: 2022-08-16
"""

# --------------------------------------------------
# Initialize
import json
from pathlib import Path

from federal_register_api import query_endpoint_public_inspection

p = Path(__file__)
data_dir = p.parents[1].joinpath("data", "raw")
if data_dir.exists():
    pass
else:
    try:
        data_dir.mkdir(parents=True)
    except:
        print("Cannot create data directory.")

# --------------------------------------------------
# retrieve data from API
dctsRules = query_endpoint_public_inspection()

# --------------------------------------------------
# export json file
file_path = data_dir / r"public_inspection_endpoint_midnight_documents.json"
with open(file_path, "w", encoding="utf-8") as outfile:
    json.dump(dctsRules, outfile, indent=4)

print("Exported as JSON!")

