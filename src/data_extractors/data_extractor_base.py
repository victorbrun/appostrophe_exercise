import uuid
import pandas as pd

from abc import ABC, abstractmethod

class DataExtractorBase(ABC):
    """
    """

    def __init__(self):
        """
        """
        pass

    @abstractmethod
    def fetch_data(self) -> pd.DataFrame:
        """Returns a single pandas dataframe containing all necessary
        data from the implemented API.

        Note: the README specifies that all data related to one API
        (except DQ and summary reports) will be uploaded to a single 
        table in BQ. This is the explenation for this funciton only returning
        a single dataframe. Thus, that may be needed to coalesce multiple
        API calls need to be performed below (in the call stack) this funciton.

        Returns
        -------
        pd.DataFrame
            Single consolidated dataframe.
        """
        return

    @abstractmethod
    def load_to_bq(self, table: pd.DataFrame, **kwargs):
        """Establishes connection to Google BigQuery and uploads
        data in `table` to correct location.
        """ 
        return

    def create_dq_report(self, df: pd.DataFrame) -> pd.DataFrame:
        """Creates a DQ report for `df` based on:
            1. Accuracy
            2. Completeness
            3. Consistency
            4. Timeliness
            5. Validity
        """
        raise NotImplementedError()

    def create_dump_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Creates a map between unique row numbers in `df`
        and execution of exctract process.
        """
        raise NotImplementedError()

    def _add_row_id(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds a unique identifier for each row in `df`.
         
         NOTE: if the dataset grows very large, this
         method will not work. Reason being that the hash 
         used to create the ID is just very unlikely to 
         not produce the same value twice, but not 100%.
         A suggest solution would be to establish a connection with 
         Google BigQuery and generate a truly unique 
         row ID by double checking that it does not exist.
        
        Parameters
        ----------
        df : pd.DataFrame 
            Dataframe to which the column "row_id" will be added. 
            This column contains a "unique" id.

        Returns 
        -------
        pd.DataFrame 
            Input dataframe but with the column "row_id" added.
        """
        df["row_id"] = [uuid.uuid4() for _ in range(df.shape[0])]
        return df
