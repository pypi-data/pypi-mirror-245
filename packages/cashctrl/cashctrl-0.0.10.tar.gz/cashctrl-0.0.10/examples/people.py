from cashctrl import Client
from icecream import ic

cc=Client()
people=cc.person.list()
ic(people)
