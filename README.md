# public-inspection-midnight-rules

On June 22, 2022, the DC Circuit Court decided *[Humane Society of the United States v. Department of Agriculture](https://www.cadc.uscourts.gov/internet/opinions.nsf/A72330C326BFEC8385258887004DAD10/$file/20-5291-1956030.pdf)* (USDA), finding that the agency could not withdraw a final rule that was made available for public inspection, but not published, without first going through the notice-and-comment process. More information on the background of the court decision and the midnight period can be found in [this article](https://regulatorystudies.columbian.gwu.edu/court-decision-extends-period-issuing-midnight-rules).

This project seeks to make sense of the consequences of the court's decision in *Humane Society v. USDA*, using [Federal Register data](https://www.federalregister.gov/reader-aids/developer-resources/rest-api) to quantify the scope of the public inspection documents affected.

The [Federal Register](https://www.federalregister.gov) is the daily journal of the federal government that publishes official documents such as proposed rules, final rules, agency notices, and executive orders. Before a document is published in a Federal Register issue, it is filed by the Office of the Federal Register (OFR) for “[public inspection](https://www.federalregister.gov/reader-aids/using-federalregister-gov/understanding-public-inspection).” A public inspection document is essentially a preview of the document’s contents and its estimated effective or comment dates, which are typically available the day before it will be published officially.

## Contents

+ **code/**

    A directory containing a set of scripts and modules that implement the data retrieval, processing, and analysis for the project.

+ **data/for_sharing/**

    A directory and sub-directory containing the output data collected and processed for the project.

+ **.gitattributes**

+ **.gitignore**

+ **environment.yml**

+ **LICENSE**

+ **README.md**

## Coding Sequence

This section of the README describes the sequence in which the Python scripts should be run.

1. **retrieve_documents.py** : Retrieve public inspection documents from Federal Register API and save as JSON. Calls modules: *federal_register_api*.

2. **process_documents.py** : Process the retrieved JSON, convert to DataFrame, identify withdrawn documents, and save as CSV. Calls modules: *columns_to_date*, *federal_agencies*, *search_columns*.

3. **analyze_documents.py** : Analyze processed data, calculate aggregations, and create figures. Calls modules: *plots*.

4. **retrieve_web_archives.py** : Retrieves closest available archived webpage to each public inspection edition; adds archived links to withdrawn documents CSV. Calls modules: *memento_api*. Note: [Memento Client's Time Travel tool](http://timetravel.mementoweb.org/) seems to be having issues as of at least October 4, 2022 (502 Bad Gateway), so this script may not function properly.

5. **merge_analyzed_data.py** : Integrate analyzed data with manually collected NPRM data. Calls modules: n/a.

6. **analyze_midnight_rules.py** : Retreives, processes, and analyzes data on midnight rules for comparison with public inspection withdrawals. Calls modules: *columns_to_date*, *federal_agencies*, *federal_register_api*, *presidents*, *search_columns*.

7. **share_data.py** : Copy data files into "data/for_sharing" directory. Calls modules: n/a.

## Publications

Mark Febrizio, "[Quantifying the Effects of Humane Society v. Department of Agriculture](https://regulatorystudies.columbian.gwu.edu/quantifying-effects-humane-society-v-department-agriculture)," GW Regulatory Studies Center Insight, October 05, 2022. [Cross-posted](https://www.yalejreg.com/nc/quantifying-the-effects-of-humane-society-v-department-of-agriculture-by-mark-febrizio/) to Yale JREG's Notice & Comment blog on October 08, 2022.
