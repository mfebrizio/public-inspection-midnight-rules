"""
Mark Febrizio
"""

# %% Initialize
import json
from pathlib import Path

import numpy as np
import pandas as pd

from clean_agencies import FR_clean_agencies
from columns_to_date import column_to_date

p = Path(__file__)
read_dir = p.parents[1].joinpath("data", "raw")
write_dir = p.parents[1].joinpath("data", "processed")
if write_dir.exists():
    pass
else:
    try:
        write_dir.mkdir(parents=True)
    except:
        print("Cannot create data directory.")


# %% Load data

file_path = read_dir / rf"public_inspection_endpoint_rules_midnight.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data["results"])


# %%

print(df["public_inspection_issue_date"].value_counts(dropna=False))
print(df.columns)


# %% Data cleaning

# clean up API columns
df = FR_clean_agencies(df)
df.loc[:, "date"] = column_to_date(df, column="public_inspection_issue_date")
df.loc[:, "year"] = df["date"].apply(lambda x: x.year)

# filter by rules
bool_rules = np.array(df["type"] == "Rule")
dfRules = df.loc[bool_rules, :]

# filter by has editorial_note
bool_note = np.array(dfRules["editorial_note"].notna())
dfWithdrawn = dfRules.loc[bool_note, :]

# %% Filter columns

keep_cols = ["year", "date", "agencies_id_uq", "agencies_slug_uq", "agency_names", 
             "agency_letters", "document_number", "editorial_note", "json_url"]
print(dfWithdrawn.loc[:, keep_cols])


# %%
