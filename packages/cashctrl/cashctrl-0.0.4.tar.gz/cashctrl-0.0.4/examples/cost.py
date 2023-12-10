from icecream import ic
from cashctrl import CashCtrlClient

"""
This example shows how to use the limiting functionality.

"""



cc = CashCtrlClient()
ic(cc.limiter.cost())
ic(cc.limiter.cost(since="1 minute"))