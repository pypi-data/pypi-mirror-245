import logging
from cashctrl import CashCtrlClient
from icecream import ic
logging.basicConfig(level=logging.INFO)

cc= CashCtrlClient()
tools_account=cc.account.list(query="tools",sort="name",dir="ASC")
ic(tools_account)