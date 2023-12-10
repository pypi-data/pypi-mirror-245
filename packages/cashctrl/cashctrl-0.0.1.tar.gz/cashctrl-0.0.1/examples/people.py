from cashctrl import CashCtrlClient
from icecream import ic

cc=CashCtrlClient()
people=cc.person.list()
ic(people)
