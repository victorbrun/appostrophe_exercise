import os

from dotenv import load_dotenv, find_dotenv

from data_extractors import DataExtractorFacebook

USE_MOCK_API = True

def main():
    """
    Function showcasing how the extract and load script running on 
    Google Clound Functions may look.
    """
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

    # Initalising object to handle interface with
    # Facebook Graph API and Google BQ
    de = DataExtractorFacebook(
       access_token=access_token,
       app_secret=app_secret,
       app_id=app_id,
       ad_account_id=ad_account_id,
       bq_connection={}, # Placeholder connection
       metrics_to_fetch=metrics_to_fetch,
       use_mock_end_point=USE_MOCK_API
    )

    # Fetching and data from Facebook. 
    # We are also printing the data just to
    # showcase that it works. This would not
    # be done in production.
    df = de.fetch_data()
    print(df)

    # Uploading data to BQ
    placeholder_kwargs = {"target_table": "marketing.facebook_graph_v20_0"}
    de.load_to_bq(df, bq_settings=placeholder_kwargs)

if __name__ == "__main__":
    main()
