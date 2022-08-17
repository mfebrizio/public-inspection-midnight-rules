"""
Mark Febrizio
"""

# %% Initialize
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

p = Path(__file__)
read_dir = p.parents[1].joinpath("data", "processed")
write_dir = p.parents[1].joinpath("data", "analysis")
if write_dir.exists():
    pass
else:
    try:
        write_dir.mkdir(parents=True)
    except:
        print("Cannot create data directory.")


# %% Load data

file_path = read_dir / r"public_inspection_midnight_documents_withdrawn.csv"
with open(file_path, "r", encoding="utf-8") as f:
    df = pd.read_csv(f, index_col=False)
print(f"DataFrame with {len(df)} observations loaded.")


# %% Aggregate data

# groupby year and document type
by_year_type = df.groupby(["year", "type"]).agg({"document_number": "nunique"})
by_year_type = by_year_type.reset_index().rename(columns={"document_number": "documents"})
print(by_year_type)

# groupby year and agency
by_agency_year = df.groupby(["agencies_acronym_uq", "year"]).agg({"document_number": "nunique"})
by_agency_year = by_agency_year.reset_index().rename(columns={"agencies_acronym_uq": "agency", 
                                                              "document_number": "documents"})
print(by_agency_year)


# %% Add implicit zero values to data

bool_dup = by_agency_year.duplicated(subset="agency", keep=False)
missing_ = by_agency_year.loc[~bool_dup, :]
missing_.loc[:, "documents"] = 0
missing_.loc[:, "year"] = missing_.loc[:, "year"].apply(lambda x: 2017 if x==2021 else 2021)

by_agency_year_2 = pd.concat([by_agency_year, missing_], verify_integrity=True, ignore_index=True).sort_values(["agency", "year"], ignore_index=True)
print(by_agency_year_2)


# %% Plot




#plt.
