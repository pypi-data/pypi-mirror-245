import json
import logging
from datetime import datetime
from typing import List

import pandas as pd

from .batch_jobs import BatchJob
from .client_portfolio import TaxLotPortfolio, ClientPortfolio, SimplePortfolio
from .job import Job
from ...omps.omps_service import OMPSSession
from .profile import Profile
from .user_datapoints import UserDataPoint
from ...utils import constants
from ...utils.request_utility import get, post, delete, put
from ...utils.utility import get_token, env_resolver, get_client_environ, validate_date, validate_dataframe_date, \
    get_version
from msci.sdk.calc.portfolio.utils.validations import TypeValidation
from ..... import settings


class MOSSession:
    """
    Interface exposed to users that connects to MSCI Optimization Service and MSCI Portfolio Storage for optimization of equity and cash portfolios.
    """

    client_id = TypeValidation('client_id', str)
    client_secret = TypeValidation('client_secret', str)

    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        Initializes the MOS API session by authenticating the user credentials and generating token for OAuth Authentication mode. The credentials can be passed as a parameter. If the parameters are missing then MSCI_MOS_API_KEY and MSCI_MOS_API_SECRET is expected to be available as environment variables.

        Args:
            client_id(str) : Client ID for connecting to MOS API.
            client_secret(str) : Client secret for connecting to MOS API.

        For details about generating the credentials, refer the MSCI Optimization Service API Reference Guide.

        """
        settings.setup_logging()
        self.logger = logging.getLogger(__name__)

        env_dict = env_resolver('PCS')
        client_id, client_secret = get_client_environ(client_id, client_secret)

        if not client_id or not client_secret:
            self.logger.error("Error in creating MOS session, "
                              "MSCI_MOS_API_KEY and MSCI_MOS_API_SECRET not in the environment")
            raise ValueError("Please specify MSCI_MOS_API_KEY and  MSCI_MOS_API_SECRET in the environment "
                             "or pass client Id and secret as parameter.")

        self.client_id = client_id
        self.client_secret = client_secret
        self.ssl_verify = True

        token = get_token(env_dict["pcs_token_url"], self.client_id, self.client_secret, env_dict["pcs_audience"],
                          'pcs')

        version = get_version()
        self.base_url = env_dict["pcs_base_url"] + "/v" + version + "/"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Src-System": "msci-sdk",
            "Accept-Encoding": "gzip"
        }

        self.logger.debug(
            f"MOS session created with PCS base url : {self.base_url} and version : {version}")

        self.omps_session = OMPSSession(client_id=self.client_id, client_secret=self.client_secret)

        self.user_datapoint = UserDataPoint(base_url=self.base_url, headers=self.headers, ssl_verify=self.ssl_verify)

        self.bulk_request = BatchJob(base_url=self.base_url, headers=self.headers, ssl_verify=self.ssl_verify)

    def get(self, resource: str, params: dict = None, check_200=True):
        """
        Retrieve the specified resource with the passed parameters.

        Args:
            resource(str): The service URL, not including analytics/optimization, such as 'monitoring/ping'.
            params(dict): Dictionary of additional parameters in the request.
            check_200(bool): Default value is True. Raise exception if status code <> 200.

        Returns:
            Response object from requests library including status_code and content.
        """

        mos_url = self.base_url + resource
        return get(url=mos_url, headers=self.headers, params=params, check_200=check_200, ssl_verify=self.ssl_verify)

    def post(self, resource: str, data, check_200=True):
        """
        Post content to the specified resource.

        Args:
            resource(str): The service URL, not including analytics/optimization, such as 'monitoring/ping'.
            data: Dictionary or list of content to post, will be converted to the JSON format.
            check_200(bool): Default value is True. Raise exception if status code <> 200.

        Returns:
            Response object from requests library including status_code and content.
        """

        mos_url = self.base_url + resource
        return post(url=mos_url, headers=self.headers, data=data, check_200=check_200, ssl_verify=self.ssl_verify)

    def put(self, resource: str, data, check_200=True):
        """
        Updates instance of specified resource.

        Args:
            resource(str): The service URL, not including analytics/optimization, such as 'monitoring/ping'.
            data: Dictionary or list of content to post, will be converted to the JSON format.
            check_200(bool): Default value is True. Raise exception if status code <> 200.

        Returns:
            Response object from requests library including status_code and content.
        """

        mos_url = self.base_url + resource
        return put(url=mos_url, headers=self.headers, data=data, check_200=check_200)

    def delete(self, resource: str, params: dict = None, check_200=True):
        """
        Delete the specified resource.

        Args:
            resource(str): The service URL, not including analytics/optimization, such as 'monitoring/ping'.
            params(dict): Dictionary of additional parameters in the request.
            check_200(bool): Default value is True. Raise exception if status code <> 200.

        Returns:
            Response object from requests library including status_code and content.
        """

        mos_url = self.base_url + resource
        return delete(url=mos_url, headers=self.headers, params=params, check_200=check_200, ssl_verify=self.ssl_verify)

    def ping(self):
        """Ping the MOS server to make sure the connection is good."""

        resp_obj = get(url=self.base_url + "monitoring/ping", headers=self.headers, ssl_verify=self.ssl_verify)
        resp = resp_obj.text

        return resp

    def get_portfolio_identifiers(self, vendor_id: str, currency: str = None, return_type: str = None,
                                  name: str = None):
        """
        Retrieve a list of system portfolios by a specific vendor that a user is subscribed to for using in the profile as benchmark or universe. You will need the vendor ID to use this end point.

        Args:
            vendor_id (str) : Vendor ID to identify a vendor.
            currency (str) : Currency to filter. Default value is None.
            return_type (str) : Return type to filter. Default value is None.
            name (str) : Name to filter. Default value is None.

        Returns:
            JSON with universe details.
        """
        resp_obj = get(url=self.base_url + f"portfolio/mappingsIDs/{vendor_id}", headers=self.headers, ssl_verify=self.ssl_verify)
        mds_df = pd.DataFrame(eval(resp_obj.text))

        if currency:
            self.logger.debug(f" Filtering portfolio identifiers for currency : {currency} ")
            mds_df = mds_df.loc[mds_df['currency'] == currency.upper()]
        if return_type:
            self.logger.debug(f" Filtering portfolio identifiers for return Type : {return_type} ")
            mds_df = mds_df.loc[mds_df['returnType'] == return_type.upper()]
        if name:
            self.logger.debug(f" Filtering portfolio identifiers for name like : {name} ")
            mds_df = mds_df[mds_df['name'].str.contains(name.upper())]
        return mds_df

    def load_submitted_jobs(self, from_date: str = None, to_date: str = None) -> pd.DataFrame:
        """
        Load previously submitted jobs. Ordered on descending startTimestamp.
        Usage:
         - Check status of all previously run/submitted jobs
         - Get job_id to get results from previous jobs in case a session disconnects

        Args:
            from_date(str): Start date in the YYYY-MM-DD format. Default value is None.
            to_date(str): End date in the YYYY-MM-DD format. Default value is None.

        Returns:
            Pandas dataframe with details of submitted jobs including their job IDs.
        """
        self.logger.debug(f'Load submitted jobs for from_date :{from_date} and to_date : {to_date}')
        resp_jobs = get(url=self.base_url + "jobs", headers=self.headers, ssl_verify=self.ssl_verify)
        if resp_jobs.json()['jobs']:
            all_jobs_df = pd.json_normalize(resp_jobs.json()['jobs'])
            if from_date:
                self.logger.debug(f'Filtering jobs for from_date : {from_date} ')
                validate_date(from_date)
                all_jobs_df['start_date'] = pd.to_datetime(all_jobs_df['startTimestamp']).dt.date
                all_jobs_df = all_jobs_df.loc[
                    all_jobs_df['start_date'] >= datetime.strptime(from_date, '%Y-%m-%d').date()]
            if to_date:
                self.logger.debug(f'Filtering jobs for to_date : {to_date} ')
                validate_date(to_date)
                all_jobs_df['start_date'] = pd.to_datetime(all_jobs_df['startTimestamp']).dt.date
                all_jobs_df = all_jobs_df.loc[
                    all_jobs_df['start_date'] <= datetime.strptime(to_date, '%Y-%m-%d').date()]
            job_ids = list(all_jobs_df['jobId'])
            if job_ids:
                resp = post(url=self.base_url + "jobs/status?isReturnImmediately=True", headers=self.headers,
                            data=job_ids, ssl_verify=self.ssl_verify)
                jobs_df = pd.json_normalize(resp.json())
                if not jobs_df.empty:
                    return jobs_df.sort_values(['startTimestamp'], ascending=False)
                else:
                    self.logger.info(constants.NO_PREVIOUS_JOB_MESSAGE)
            else:
                self.logger.info(constants.NO_PREVIOUS_JOB_MESSAGE)
        else:
            self.logger.info(constants.NO_PREVIOUS_JOB_MESSAGE)

    def load_job(self, job_id: str) -> Job:
        """
        Load job object. Useful in case a session disconnects after job submission.

        Args:
            job_id(str): Job ID of any initiated/previous job. To retrieve a job ID, use load_submitted_jobs.

        Returns:
            Job object.
        """
        return Job(job_id=job_id, get=self.get, post=self.post)

    def execute(self, profile: Profile):

        """
        Execute the optimization process based on the configured strategy.

        Args:
            profile (Profile) : The profile to execute, which contains all information required to construct a portfolio using the defined        strategy on a specific date or to run a backtest over a period of time.

        Returns:
            Execution job instance.
        """

        self.logger.debug(f"Profile : {json.dumps(profile.body)}")
        resp = post(url=self.base_url + "jobs", headers=self.headers, data=profile.body, ssl_verify=self.ssl_verify)
        job = Job(job_id=resp.text, calculation_type=profile.simulation_settings.calculation_type,
                  get=self.get, post=self.post, profile=profile)
        self.logger.debug(f"Executing profile for job id : {resp.text}")
        return job

    def validate_profile(self, profile: Profile):
        """
        Validates the profile and gives output which includes nullFields, emptyCollections or any other failures.

        Args:
            profile (Profile) : The profile to validate, which contains all information required to construct a portfolio using the defined strategy on a specific date or to run a backtest over a period of time.

        Returns:
            Output in json format.
        """
        resp = post(url=self.base_url + "profileUtils/validateProfile", headers=self.headers, data=profile.body, ssl_verify=self.ssl_verify)
        return resp.json()

    def upload_portfolio(self, as_of_date, asset_id, portfolio_id='BasePortfolio',
                         snapshot_type='CLOSE', initial_cash=None, quantity_type='NumShares',
                         assets: list = None,
                         quantities: list = None):
        """
        Upload Client portfolio without taxlots to OMPS database

        Args:
            as_of_date (str): Portfolio upload date.
            asset_id (str): Asset Id for portfolio upload like ISIN, CUSIP, TICKER.
            portfolio_id (str): Identifier assigned to the uploaded portfolio. Default is 'BasePortfolio'.
            snapshot_type (str):  Allowed snapshots can be OPEN or CLOSE. Default is 'CLOSE'.
            initial_cash (float): Initial cash position in the portfolio, in USD.
            quantity_type (str): quantity type for the portfolio positions, typically NumShares or Weight.
            assets (list): asset identifiers in the asset_id provided.
            quantities (list): asset quantities in the quantity_type provided.

        Returns:
             Generated Client portfolio reference
        """

        validate_date(as_of_date)

        asset_id = asset_id.upper()
        required_identifiers = ['ISIN', 'CUSIP', 'MDSUID', 'TICKER']

        if asset_id not in required_identifiers:
            self.logger.error(f"asset id not among {required_identifiers}")
            raise ValueError(f"asset_id should be one among {required_identifiers}")

        client_portfolio = SimplePortfolio(portfolio_id=portfolio_id, as_of_date=as_of_date, initial_cash=initial_cash,
                                           asset_id=asset_id, quantity_type=quantity_type, assets=assets,
                                           snapshot_type=snapshot_type,
                                           quantities=quantities)

        # UPLOAD PORTFOLIO
        body = client_portfolio.portfolio_body()
        upload_response = self.omps_session.upload_portfolio(portfolio_id, body, snapshotType=snapshot_type)
        if upload_response.json()["success"]:
            self.logger.info(
                f"Succesfully posted portfolio {portfolio_id} for date {as_of_date} with snapshotType {snapshot_type}")
        else:
            self.logger.debug(
                f"Portfolio upload failed for {portfolio_id} for date {as_of_date} with snapshotType {snapshot_type}")

        return client_portfolio

    def upload_taxlot_portfolio(self, as_of_date, asset_id, portfolio_id='BasePortfolio',
                                snapshot_type='CLOSE', initial_cash=None, quantity_type='NumShares',
                                taxlot_file_path=None, taxlot_df=None):
        """
        Upload Client portfolio with taxlots to MSCI Portfolio Storage database

        Args:
            as_of_date (str): Portfolio upload date.
            asset_id (str): Asset ID for portfolio upload like ISIN, CUSIP, TICKER.
            portfolio_id (str): Identifier assigned to the uploaded portfolio. Default is 'BasePortfolio'.
            snapshot_type (str):  Allowed snapshots; can be OPEN or CLOSE. Default is 'CLOSE'.
            initial_cash (float): Initial cash position in the portfolio, in USD.
            quantity_type (str): Quantity type for the portfolio positions, typically NumShares or Weight.
            taxlot_file_path (str): Taxlot data in JSON format from file.
            taxlot_df (dataFrame): Taxlot data in pandas dataframe format.

        Returns:
             Generated user portfolio reference.
        """

        validate_date(as_of_date)

        asset_id = asset_id.upper()
        required_identifiers = ['ISIN', 'CUSIP', 'MDSUID', 'TICKER']

        if taxlot_file_path:
            positions = pd.read_json(taxlot_file_path)
            self.logger.debug(f"taxlot file path : {taxlot_file_path}")
        elif taxlot_df is not None:
            positions = taxlot_df
        else:
            raise ValueError("Please provide either taxlot_file_path or taxlot_df")

        positions_col = list(positions.columns)

        self.logger.debug(f"taxlot file columns : {positions_col}")

        if asset_id not in required_identifiers:
            self.logger.error(f"asset id not among {required_identifiers}")
            raise ValueError(f"asset_id should be one among {required_identifiers}")

        if asset_id not in positions_col:
            self.logger.error(f"asset_id: {asset_id} not present in the portfolio")
            raise ValueError(f"asset_id: {asset_id} not present in the portfolio")

        # To check whether a particular row is NULL(all columns of the row) and if all are NULL then drop them.
        if (positions.isnull().all(axis=1)).any():
            positions = positions.dropna()

        # To raise a value error if any mandatory fields or columns are NULL.
        not_null_cols = ["openTradeDate", asset_id, "quantity", "openCostBasis"]
        null_cols = [column for column in not_null_cols if positions[column].isnull().any()]

        if null_cols:
            error_msg = "Missing value for: " + ", ".join(null_cols)
            raise ValueError(error_msg)

        # Validate date format
        validate_dataframe_date(positions, 'openTradeDate')

        client_portfolio = ClientPortfolio(portfolio_id=portfolio_id, as_of_date=as_of_date, initial_cash=initial_cash)
        tax_portfolio = TaxLotPortfolio(as_of_date, asset_id, portfolio_id=portfolio_id, initial_cash=initial_cash,
                                        quantity_type=quantity_type)
        tax_portfolio.modify_portfolio(portfolio_id, snapshot_type, positions)

        # UPLOAD PORTFOLIO
        body = tax_portfolio.portfolio_body()
        upload_response = self.omps_session.upload_portfolio(portfolio_id, body, snapshotType=snapshot_type)
        if upload_response.json()["success"]:
            self.logger.info(
                f"Succesfully posted portfolio {portfolio_id} for date {as_of_date} with snapshotType {snapshot_type}")
        else:
            self.logger.debug(
                f"Portfolio upload failed for {portfolio_id} for date {as_of_date} with snapshotType {snapshot_type}")

        # UPLOAD TAXLOT
        initial_taxlots_obj = tax_portfolio.taxlot_body()
        upload_response = self.omps_session.upload_taxlot(portfolio_id, as_of_date=as_of_date,
                                                          data=initial_taxlots_obj, snapshotType=snapshot_type)

        if upload_response.json()["success"]:
            self.logger.info(
                f"Succesfully posted tax lots for {portfolio_id} for date {as_of_date} with snapshotType {snapshot_type}")
        else:
            self.logger.debug(
                f"Taxlot upload failed for {portfolio_id} for date {as_of_date} with snapshotType {snapshot_type}")

        return client_portfolio

    def upload_bulk_taxlot_portfolios(self, portfolios: List[TaxLotPortfolio], snapshot_type='CLOSE'):

        portfolios_body = []

        required_identifiers = ['ISIN', 'CUSIP', 'MDSUID', 'TICKER']

        for portfolio in portfolios:
            validate_date(portfolio.as_of_date)

            asset_id = portfolio.asset_id.upper()

            if portfolio.taxlot_file_path:
                positions = pd.read_json(portfolio.taxlot_file_path)
                self.logger.debug(f"taxlot file path : {portfolio.taxlot_file_path}")
            elif portfolio.taxlot_df is not None:
                positions = portfolio.taxlot_df
            else:
                raise ValueError("Please provide either taxlot_file_path or taxlot_df")

            positions_col = list(positions.columns)

            self.logger.debug(f"taxlot file columns : {positions_col}")

            if asset_id not in required_identifiers:
                self.logger.error(f"asset id not among {required_identifiers}")
                raise ValueError(f"asset_id should be one among {required_identifiers}")

            if asset_id not in positions_col:
                self.logger.error(f"asset_id: {asset_id} not present in the portfolio")
                raise ValueError(f"asset_id: {asset_id} not present in the portfolio")

            # To check whether a particular row is NULL(all columns of the row) and if all are NULL then drop them.
            if (positions.isnull().all(axis=1)).any():
                positions = positions.dropna()

            # To raise a value error if any mandatory fields or columns are NULL.
            not_null_cols = ["openTradeDate", asset_id, "quantity", "openCostBasis"]
            null_cols = [column for column in not_null_cols if positions[column].isnull().any()]

            if null_cols:
                error_msg = "Missing value for: " + ", ".join(null_cols)
                raise ValueError(error_msg)

            # Validate date format
            validate_dataframe_date(positions, 'openTradeDate')

            portfolio.modify_portfolio(portfolio_id=portfolio.portfolio_id, snapshot_type=snapshot_type, positions=positions)

            single_body = portfolio.portfolio_body()
            single_body.update({"taxlots": portfolio.taxlot_body()})
            portfolios_body.append(single_body)

        upload_responses = self.omps_session.upload_portfolios(data=portfolios_body, snapshot_type=snapshot_type)
        json_response = upload_responses.json()
        failure_portfolios, success_portfolios = [], []
        for response in json_response:
            if response["success"]:
                success_portfolios.append(response['portfolio']['id'])
            else:
                failure_portfolios.append(response['portfolio']['id'])

        if success_portfolios:
            self.logger.info("Successfully posted portfolios")

        if failure_portfolios:
            self.logger.info(f"Failed to post portfolios: {failure_portfolios}")

    def get_portfolio_taxlots(self, as_of_date, portfolio_id='BasePortfolio', snapshot_type='CLOSE'):
        """

        Get the set of taxlots for a portfolio snapshot as of a specific date.
        This returns the tax lots for the portfolio with additional information about the identifiers found in the system for each.

        Args:
            as_of_date (str): Portfolio upload date.
            portfolio_id (str): Identifier assigned to the uploaded portfolio. Default is 'BasePortfolio'.
            snapshot_type (str):  Allowed snapshots; can be OPEN or CLOSE. Default is 'CLOSE'.

        Returns:
             Uploaded taxlot as of date.
        """

        validate_date(as_of_date)
        self.logger.debug(
            f"Fetching taxlots with portfolio id {portfolio_id} as of date {as_of_date} with snapshot_type {snapshot_type}")
        taxlot = self.omps_session.get_taxlots_asofdate(portfolio_id=portfolio_id, as_of_date=as_of_date,
                                                        snapshotType=snapshot_type,
                                                        instrumentResolutionStrategy='LocatePrimaryID')
        if not taxlot:
            self.logger.info(
                f"No taxlot available with portfolio id:{portfolio_id}, date:{as_of_date} and snapshot_type:{snapshot_type}")
        else:
            return taxlot

    def get_portfolio_positions(self, as_of_date, portfolio_id='BasePortfolio', snapshot_type='CLOSE'):
        """
        Get the set of positions for a portfolio snapshot as of a specific date.
        This returns the positions for the portfolio with additional information about the identifiers found in the system for each.

        Args:
            as_of_date (str): Portfolio upload date.
            portfolio_id (str): Identifier assigned to the uploaded portfolio. Default is 'BasePortfolio'.
            snapshot_type (str):  Allowed snapshots; can be OPEN or CLOSE. Default is 'CLOSE'.

        Returns:
             Uploaded taxlot as of date.
        """

        validate_date(as_of_date)
        self.logger.debug(
            f"Fetching positions with portfolio id {portfolio_id} as of date {as_of_date} with snapshot_type {snapshot_type}")
        positions = self.omps_session.get_positions_asofdate(portfolio_id=portfolio_id, as_of_date=as_of_date,
                                                             snapshotType=snapshot_type,
                                                             instrumentResolutionStrategy='LocatePrimaryID')
        if not positions:
            self.logger.info(
                f"No positions available with portfolio id:{portfolio_id}, date:{as_of_date} and snapshot_type:{snapshot_type}")
        else:
            return positions
