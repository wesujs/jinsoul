import os
from dotenv import load_dotenv
import random as r
load_dotenv()

class Config:
    # Bot Settings
    def __init__(self):
        self.colors = [
            "d2b9c5",
            "f482c1",
            "fdc0d1",
            "984064",
            "473058"
        ]
    # Random Colors For Embeds
    def get_embed_color(self):
        return int("0x" + r.choice(self.colors), 16)

    def owner_id(self):
        return 703112459313217556

config = Config()