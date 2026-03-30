import random
import time

class Card:
    def __init__(self,suit,rank,value):
        self.suit=suit
        self.rank=rank
        self.value=value

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.cards=[]
        suits=["Heart","Diamond","Club","Spade"]
        id={
            "A": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            }
        
        for suit in suits:
            for rank, value in ranks.items():
                self.cards.append(Card(suit,rank, value))

        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
    
class Hand:
    def __init__(self):
        self.cards=[]
    def add_card(self,card):
        self.cards.append(card)
        