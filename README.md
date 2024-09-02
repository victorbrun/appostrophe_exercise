# Data engineering exercise | Appostrophe AB

# 1 Introduction

This repo contains code and documentation related to an exercise provided by Appostrophe AB as part of the interview process for a data engineering position.

The scope of the exercise involves collecation, processing and storage of marketing data for the imaginary iOS app BestPhotoEditor. Below follow the aspects which the solution should take into account:
1. The app was recently released on the AppStore and has a single marketing channel; Meta.
2. The marketing team needs to know the advertisement campaigns on Meta are performing. A data analyst will support them on this toppic, but they need to have the raw data available in Google
BigQuery to carry out their analysis.
3. As of now, the marketing campaigns in Meta are composed of five different campaigns focusing on 5 different regions. There are however plans to increase the number of campaigns and regions. Morover, each of the campaigns have multiple adsets and ads.
4. Multiple metrics are relevant for the data team to analyse, but the main ones are: spend, reach, impressions, clicks, attributed installs, attributed conversions.
5. Above metrics need to be combined with the following dimensions: date, country, campaign (name and id), adset (name and id) and ad.

This exercise involes the following tasks:
1. Draft a project plan starting from the data collection phase and ending with the data being put on Google BigQuery, making it readily available for data analysts. The plan ought to detail what software or tools will be used in each step.
2. Write the code needed to gather the required data from the [Facebook Graph API](https://developers.facebook.com/docs/graph-api/).
3. Explain how above mentioned code can be extended to other apps and their related API, e.g., TikTok and Google Ads.

# 2 Project plan

## 2.1 Strtegic considerations 

The goal of this project is to build a data extraction process where marketing data is gathered from (possibly) multiple sources, and a data loading process where the raw data is uploaded to Google BigQuery. Consequently, a natural choice would be to implement an ETL (Extract, Transform, Load) or the more modern alternative, an ELT (Extract, Load, Transform). To determine whether an ETL or ELT is best fit-for-purpose, and to understand which surrounding technologies to use, there are some aspects that require careful consideration:

1. **Ecosystem lock-in:** As the load location of the data is part of Google Cloud Platform (GCP), it would be straightforward to build a complete solution utilising GCP tools. However, ecosystem lock-in needs to be considered to minimise future work if Appostrophe decides to switch cloud providers or move to an on-premise solution.
2. **Robustness and reliability:** This project will act as the interface between "the world" and Appostrophe, and thus needs to be robust while also ensuring that the data it loads into Google BigQuery is reliable.
3. **Scalability:** Although Appostrophe is a start-up, the solution needs to cater for expansion, both in terms of data sources and the amount of data it can handle.
4. **Complexity and maintenance:** Appostrophe is a fast-moving start-up and therefore requires a solution that does not overcomplicate things. The solution should be easily maintained and brought into production within a short time frame.
5. **Data sensitivity:** As data can be highly sensitive, it is necessary to consider whether the data concerning this project requires special treatment due to privacy or sensitivity concerns.

## 2.2 Proposed solution

By implementing an ELT approach, we propose the following steps:

1. Data Extraction:
	- A class called DataExtractor fetches the data via HTTPS. This class then dumps the data into a designated storage location and produces a data quality (DQ) report summarising the five dimensions of data quality. The DQ report also contains a summary of the data that was added to BigQuery.

2. Data Loading:
	- Load the data directly into BigQuery (BQ) without any transformation. Create a single dataset for marketing data, where each table contains the data from a specific source. Note that if the source API changes, a new table could be created. If only a single new column is added, old missing values can simply be set to null.

3. Data Transformation:
	- Create views accessible by data analysts. These views will transform the data into a relational data model.

Benefits of this ELT Solution:

- Ecosystem Flexibility:
	- Prevent ecosystem lock-in by writing our own data extraction script, which is platform-agnostic. Additionally, the data model provided by views in the transformation step is written in SQL, making it easy to implement on different platforms.

- Robustness and Reliability:
	- Ensuring robustness and reliability by producing a DQ report. Moreover, by saving the raw input data in a single table, there is no need for advanced logic (e.g., normalising it). Thus, we can examine the data in BQ and confidently assert that it reflects what was provided by the API.

- Scalability:
		- Scalability is ensured by selecting serverless GCP products, which can expand to fit the data. The only possible bottleneck may be the views accessed by analysts. If these contain very advanced logic, it may take time to run them, consuming precious compute time, as each view will be run multiple times. This could easily be solved by extending the solution with an additional BQ dataset, which is the output of the views, thereby turning the old BQ into a staging BQ that only contains the transformation logic and the raw data.

- Simplicity and Maintainability:
	- Complexity is kept to a minimum by writing as little code as possible (data extraction class and view SQL logic), making it easy to maintain and troubleshoot, as we confine the potentially complicated logic to the views.

- Data Sensitivity:
	- Currently, there are no data sensitivity aspects to consider as the Meta marketing data is depersonalised when received from the API. If this changes with additional data sources, a solution would be to create this staging dataset and incorporate the depersonalisation of the data in the transformation logic.

Note: If the staging dataset is created, this approach would transition from an ELT to an ETL.

## 2.3 Future extensions

## TODO
2. Create data model. 
3. Create diagram for solution.
4. Write future extensions.
5. Create diagram for future extension.
6. Write DataExtractor.

