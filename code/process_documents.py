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
from search_columns import search_columns

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


# %% Data cleaning

# clean up API columns
if "agencies_id_unique" in df.columns:
    pass
else:
    df = FR_clean_agencies(df)
df.loc[:, "date"] = column_to_date(df, column="public_inspection_issue_date")
df.loc[:, "year"] = df["date"].apply(lambda x: x.year)
df.loc[:, "agency_names"] = df["agency_names"].apply(lambda x: "; ".join(x))

# check for agency letters; drop column if none
if sum(df["agency_letters"].notna()) == 0:
    print("No agency letters.")

# filter by rules
bool_rules = np.array(df["type"] == "Rule")
dfRules = df.loc[bool_rules, :]

# filter by has editorial_note
bool_note = np.array(dfRules["editorial_note"].notna())
dfNote = dfRules.loc[bool_note, :]

# search editorial_note for withdrawals
dfWithdrawn = search_columns(dfNote, patterns=[r"\bwithdr[\w]+\b"], columns=["editorial_note"])


# %% Filter columns

keep_cols = ["year", "date", "agencies_slug_uq", "agency_names", 
             "document_number", "editorial_note", "json_url"]
dfWithdrawn = dfWithdrawn.loc[:, keep_cols]


# %% Save processed data

file_path = write_dir / rf"public_inspection_midnight_rules_withdrawn.csv"
with open(file_path, 'w', encoding='utf-8') as f:
    dfWithdrawn.to_csv(f, index_label='index', line_terminator='\n')
print('Exported as CSV!')

