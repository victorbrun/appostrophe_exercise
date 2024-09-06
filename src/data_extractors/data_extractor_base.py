import uuid
import pandas as pd

from abc import ABC, abstractmethod
from typing import Any, Dict

class DataExtractorBase(ABC):
    """
    Abstract base class for data extractors.

    This class provides the interface and common functionality for classes that extract
    data from external sources (e.g., APIs) and load it into Google BigQuery.

    Attributes
    ----------
    bq_connection : BigQueryConnection
        A connection object to interact with Google BigQuery.

    Methods
    -------
    fetch_data()
        Fetches and returns the consolidated data as a pandas DataFrame.
    load_to_bq(df, **kwargs)
        Loads the provided data into Google BigQuery.
    create_dq_report(df)
        Creates a Data Quality (DQ) report for the given DataFrame.
    create_dump_summary(df)
        Creates a summary mapping between unique rows and the data extraction process.
    _add_row_id(df)
        Adds a unique identifier for each row in the DataFrame.
    """

    def __init__(self, bq_connection: Any):
        """
        Initialize the DataExtractorBase with a Google BigQuery connection.

        Parameters
        ----------
        bq_connection : BigQueryConnection
            The connection object to interact with Google BigQuery for loading data.
        """
        self.bq_connection = bq_connection

    @abstractmethod
    def fetch_data(self) -> pd.DataFrame:
        """
        Returns a single pandas dataframe containing all necessary
        data from the implemented API.

        Note: the README specifies that all data related to one API
        (except DQ and summary reports) will be uploaded to a single 
        table in BQ. This is the explanation for this function only returning
        a single dataframe. Thus, it may be needed to coalesce multiple
        API calls below (in the call stack) this function.

        Returns
        -------
        pd.DataFrame
            Single consolidated dataframe.
        """
        return

    @abstractmethod
    def load_to_bq(self, df: pd.DataFrame, **kwargs: Dict):
        """
        Uploads data in ´df´ to Google BigQuery.

        Parameters
        ----------
        table : pd.DataFrame
            The pandas DataFrame containing the data to be uploaded to BigQuery.
        **kwargs : dict
            Additional arguments for customisation during the loading process.
        """
        return

    def create_dq_report(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates a DQ report for `df` based on:
            1. Accuracy
            2. Completeness
            3. Consistency
            4. Timeliness
            5. Validity

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame for which the DQ report is generated.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the results of the DQ report.
        """
        raise NotImplementedError()

    def create_dump_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates a map between unique row numbers in `df`
        and execution of the extract process.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame for which the dump summary is created.

        Returns
        -------
        pd.DataFrame
            DataFrame with the mapping between unique rows and the data extraction process.
        """
        raise NotImplementedError()

    def _add_row_id(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a unique identifier for each row in `df`.
         
        NOTE: if the dataset grows very large, this
        method will not work. Reason being that the hash 
        used to create the ID is just very unlikely to 
        not produce the same value twice, but not 100%.
        A suggested solution would be to establish a connection with 
        Google BigQuery and generate a truly unique 
        row ID by double checking that it does not exist.
        
        Parameters
        ----------
        df : pd.DataFrame 
            DataFrame to which the column "row_id" will be added. 
            This column contains a "unique" id.

        Returns 
        -------
        pd.DataFrame 
            Input DataFrame but with the column "row_id" added.
        """
        df["row_id"] = [uuid.uuid4() for _ in range(df.shape[0])]
        return df
