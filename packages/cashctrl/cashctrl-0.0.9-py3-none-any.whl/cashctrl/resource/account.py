from cashctrl.base import CashCtrlResource
from icecream import ic


class Account(CashCtrlResource):
    """
    The following API endpoints are for managing accounts.
    To avoid confusion: We are talking about financial accounts (assets, liabilities, etc.), not user accounts.
    """

    def __init__(self, client):
        super().__init__(client, 'account')

    def read(self, id):
        """
            Returns a single account by ID.
        """
        return super().read(id)

    def list(self, **kwargs):
        """
            Retrieves a list of accounts.

            :param categoryId: The ID of the category to filter the list by.
            :type categoryId: int, optional
            :param dir: The direction of the sort order. Defaults to 'ASC'.
            :type dir: str, optional
            :param filter: An array of filters to filter the list. All filters must match (AND).
            :type filter: list[dict], optional
                - comparison (str, optional): Comparison type. Possible values: 'eq', 'like', 'gt', 'lt'.
                - field (str, optional): The name of the column to filter by.
                - value (str or list, optional): Text to filter by, or a JSON array of multiple values (OR).
            :param fiscalPeriodId: The ID of the fiscal period, from which we retrieve the balances.
            :type fiscalPeriodId: int, optional
            :param onlyActive: Flag to only include active accounts. Defaults to false.
            :type onlyActive: bool, optional
            :param onlyCostCenters: Flag to only include entries with cost centers. Defaults to false.
            :type onlyCostCenters: bool, optional
            :param onlyNotes: Flag to only include entries with notes. Defaults to false.
            :type onlyNotes: bool, optional
            :param query: Fulltext search query.
            :type query: str, optional
            :param sort: The column to sort the list by. Defaults to 'number'.
            :type sort: str, optional
            :return: A list of filtered and sorted items.
            :rtype: list
        """
        return super().list(**kwargs)
