from icecream import ic
from cashctrl import Client

"""
This example shows how to use the limiting functionality.

"""



cc = Client()
ic(cc.limiter.cost())
ic(cc.limiter.cost(since="1 minute"))