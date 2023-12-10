import logging
from cashctrl import Client
from icecream import ic
logging.basicConfig(level=logging.INFO)

cc= Client()
tools_account=cc.account.list(query="tools",sort="name",dir="ASC")
ic(tools_account)