import random
import time

class Card:
    def __init__(self,type,id,value):
        self.type=type
        self.id=id
        self.value=value

    def __str__(self):
        return f"{self.id} of {self.type}"
    
class Deck:
    def __init__(self):
        self.cards=[]
        type=["Heart","Diamond","Club","Spade"]
        ranks={""}