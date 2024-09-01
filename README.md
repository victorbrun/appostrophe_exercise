# Data engineering exercise | Appostrophe AB

# Introduction

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

# Project plan

## Strtegic considerations 

The goal of this project is to build a data extraction process where marketing data is gathered from (possibly) multiple sources, and a data loading process where the raw data is uploaded to Google BigQuery. Consequently, a natural choice would be to implement an ETL (Extract, Transform, Load) or the more modern alternative, an ELT (Extract, Load, Transform). To determine whether an ETL or ELT is best fit-for-purpose, and to understand which surrounding technologies to use, there are some aspects that require careful consideration:

1. **Ecosystem lock-in:** As the load location of the data is part of Google Cloud Platform (GCP), it would be straightforward to build a complete solution utilising GCP tools. However, ecosystem lock-in needs to be considered to minimise future work if Appostrophe decides to switch cloud providers or move to an on-premise solution.
2. **Robustness and reliability:** This project will act as the interface between "the world" and Appostrophe, and thus needs to be robust while also ensuring that the data it loads into Google BigQuery is reliable.
3. **Scalability:** Although Appostrophe is a start-up, the solution needs to cater for expansion, both in terms of data sources and the amount of data it can handle.
4. **Complexity and maintenance:** Appostrophe is a fast-moving start-up and therefore requires a solution that does not overcomplicate things. The solution should be easily maintained and brought into production within a short time frame.
5. **Data sensitivity:** As data can be highly sensitive, it is necessary to consider whether the data concerning this project requires special treatment due to privacy or sensitivity concerns.

These different aspects are discussed in the following sections.

### Ecosystem lock-in 

### Robustness and reliability

### Scalability

### Complexity and maintenance

### Data sensitivity



## Extraction

## Transform

## Load

# Implementation

# Moving forward

# Sources 
- 
