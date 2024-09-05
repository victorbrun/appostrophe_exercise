# General imports
import os
import uuid
import requests
import pandas as pd

from typing import Dict, List

# Local imports
from .data_extractor_base import DataExtractorBase

class DataExtractorFacebook(DataExtractorBase):
    """
    Extracts advertising data from the Facebook Graph API or a mock endpoint
    and processes it for further use.

    Attributes
    ----------
    api_version : str
        The version of the Facebook Graph API to use.
    url : str
        The base URL for the Facebook Graph API.
    mandatory_metrics : list
        A list of metrics that must always be fetched.
    access_token : str
        The access token for Facebook Graph API.
    app_secret : str
        The app secret for Facebook Graph API.
    app_id : str
        The app ID for Facebook Graph API.
    ad_account_id : str
        The ID of the advertising account from which to pull data.
    metrics_to_fetch : list
        A list of metrics to be fetched, including mandatory metrics.
    use_mock_end_point : bool,
        A flag indicating whether to use a mock API endpoint.
    mock_api_end_point : str
        The mock API endpoint URL.
    end_point : str
        The constructed Facebook Graph API endpoint to fetch ads insights.
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
        """Initializes the DataExtractorFacebook instance with the necessary credentials and 
        settings for the Facebook Graph API.

        Parameters
        ----------
        access_token : str
            The access token for Facebook Graph API authentication.
        app_secret : str
            The app secret for Facebook Graph API authentication.
        app_id : str
            The app ID for Facebook Graph API.
        ad_account_id : str
            The advertising account ID to fetch data from.
        metrics_to_fetch : list of str
            The list of metrics to be fetched in addition to mandatory metrics.
        use_mock_end_point : bool, default=True
            Whether to use a mock endpoint for testing.

        Raises
        ------
        Exception
            If the MOCK_END_POINT environment variable is not set.
        """
        super().__init__()

        # Mock API endpoint. Used to fetch example data.
        self.mock_api_end_point = os.environ.get("MOCK_END_POINT") 
        if self.mock_api_end_point is None:
            raise Exception("Missing environment variable: MOCK_END_POINT")

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
        """Fetches data from the Facebook Graph API or mock endpoint and returns it as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing all requested advertising data.

        Warns
        -----
        Warning
            If an error occurs during the HTTP request, an empty DataFrame is returned.
        """
        try: 
            return self._fetch_ads_insights()
        except requests.exceptions.RequestException as e:
            print("WARNING: empty dataframe will be returned. Error while fetching data: " + str(e))

            return pd.DataFrame()
       
    def load_to_bq(self, df: pd.DataFrame, **kwargs: Dict):
        """Uploads the provided DataFrame to Google BigQuery.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing the data to be uploaded.
        **kwargs : dict
            Additional arguments for BigQuery upload, e.g. parameters needed to establish
            BQ connection.

        Warns
        -----
        Warning
            If the DataFrame is empty, no data will be uploaded.
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
        """Fetches advertising insights data from the Facebook Graph API.

        This method fetches data at the ad level for yesterday for every add 
        connected to `ad_account_id`, grouped by country, and includes the 
        mandatory and additional metrics specified in `metrics_to_fetch`.

        Returns
        -------
        pd.DataFrame
            A DataFrame where each row represents yesterday's metrics for a given ad 
            in a given country.

        Raises
        ------
        requests.exceptions.HTTPError
            If the API returns an error.
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


