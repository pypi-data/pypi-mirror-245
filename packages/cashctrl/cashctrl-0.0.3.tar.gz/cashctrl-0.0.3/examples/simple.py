from cashctrl import CashCtrlClient
from icecream import ic

# Initialize CashCtrlClient
cc = CashCtrlClient()

# list all accounts
accounts = cc.account.list()
ic(accounts)
