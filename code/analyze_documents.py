"""
Mark Febrizio
"""

# %% Initialize
from pathlib import Path

import pandas as pd

from plots import plot_and_save_barh

p = Path(__file__)
read_dir = p.parents[1].joinpath("data", "processed")
write_dir = p.parents[1].joinpath("data", "analysis")
fig_path = p.parents[1].joinpath("data", "analysis", "figures")
if write_dir.exists() and fig_path.exists():
    pass
else:
    try:
        write_dir.mkdir(parents=True, exist_ok=True)
        fig_path.mkdir(parents=True, exist_ok=True)
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


# %% Plot data

# by type
colors = ["#003b5c", "#a89968", "#009cde"]
labels = {"x": "Number of documents", 
          "y": "Transition year", 
          "t": "Figure 1: Public Inspection Documents Withdrawn by Type", 
          "a": "Source: Federal Register API and author's calculations."
          }
save_path = fig_path / r"withdrawn_by_type.png"

plot_and_save_barh(by_year_type, "documents", "year", "type", 
                   color_list=colors, xlabel=labels["x"], ylabel=labels["y"], 
                   title=labels["t"], 
                   text_annotation=(0.1, 0, labels["a"]), save_as=save_path)

# by agency
colors = ["red", "blue"]
labels = {"x": "Number of documents", 
          "y": "Agency acronym", 
          "t": "Figure 2: Public Inspection Documents Withdrawn by Agency", 
          "a": "Source: Federal Register API and author's calculations.", 
          "leg": "Year"}
save_path = fig_path / r"withdrawn_by_agency.png"

plot_and_save_barh(by_agency_year_2, "documents", "agency", "year", 
                   color_list=colors, xlabel=labels["x"], ylabel=labels["y"], 
                   title=labels["t"], legend_title=labels["leg"], 
                   xlim=(0, 17), xticks=(list(range(0, 18, 3)), None), 
                   text_annotation=(0.1, 0, labels["a"]), save_as=save_path)


# %% Export spreadsheet

base = "https://www.federalregister.gov/public-inspection/"
df.loc[:, "date_slash"] = df["date"].apply(lambda x: x.replace("-", r"/"))
df.loc[:, "pi_url"] = base + df["date_slash"] + "#" + df["filing_type"] + "-filing-" + df["agency_slugs"]

write_cols = ["date", "type", "agencies_acronym_uq", "title", "pi_url"]

file_path = write_dir / r"documents_withdrawn.csv"
with open(file_path, 'w', encoding='utf-8') as f:
    df.to_csv(f, index=False, line_terminator='\n', columns=write_cols)
print('Exported as CSV!')

