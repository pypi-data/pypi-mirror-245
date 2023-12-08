from typing import Union

from ...utils.validations import TypeValidation, StringDateFormat
import re


class ClientPortfolio:
    """
    Wrapper around the portfolio service using the same session as MOS.

    Args:
        portfolio_id (str): (optional) Identifier assigned to cash portfolio. Default value is BaseCashPortfolio.
        as_of_date (str): As of date in the YYYY-MM-DD format.

    Returns:
        body (dict): Dictionary representation of ClientPortfolio.
    """

    portfolio_id = TypeValidation('portfolio_id', str)
    as_of_date = StringDateFormat('as_of_date')
    initial_cash = TypeValidation('initial_cash', [int, float])

    def __init__(self, portfolio_id="BasePortfolio",
                 as_of_date=None,
                 initial_cash=0):
        self.portfolio_id = portfolio_id
        self.as_of_date = as_of_date
        self.initial_cash = initial_cash

    @property
    def body(self):
        """
        Generates the request body as dictionary based on the parameter passed.

        Returns:
            dict: Dictionary representation of the node.
        """
        body = {
            "objType": "PortfolioSearchInput",
            "identification": {
                "source": "OMPS",
                "objType": "SimpleIdentification",
                "portfolioId": self.portfolio_id,
            },
        }
        return body

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.__dict__}>"


class TaxLotPortfolio(ClientPortfolio):
    """
   Upload tax lots portfolio. Inherits class ClientPortfolio.

    Args:
        portfolio_id (str): (optional) Identifier assigned to cash portfolio. Default value is BaseCashPortfolio.
        as_of_date (str): As of date in the YYYY-MM-DD format.
        asset_id (str) : Asset ID.

    Returns:
        body (dict): Dictionary representation of TaxLotPortfolio.
    """

    as_of_date = StringDateFormat('as_of_date', mandatory=True)
    asset_id = TypeValidation('asset_id', str, mandatory=True)
    portfolio_id = TypeValidation('portfolio_id', str)

    def __init__(self, as_of_date,
                 asset_id,
                 portfolio_id="BasePortfolio",
                 quantity_type="NumShares",
                 initial_cash: Union[int, float] = None,
                 taxlot_file_path=None,
                 taxlot_df=None
                 ):
        super().__init__(portfolio_id, as_of_date=as_of_date, initial_cash=initial_cash)
        self.asset_id = asset_id
        self.initial_cash = initial_cash
        self.quantity_type = quantity_type
        self.taxlot_file_path = taxlot_file_path
        self.taxlot_df = taxlot_df

    def taxlots_to_shares_obj(self):
        """
        Method to create JSON objects from positions data.
        """

        asset_id = self.asset_id
        initial_shares = self.positions.groupby(self.asset_id).sum(numeric_only=True)
        initial_shares.reset_index(inplace=True)
        initial_shares["quantityType"] = self.quantity_type
        initial_shares["instrument"] = [
            {"primaryId": {"id": iid, "idType": asset_id}}
            for iid in initial_shares[asset_id]
        ]

        initial_shares_obj = initial_shares.drop(
            columns=[asset_id, "openCostBasis"]
        ).to_dict(orient="records")

        # Adding initial cash component
        if self.initial_cash is not None:
            taxlot_init_cash_rec = {
                'quantity': self.initial_cash,
                'quantityType': self.quantity_type,
                'instrument': {'primaryId': {'id': "USD", 'idType': "MDSUID"}},
            }

            initial_shares_obj.append(taxlot_init_cash_rec)

        return initial_shares_obj

    def portfolio_body(self):
        """
        Method to create portfolio body for uploading to MSCI Portfolio Storage in JSON format.
        """
        initial_shares_obj = self.taxlots_to_shares_obj()
        taxlot_initial_portfolio = {
            "id": self.portfolio_id,
            "asOfDate": self.as_of_date,
            "snapshotType": self.snapshot_type,
            "baseCurrency": "USD",
            "positions": initial_shares_obj,
        }
        return taxlot_initial_portfolio

    def taxlot_body(self):
        """
        Method to create taxlot body for uploading to MSCI Portfolio Storage in JSON format.
        """
        asset_id = self.asset_id
        initial_taxlots = self.positions
        pattern = r'[^a-zA-Z0-9]'
        initial_taxlots[asset_id] = initial_taxlots[asset_id].apply(lambda x: re.sub(pattern, '', x))
        initial_taxlots["id"] = initial_taxlots.apply(
            lambda x: [x[asset_id] + "_qty_" + x["openTradeDate"]][0], axis=1
        )

        # add a sequence number to discriminate lots opened on the same date
        initial_taxlots['lotSeq'] = initial_taxlots.groupby('id').cumcount()
        initial_taxlots['id'] = initial_taxlots['id'] + \
                                '_' + initial_taxlots['lotSeq'].apply(str)

        initial_taxlots["instrument"] = [
            {"primaryId": {"id": isin, "idType": asset_id}}
            for isin in initial_taxlots[asset_id]
        ]

        obj_columns = [
            "openTradeDate",
            "quantity",
            "quantityType",
            "status",
            "portfolioID",
            "openCostBasisPrice",
            "id",
            "instrument",
        ]
        initial_taxlots_obj = initial_taxlots[[f for f in obj_columns]].to_dict(
            orient="records"
        )
        return initial_taxlots_obj

    def modify_portfolio(self, portfolio_id, snapshot_type, positions):
        """
        Method to update position data provided by user by addition additional properties.
        """
        self.snapshot_type = snapshot_type

        positions = positions.copy()
        # Modifying the positions df and adding columns to dataframe
        positions['quantityType'] = self.quantity_type
        positions['status'] = 'Open'
        positions['portfolioID'] = portfolio_id
        positions['openCostBasisPrice'] = positions.apply(lambda x: ['USD ' + str(x['openCostBasis'])][0], axis=1)
        self.positions = positions
        return positions


