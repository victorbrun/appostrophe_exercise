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

1. **Ecosystem lock-in**: As the load location of the data is part of Google Cloud Platform (GCP), it would be straightforward to build a complete solution utilising GCP tools. However, ecosystem lock-in needs to be considered to minimise future work if Appostrophe decides to switch cloud providers or move to an on-premise solution.
2. **Robustness and reliability**: This project will act as the interface between "the world" and Appostrophe, and thus needs to be robust while also ensuring that the data it loads into Google BigQuery is reliable.
3. **Scalability**: Although Appostrophe is a start-up, the solution needs to cater for expansion, both in terms of data sources and the amount of data it can handle.
4. **Complexity and maintenance:** Appostrophe is a fast-moving start-up and therefore requires a solution that does not overcomplicate things. The solution should be easily maintained and brought into production within a short time frame.
5. **Data sensitivity**: As data can be highly sensitive, it is necessary to consider whether the data concerning this project requires special treatment due to privacy or sensitivity concerns.

## 2.2 Proposed Solution

By implementing an ELT approach, we propose the following steps:

1. **Data Extraction**:
    - Implement an abstract class called `DataExtractorBase` is containing abstract methods for fetching data via HTTPS, producing Data Quality (DQ) reports, and reports containing a summary of the fetched data. Each API will then have its own implementation of this abstract class containing the API-specific logic. The API-specific class then dumps the data and reports directly into BQ.

2. **Data Loading**:
    - Load the data directly into BQ without any transformation. Create a single dataset for marketing data, where each table contains the data from a specific source (and possibly API version if the schema changes are large enough). Morover, the reports produced by the `DataExtractorBase` implementations will be put in a separate dataset in a table called `DataQualityReports` and `DataLoadSummary`. Each of these tables will have a column(s) relating it to the the table and subsequently also rows they concern in the marketing dataset. 

3. **Data Transformation**:
    - Create views accessible by data analysts. These views will transform the data into a relational data model.

Beacuse the transformations in the exctraction layer, i.e. turning JSON data into a tabular format, are very simple, there is no need for advanched orchestration. Instead the solution will rely on a Cloud Scheduler to run the extraction procedure once every day. Moreover, due to the simple structure of the data uploaded to BQ in the load layer, different APIs will not independent. This means that every API can have a separate Cloud Function running the extraction script in parallel. 

Benefits of this ELT Solution:

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
    - To further reduce ecosystem lock-in, the data extraction scripts could be containerised using a tool like Docker. Additionally, the cloud architecture could be defined using Terraform. This approach allows the entire project to be version-controlled, hosted on platforms like GitHub, and automatically deployed using a CI/CD pipeline with GitHub Actions. By hosting the project as a single repository on a platform like GitHub, convenient documentation and issue-tracking tools can also be utilised.

- **Robustness and Reliability**:
    - Initially, a simple data quality report considering the five DQ dimensions ought to suffice. As the project increases both in scope and team members, there is no need to reinvent the wheel. Thus, implementing a DQ tool such as Apache Griffin would be a valuable extension.

- **Scalability, Simplicity and Maintainability**: As the project app grows, a multitude of different data sources may be added. And as the analysts require more advanced metrics, the transformations done in the materialised views may become increasingly complex. Moreover, the code for these transformations could become poorly organised if they are all considered to be at the same level. To solve this, one could implement a medallion data architecture with its bronze, silver, and gold layers utilising different datasets in BQ. The bronze layer would consist of the tables as described in the initial proposed solution. The silver layer would contain slightly transformed data, e.g., null value treatment, outlier removal, etc. The gold layer would contain the tables or views accessible to analysts. By following this architecture, the SQL code performing the transformations can be organised by `bronze -> silver` and `silver -> gold`.

- **Data lineage**:
	- The data load summary report provides data lineage for the between the extraction and load layers. To also provide data lineage in the transformation layer [data lineage in BigQuery](https://cloud.google.com/data-catalog/docs/how-to/track-lineage) ought to be set up.

Batch loading of the size of the data becomes very large. Current implementation just loads everything for one day into RAM.

## 2.4 Timeline
Below are the time estimates for implementing the initially proposed solution by a single developer, i.e., without extentsions.

- **Extract (3/2/1 weeks)**: 
	- Implementing the abstract class `DataExtractorBase` and the class `FacebookGraphDataExtractor(DataExtractorBase)` will take two weeks, as the logic for the different reports need to be carefully laid out in order to ensure proper data lineage. The implementation of the Facebook Graph API will take one week, as the transformation from JSON to a table format will be very simple. Note that these two tasks can be done somewhat in parallel, with one person developing the abstract class while the other implements the bulk of the logic to fetch the data.
	- The second API to be implemented is estimated to take two weeks. The reason for this is that some, if not all, of the abstract class `DataExtractorBase` will have to be rewritten to ensure that it is flexible enough to properly encompass multiple APIs.
	- Subsequent APIs is estimated to take around one week to implement.

- **Load (1 week)**: Implementing this step involves configuring BQ and setting up the datasets. This is expected to take one week for someone with limited experience with Google Cloud Platform.

- **Transform (5 weeks)**: This step is estimated to take five weeks, even though some transformations are independent and can be developed in parallel. The large allocation of time is attributed to creating a data model, as well as going back and forth with analysts to develop the transformations they request. However, including the analysts in this step, i.e., allowing them to also write the transformations, could probably shorten this process by a week, as this back-and-forth would not be needed to the same extent

From above, we can conclude that the total estimated time for this project is 9 weeks. However, it is possible to shorten this time by putting multiple developers on it, and by letting analysts help out with the development of the transformation step.

# 3 Implementation

In `src/data_extractors/` a partial implementation of the abstract class `DataExtractorBase` and the class `DataExtractorFacebook` can be foud. The functinality of these are explained above, and the code is thoruoghly documented. In `src/` a script for executing above implementation of `DataExtractorFacebook` can be found. For explenations on the functionallity of these classes and functions, you are refered to the source code, as it well commented.

**Note**: to be able to run `src/run_facebook.py` a `.env` file containing the environment variable `MOCK_END_POINT` must be present at the root of this project. This endpoint ought to be set to the one provided in the exercise description.
