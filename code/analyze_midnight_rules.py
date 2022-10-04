# %% Init

import json
from pathlib import Path
import numpy as np
import pandas as pd
from columns_to_date import column_to_date
from federal_agencies import clean_agencies_column
from federal_register_api import query_endpoint_documents
from presidents import clean_president_column
from search_columns import search_columns

p = Path(__file__)
raw_dir = p.parents[1].joinpath("data", "raw")
analysis_dir = p.parents[1].joinpath("data", "analysis")


# %% Retrieve documents
response = query_endpoint_documents()

# save retrieved data
file_path = raw_dir / r"documents_endpoint_midnight_documents.json"
with open(file_path, "w", encoding="utf-8") as outfile:
    json.dump(response, outfile, indent=4)
print("Exported as JSON!")


# %% Load data

# dataframe for retrieved documents
df = pd.DataFrame(response["results"])

# load agencies metadata
file_path = raw_dir / r"agencies_endpoint_metadata.json"
with open(file_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)["results"]


# %% Process documents

df["date"] = column_to_date(df, column = "publication_date")
df["year"] = df["date"].apply(lambda x: x.year)
df["month"] = df["date"].apply(lambda x: x.month)
df = clean_agencies_column(df, metadata=metadata)
df = clean_president_column(df)

df = search_columns(df, patterns = [r"\bcorrecti[\w]+\b"], columns=["title", "action", "dates"]
                    )

print(df["indicator"].value_counts(dropna=False))

#bool_issuing_president = np.array(df["president_id"]=="barack-obama" & (df["year"]==2016 | df["year"]==2017)) | np.array(df["president_id"]=="donald-trump" & (df["year"]==2020 | df["year"]==2021))
bool_type = np.array(df["type"]=="Rule")
bool_notcorrection = np.array(df["indicator"]==0) & np.array(df["correction_of"].isna())
dfRules = df.loc[bool_type & bool_notcorrection, :]
print(len(dfRules))


# %% Aggregate data

by_prez_yyyy_mm = dfRules.groupby(["president_id", "year", "month"]).agg({"document_number": "nunique"})
by_prez_yyyy_mm = by_prez_yyyy_mm.reset_index()
print(by_prez_yyyy_mm)


# %% Save data

file_path = analysis_dir / r"midnight_rules_by_president_year_month.csv"
with open(file_path, 'w', encoding='utf-8') as f:
    by_prez_yyyy_mm.to_csv(f, index=False, line_terminator='\n')
print('Exported as CSV!')

