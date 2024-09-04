# General imports
import os
import uuid
import requests
import pandas as pd

from typing import List

# Local imports
from data_extractor_base import DataExtractorBase

class DataExtractorFacebook(DataExtractorBase):
    """
    """

    # Instance invariant Facebook Graph API params
    api_version = "20.0"
    url = f"https://graph.facebook.com/{api_version}/"

    # List over instance invariant metrics which are 
    # mandatory to be fetched
    mandatory_metrics = [
        "campaign_name",
        "campaign_id",
        "ad_name",
        "ad_id",
        "adset_name",
        "adset_id",
        "date_start",
        "date_stop",
        "country"
    ]


    def __init__(
        self, 
        access_token: str, 
        app_secret: str,
        app_id: str,
        ad_account_id: str,
        metrics_to_fetch: List[str],
        use_mock_end_point: bool = True
    ):
        """
        """
        super().__init__()

        # Mock API endpoint. Used to fetch example data.
        self.mock_api_end_point = os.environ.get("MOCK_END_POINT") 

        # Sets attributes
        self.access_token = access_token
        self.app_secret = app_secret
        self.app_id = app_id
        self.ad_account_id = ad_account_id
        self.use_mock_end_point = use_mock_end_point

        # Setting metrics to fetch and ensuring 
        # the inclusion of all necessary metrics 
        self.metrics_to_fetch = list(set(metrics_to_fetch + self.mandatory_metrics))

        # Consructs endpoint as this is dependent on account id
        self.end_point = self.url + f"act_{self.ad_account_id}/insights"
   
    def fetch_data(self) -> pd.DataFrame:
        """Returns a single pandas containing all necessary data from the implemented
        API.

        Returns
        -------
        pd.DataFrame
            Single consolidated dataframe.
        """
        try: 
            return self._fetch_ads_insights()
        except requests.exceptions.RequestException as e:
            print("WARNING: empty dataframe will be returned. Error while fetching data: " + str(e))

            return pd.DataFrame()
       
    def load_to_bq(self, df: pd.DataFrame, **kwargs):
        """Establishes connection to Google BigQuery and uploads
        the data in `df` to correct location.
        """
        # If df is empty dataframe no data will be uploaded
        if df.empty:
            print("WARNING: No data supplied. No data will be writen to Google BigQuery.")
            return

        # Produces data quality and dump summary reports
        dq_report = self.create_dq_report(df)
        dump_summary = self.create_dump_summary(df)

        raise NotImplementedError()

    def _fetch_ads_insights(self) -> pd.DataFrame:
        """For each add connected to the account 
        identifier by `self.ad_account_id`, it fetches
        the following data:
            - Campaign name
            - Campaign id
            - Ad name
            - Ad id
            - Adset name 
            - Adset id 
            - Date start 
            - Day end
            - Country
            - Any additional metrics specified in metrics_to_fetch 
            constructor argument.

        The data has a daily resolution and always concerns yesterday.

        Returns
        -------
        pd.DataFrame
            Dataframe where each row represents yesterdays metrics for a given ad
            in a given country.
        """
        # Constructs payload for request 
        payload = {
            "level": "ad", # Data will be given on an ad level of resolution
            "date_preset": "yesterday", # Getting yesterdays data
            "breakdowns": "country", # Grouping data by country
            "fields": ",".join(self.metrics_to_fetch),
            "access_token": self.access_token,
        }

        # Performs HTTP call to Facebook Graph API if 
        # mock api is not active.
        data = {}
        if self.use_mock_end_point:
            req = requests.get(self.mock_api_end_point).json()
            data = req["data"]
        else:
            req = requests.get(self.end_point, params=payload).json()

            # If return code is not OK we raise exception
            if "error" in req:
                raise requests.exceptions.HTTPError(req["error"]["message"])

            data = req["data"]

        # Constructing pandas dataframe
        df = pd.DataFrame(data=data)

        # Adding unique row id 
        df = self._add_row_id(df)

        return df


