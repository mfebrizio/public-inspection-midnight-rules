# --------------------------------------------------
from datetime import date
import json
from pathlib import Path

import requests

# --------------------------------------------------
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
# configure requests: Federal Register API
# documentation: https://www.federalregister.gov/developers/documentation/api/v1/
# endpoint: /documents.{format} -- results since 1994

# define endpoint url
endpoint_url = r"https://www.federalregister.gov/api/v1/public-inspection-documents.json?"

# define parameters
res_per_page = 1000
page_offset = 0  # both 0 and 1 return first page

fieldsList = ["agencies", "agency_letters", "agency_names", 
              "document_number", "editorial_note", "filing_type", 
              "json_url", "publication_date", "type"]

years = list(map(str, list(2001, 2009, 2017, 2021)))
days = [f"01-{x}" for x in range(15,20)]

# dictionary of parameters
dcts_params = {"per_page": res_per_page,
               "page": page_offset,
               "fields[]": fieldsList,
               "conditions[available_on]": ""
               }

# check API configuration
print(years, "\n")
test_response = requests.get(endpoint_url, params=dcts_params)
request_url = test_response.url
print(request_url)

# --------------------------------------------------
# retrieve data from Federal Register API
# create objects
dctsResults_all = []
dctsCount_all = 0

# for loop to pull data for each publication year
for year in years:
    print(f"\n***** Retrieving results for year = {year} *****")

    dctsResults = []
    dctsCount = 0
    # for loop to pull data for each quarter
    for d in days:
        available_on = f"{year}-{d}"

        # update parameters for year
        dcts_params.update({"conditions[available_on]": available_on})

        # get documents
        dcts_response = requests.get(endpoint_url, params=dcts_params)
        print(dcts_response.status_code,
              dcts_response.headers[""],
              dcts_response.url, sep="\n")  # print request URL

        # set variables
        dctsCount += dcts_response.json()["count"]
        dctsPages = dcts_response.json()["total_pages"]  # number of pages to retrieve all results

        # for loop for grabbing results from each page
        for page in range(1, dctsPages + 1):
            dcts_params.update({"page": page})
            dcts_response = requests.get(endpoint_url, params=dcts_params)
            results_this_page = dcts_response.json()["results"]
            dctsResults.extend(results_this_page)
            print("Results retrieved = " + str(len(dctsResults)))

    # create dictionary for year to export as json
    if len(dctsResults) == dctsCount:
        dctsRules_one_year = {"source": "Federal Register API",
                              "endpoint": "https://www.federalregister.gov/api/v1/documents.{format}",
                              "requestURL": request_url,
                              "dateRetrieved": str(date.today()),
                              "count": dctsCount,
                              "results": dctsResults}

        filePath = data_dir / rf"documents_endpoint_rules_{year}.json"
        with open(filePath, "w", encoding="utf-8") as outfile:
            json.dump(dctsRules_one_year, outfile, indent=4)

        print("Retrieved all results for " + str(year) + "!")

    else:
        print("Counts do not align for " + str(year) + ": " + str(len(dctsResults)) + " =/= " + str(dctsCount))

    # extend list of cumulative results and counts
    dctsResults_all.extend(dctsResults)
    dctsCount_all = dctsCount_all + dctsCount

# save params for export with metadata
save_params = dcts_params.copy()
save_params.pop("page")
save_params.pop("per_page")
save_params.pop("conditions[publication_date][gte]")
save_params.pop("conditions[publication_date][lte]")

# create dictionary of data with retrieval date
dctsRules = {"source": "Federal Register API, https://www.federalregister.gov/reader-aids/developer-resources/rest-api",
             "endpoint": endpoint_url,
             "requestURL": request_url,
             "dateUpdated": str(date.today()),
             "params": save_params,
             "count": dctsCount_all,
             "results": dctsResults_all}
if dctsRules["count"] == len(dctsRules["results"]):
    print("\nDictionary with retrieval date created!")
else:
    print("\nError creating dictionary...")

# export json file
filePath = data_dir / rf"public_inspection_endpoint_rules_midnight.json"
with open(filePath, "w", encoding="utf-8") as outfile:
    json.dump(dctsRules, outfile, indent=4)

print("Exported as JSON!")



