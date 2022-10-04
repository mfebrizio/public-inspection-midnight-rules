# %% Initialize
from pathlib import Path
import pandas as pd

p = Path(__file__)
analysis_dir = p.parents[1].joinpath("data", "analysis")
if analysis_dir.exists():
    pass
else:
    try:
        analysis_dir.mkdir(parents=True, exist_ok=True)
    except:
        print("Cannot create data directory.")


# %% Load data

file_path = analysis_dir / r"documents_withdrawn_archived_checked.csv"
with open(file_path, "r", encoding="utf-8") as f:
    dfChecked = pd.read_csv(f, index_col=False)
print(f"DataFrame with {len(dfChecked)} observations loaded.")

file_path = analysis_dir / r"nprm_data.csv"
with open(file_path, "r", encoding="utf-8") as f:
    dfNPRM = pd.read_csv(f, index_col=False)
print(f"DataFrame with {len(dfNPRM)} observations loaded.")


# %% Merge data

dfMerged = dfChecked.merge(dfNPRM, on="document_number", how="inner", validate="1:1")
print(dfMerged["type"].value_counts(dropna=False))


# %% Clean merged data

keep_cols = ["date", 'pi_url', 
             "document_number", 'document_url', 
             "agencies_acronym_uq", 
             'title_x', 
             'nprm_document_number', 'fr_nprm_url', 
             'nprm_rin', 'rin_url', 
             'rin_priority', 'notes']

dfClean = dfMerged[keep_cols]
dfClean = dfClean.rename(columns={"title_x": "title", "agencies_acronym_uq": "agency"})


# %% Export data

file_path = analysis_dir / r"rules_withdrawn_priority.csv"
with open(file_path, 'w', encoding='utf-8') as f:
    dfClean.to_csv(f, index=False, line_terminator='\n')
print('Exported as CSV!')

