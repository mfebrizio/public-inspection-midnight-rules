"""
Mark Febrizio
"""

#%% Initialize
import json
from pathlib import Path

import pandas as pd

#from federal_register_api import query_endpoint_public_inspection

p = Path(__file__)
data_dir = p.parents[1].joinpath("data", "processed")
if data_dir.exists():
    pass
else:
    try:
        data_dir.mkdir(parents=True)
    except:
        print("Cannot create data directory.")


#%% Load data

file_path = data_dir / rf"public_inspection_endpoint_rules_midnight.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data["results"])

