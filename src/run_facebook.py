import os

from dotenv import load_dotenv, find_dotenv

from data_extractors import DataExtractorFacebook

USE_MOCK_API = True

def main():
    # Loading in dotenv file containig
    # all very secret end points and keys
    load_dotenv(find_dotenv())


    # Extracting Facebook ads environment variables
    access_token = os.environ.get("ACCESS_TOKE")
    app_secret = os.environ.get("APP_SECRET")
    app_id = os.environ.get("APP_ID")
    ad_account_id = os.environ.get("AD_ACCOUNT_ID")

    # Specifying the metrics to fetch from 
    # the Facebook Graph API. Note that
    # this has no effect when using the 
    # mock API end point
    metrics_to_fetch = [
        "spend",
        "clicks",
        "reach",
        "impressions",
        "atrributed_installs",
        "attributed_conversions"
    ]


    de = DataExtractorFacebook(
       access_token=access_token,
       app_secret=app_secret,
       app_id=app_id,
       ad_account_id=ad_account_id,
       metrics_to_fetch=metrics_to_fetch,
       use_mock_end_point=USE_MOCK_API
    )

    # Fetching and printing the table which would 
    # be written to Google BigQuery if this solution 
    # was put in production
    df = de.fetch_data()
    print(df)

    

if __name__ == "__main__":
    main()
