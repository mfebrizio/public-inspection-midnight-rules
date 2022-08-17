"""
Mark Febrizio
"""

# %% Initialize
import json
from pathlib import Path

import numpy as np
import pandas as pd

from federal_agencies import clean_agencies_column
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

# public inspection data
file_path = read_dir / r"public_inspection_endpoint_midnight_documents.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data["results"])

# agencies metadata
file_path = read_dir / r"agencies_endpoint_metadata.json"
with open(file_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)["results"]


# %% Data cleaning

# filter out duplicates
df = df.drop_duplicates(subset="document_number", keep="first")

# clean up API columns
if "agencies_id_unique" in df.columns:
    pass
else:
    df = clean_agencies_column(df, metadata=metadata)
df.loc[:, "date"] = column_to_date(df, column="public_inspection_issue_date")
df.loc[:, "year"] = df["date"].apply(lambda x: x.year)
df.loc[:, "agency_names"] = df["agency_names"].apply(lambda x: "; ".join(x))

# check for agency letters; drop column if none
if sum(df["agency_letters"].notna()) == 0:
    print("No agency letters.")

# ignoring this for now; let's return all documents to csv with type indicator
# filter by rules
# bool_rules = np.array(df["type"] == "Rule")
# dfRules = df.loc[bool_rules, :]

# filter by has editorial_note
bool_note = np.array(df["editorial_note"].notna())
dfNote = df.loc[bool_note, :]

# search editorial_note for withdrawals
dfWithdrawn = search_columns(dfNote, patterns=[r"\bwithdr[\w]+\b"], columns=["editorial_note"])

# clean agency info for export
cols = ["agencies_slug_uq", "agencies_id_uq", "agencies_acronym_uq"]
for c in cols:
    dfWithdrawn[c] = dfWithdrawn[c].apply(lambda x: "; ".join(str(i) for i in x))


# %% Filter columns

keep_cols = ["year", "date", "type", 
             "agencies_slug_uq", "agencies_id_uq", "agencies_acronym_uq", "agency_names", 
             "document_number", "editorial_note", "json_url"]
dfWithdrawn = dfWithdrawn.loc[:, keep_cols]

# sort df
dfWithdrawn = dfWithdrawn.sort_values(["year", "date", "type", "agencies_slug_uq"], kind="stable")

print(dfWithdrawn.iloc[:,:5].head())


# %% Save processed data

file_path = write_dir / r"public_inspection_midnight_documents_withdrawn.csv"
with open(file_path, 'w', encoding='utf-8') as f:
    dfWithdrawn.to_csv(f, index=False, line_terminator='\n')
print('Exported as CSV!')
