from cashctrl import Client
from icecream import ic

# Initialize CashCtrlClient
cc = Client()

# list all accounts
accounts = cc.account.list()
ic(accounts)
