# Data engineering exercise | Appostrophe AB

# 1 Introduction

This repo contains code and documentation related to an exercise provided by Appostrophe AB as part of the interview process for a data engineering position.

The scope of the exercise involves collecation, processing and storage of marketing data for the imaginary iOS app BestPhotoEditor. Below follow the aspects which the solution should take into account:
1. The app was recently released on the AppStore and has a single marketing channel; Meta.
2. The marketing team needs to know the advertisement campaigns on Meta are performing. A data analyst will support them on this toppic, but they need to have the raw data available in Google
BigQuery (BQ) to carry out their analysis.
3. As of now, the marketing campaigns in Meta are composed of five different campaigns focusing on 5 different regions. There are however plans to increase the number of campaigns and regions. Morover, each of the campaigns have multiple adsets and ads.
4. Multiple metrics are relevant for the data team to analyse, but the main ones are: spend, reach, impressions, clicks, attributed installs, attributed conversions.
5. Above metrics need to be combined with the following dimensions: date, country, campaign (name and id), adset (name and id) and ad.

This exercise involves the following tasks:
1. Draft a project plan starting from the data collection phase and ending with the data being put on Google BigQuery, making it readily available for data analysts. The plan ought to detail what software or tools will be used in each step.
2. Write the code needed to gather the required data from the [Facebook Graph API](https://developers.facebook.com/docs/graph-api/).
3. Explain how above mentioned code can be extended to other apps and their related API, e.g., TikTok and Google Ads.

# 2 Project plan

## 2.1 Strategic considerations 

The goal of this project is to build a data extraction process where marketing data is gathered from (possibly) multiple sources, and a data loading process where the raw data is uploaded to Google BigQuery. Consequently, a natural choice would be to implement an ETL (Extract, Transform, Load) or the more modern alternative, an ELT (Extract, Load, Transform). To determine whether an ETL or ELT is best fit-for-purpose, and to understand which surrounding technologies to use, there are some aspects that require careful consideration:

1. **Ecosystem lock-in:** As the load location of the data is part of Google Cloud Platform (GCP), it would be straightforward to build a complete solution utilising GCP tools. However, ecosystem lock-in needs to be considered to minimise future work if Appostrophe decides to switch cloud providers or move to an on-premise solution.
2. **Robustness and reliability:** This project will act as the interface between "the world" and Appostrophe, and thus needs to be robust while also ensuring that the data it loads into Google BigQuery is reliable.
3. **Scalability:** Although Appostrophe is a start-up, the solution needs to cater for expansion, both in terms of data sources and the amount of data it can handle.
4. **Complexity and maintenance:** Appostrophe is a fast-moving start-up and therefore requires a solution that does not overcomplicate things. The solution should be easily maintained and brought into production within a short time frame.
5. **Data sensitivity:** As data can be highly sensitive, it is necessary to consider whether the data concerning this project requires special treatment due to privacy or sensitivity concerns.

## 2.2 Proposed Solution

By implementing an ELT approach, we propose the following steps:

1. **Data Extraction**:
    - Implement an abstract class called `DataExtractor` is containing abstract methods for fetching data via HTTPS, producing Data Quality (DQ) reports, and reports containing a summary of the fetched data. Each API will then have its own implementation of this abstract class containing the API-specific logic. The API-specific class then dumps the data and reports directly into BQ.

2. **Data Loading**:
    - Load the data directly into BQ without any transformation. Create a single dataset for marketing data, where each table contains the data from a specific source (and possibly API version if the schema changes are large enough). Morover, the reports produced by the `DataExtractor` implementations will be put in a separate dataset in a table called `DataQualityReports` and `DataLoadSummary`. Each of these tables will have a column(s) relating it to the the table and subsequently also rows they concern in the marketing dataset. 

3. **Data Transformation**:
    - Create views accessible by data analysts. These views will transform the data into a relational data model.

**Benefits of this ELT Solution:**

- **Ecosystem Flexibility**:
    - Prevent ecosystem lock-in by writing our own data extraction script, which is platform-agnostic, and executing these using Google Cloud Functions. Additionally, the data model provided by views in the transformation step is written in SQL, making it easy to implement on different platforms.

- **Robustness and Reliability**:
    - Ensure robustness and reliability by producing a DQ report. Moreover, by saving the raw input data in a single table, there is no need for advanced logic (e.g., normalising it). Thus, we can examine the data in BQ and confidently assert that it reflects what was provided by the API.

- **Scalability**:
    - Scalability is ensured by selecting serverless GCP products, which can expand to fit the data. The only possible bottleneck may be the views accessed by analysts. If these contain very advanced logic, it may take time to run them, consuming precious compute time, as each view will be run multiple times. This could easily be solved by materialising the views in BQ. By doing this, the results from the views are cached, removing the need for recomputing them upon every access.

- **Simplicity and Maintainability**:
    - Complexity is kept to a minimum by writing as little code as possible (data extraction class and view SQL logic), making it easy to maintain and troubleshoot, as we confine the potentially complicated logic to the views.

- **Data Sensitivity**:
    - Currently, there are no data sensitivity aspects to consider as the Meta marketing data is depersonalised when received from the API. However, since BQ by default encrypts all data before writing it to disk and decrypts it on an authorised request, there are already some data sensitivity measures built into the solution. If the nature of the data changes to include highly personal information, a solution would be to incorporate the depersonalisation of the data in the transformation logic and restrict access to the raw data.

## 2.3 Future Extensions

- **Ecosystem Flexibility**:
    - To further reduce ecosystem lock-in, the data extraction scripts may be containerised using something like Docker. Moreover, the cloud architecture can be written in something like Terraform. This way, the entire project could be version-controlled and hosted on, e.g., GitHub and be automatically deployed using a CI/CD pipeline with GitHub Actions. By hosting the project as a single repository on a solution such as GitHub, convenient documentation and issue tracking tools may also be leveraged.

- **Robustness and Reliability**:
    - Initially, a simple data quality report considering the five DQ dimensions ought to suffice. As the project increases both in scope and possibly also in team members, there is no need to reinvent the wheel. Thus, implementing a DQ tool such as Apache Griffin would be a good extension.

- **Data lineage**:
	- The data load summary report provides data lineage for the between the extraction and load layers. To also provide data lineage in the transformation layer [data lineage in BigQuery](https://cloud.google.com/data-catalog/docs/how-to/track-lineage) ought to be set up.

## TODO
2. Create data model. 
3. Create diagram for solution.
4. Write future extensions.
5. Create diagram for future extension.
6. Write DataExtractor.

