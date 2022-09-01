# %% Initialize

from pathlib import Path
import pandas as pd
from memento_api import get_date_tuples, get_urls, query_closest_memento

p = Path(__file__)
data_dir = p.parents[1].joinpath("data", "analysis")
if data_dir.exists():
    pass
else:
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except:
        print("Cannot create data directory.")


# %% Load data

file_name = data_dir / r"documents_withdrawn.csv"
with open(file_name, "r") as f:
    df = pd.read_csv(f)

print(f"Observations loaded: {len(df)}")


# %% Format data

dates = get_date_tuples(df)
urls = get_urls(df)

set_list = list(zip(*set(tuple(zip(dates, urls)))))


# %% Query Memento

closest_list = []
for dt, url in zip(*set_list):
    #print(dt, url)
    closest_uri = query_closest_memento(url, dt)
    closest_list.append(closest_uri)


# %% Merge with Dataframe

date_list = (f"{s[1]}/{s[2]}/{s[0]}" for s in set_list[0])
mementos = list(zip(date_list, closest_list))

dfMemento = pd.DataFrame(mementos, columns=["date", "archive_url"])

dfMerged = df.merge(dfMemento, how="left", on="date", 
                    indicator=False, validate="m:1")


# %% Export data

file_path = data_dir / r"documents_withdrawn_archived.csv"
with open(file_path, 'w', encoding='utf-8') as f:
    dfMerged.to_csv(f, index=False, line_terminator='\n')
print('Exported as CSV!')