class CashPortfolio(ClientPortfolio):
    """
    Creates a cash portfolio for optimization. Inherits class ClientPortfolio.
    
    Args:
        portfolio_id (str): (optional) Identifier assigned to cash portfolio. Default value is BaseCashPortfolio.
        initial_cash (float, int): (optional) Cash value in USD. Default value is 10 million USD.

    Returns:
        body (dict): Dictionary representation of CashPortfolio.

    """

    portfolio_id = TypeValidation('portfolio_id', str)
    initial_cash = TypeValidation('initial_cash', [float, int])

    def __init__(self, portfolio_id="BaseCashPortfolio", initial_cash=10000000):
        super().__init__(portfolio_id)
        self.initial_cash = initial_cash

    @property
    def body(self):
        """
        Generates the request body as dictionary based on the parameter passed.

        Returns:
            dict: Dictionary representation of the node.
        """
        return {
            "objType": "InlineCashPortfolio",
            "initialAmount": self.initial_cash,
            "currency": "USD",
        }


class SimplePortfolio(ClientPortfolio):
    """
    Upload simple portfolio (no taxlots). Inherits class ClientPortfolio.

    Args:
        portfolio_id (str): (optional) Identifier assigned to cash portfolio. Default value is BaseCashPortfolio.
        as_of_date (str): As of date in the YYYY-MM-DD format.
        asset_id (str) : Asset ID.
        initial_cash (float): (optional) Cash component in the portfolio in USD.

    Returns:
        body (dict): Dictionary representation of SimplePortfolio.
    """
    as_of_date = StringDateFormat('as_of_date', mandatory=True)
    asset_id = TypeValidation('asset_id', str, mandatory=True)
    portfolio_id = TypeValidation('portfolio_id', str)

    def __init__(self, as_of_date,
                 asset_id,
                 portfolio_id="BasePortfolio",
                 snapshot_type="CLOSE",
                 quantity_type="NumShares",
                 initial_cash: Union[int, float] = None,
                 assets: list = None,
                 quantities: list = None):

        super().__init__(portfolio_id, as_of_date=as_of_date, initial_cash=initial_cash)
        self.asset_id = asset_id
        self.snapshot_type = snapshot_type
        self.initial_cash = initial_cash
        self.quantity_type = quantity_type
        self.quantities = quantities
        self.assets = assets

    def shares_obj(self):
        """
        Method to create positions data.
        """

        initial_shares_obj = list()
        for q in range(len(self.quantities)):
            tmp = {
                'quantity': self.quantities[q],
                'quantityType': self.quantity_type,
                'instrument': {"primaryId": {"id": self.assets[q], "idType": self.asset_id}}
            }
            initial_shares_obj.append(tmp)

        # Adding initial cash component
        if self.initial_cash is not None:
            initial_cash_rec = {
                'quantity': self.initial_cash,
                'quantityType': self.quantity_type,
                'instrument': {'primaryId': {'id': "USD", 'idType': "MDSUID"}},
            }

            initial_shares_obj.append(initial_cash_rec)

        return initial_shares_obj

    def portfolio_body(self):
        """
        Method to create portfolio body for uploading to MSCI Portfolio Storage in JSON format.
        """
        initial_shares_obj = self.shares_obj()
        initial_portfolio = {
            "id": self.portfolio_id,
            "asOfDate": self.as_of_date,
            "snapshotType": self.snapshot_type,
            "baseCurrency": "USD",
            "positions": initial_shares_obj,
        }
        return initial_portfolio
