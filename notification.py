import tk
from globals import globals
import config

HEIGHT, WIDTH = 100, 30

class Notification:
    def __init__(self):
        background = canvas1.create_rectangle(0, 0, 100, 30, fill="grey40", outline="grey60")
        background = canvas1.create_text(50, 15, text="click")
