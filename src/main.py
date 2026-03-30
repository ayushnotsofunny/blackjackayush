import random
import time

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = {
            "A": 1, "2": 2, "3": 3, "4": 4, "5": 5,
            "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "J": 10, "Q": 10, "K": 10
        }
        for s in suits:
            for r, v in ranks.items():
                self.cards.append(Card(s, r, v))
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add(self, c):
        self.cards.append(c)

    def value(self):
        return sum(c.value for c in self.cards)

    def show(self, name):
        if not self.cards:
            print(name + ": No cards")
            return
        print(name + ": " + ", ".join(str(c) for c in self.cards) + " | " + str(self.value()))

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def turn(self, deck):
        while True:
            print()
            self.hand.show(self.name)

            if self.hand.value() > 21:
                print(self.name + " busted")
                return

            x = input("hit or stand: ").strip().lower()

            if x == "stand":
                print(self.name + " stands")
                return

            elif x == "hit":
                c = deck.draw()
                print(self.name + " drew " + str(c))

                if c.suit == "Hearts":
                    self.heart(c, deck)
                else:
                    self.hand.add(c)
            else:
                print("type hit or stand")

    def heart(self, c, deck):
        print("heart card")
        print("1 keep  2 discard")

        while True:
            x = input("choose: ").strip()

            if x == "1":
                self.hand.add(c)
                print("kept " + str(c))
                return

            elif x == "2":
                print("discarded " + str(c))
                n = deck.draw()
                print("new card " + str(n))
                self.hand.add(n)
                return

            else:
                print("choose 1 or 2")

class Monster(Player):
    def __init__(self):
        super().__init__("Monster")

    def turn(self, deck, ps):
        print("\nmonster turn")
        time.sleep(2)

        while True:
            self.hand.show("Monster")
            s = self.hand.value()

            if s > 21:
                print("monster busted")
                return

            if s >= ps and s >= 17:
                print("monster stands")
                return

            print("monster thinking...")
            time.sleep(2)

            c = deck.draw()
            print("monster drew " + str(c))
            time.sleep(2)

            if c.suit == "Hearts":
                self.heart_ai(c, deck, ps)
            else:
                self.hand.add(c)

    def heart_ai(self, c, deck, ps):
        s = self.hand.value()
        ns = s + c.value

        print("monster deciding...")
        time.sleep(2)

        if ns <= 21:
            self.hand.add(c)
            print("monster keeps " + str(c))
        else:
            print("monster discards " + str(c))
            n = deck.draw()
            print("monster new card " + str(n))
            self.hand.add(n)

class Game:
    def __init__(self):
        self.deck = Deck()
        self.p = Player("Player")
        self.m = Monster()

    def start(self):
        print("blackjack heart")

        self.p.hand.add(self.deck.draw())
        self.m.hand.add(self.deck.draw())

        print("\nstart")
        self.p.hand.show("Player")
        print("Monster: hidden")

        print("\nplayer turn")
        self.p.turn(self.deck)

        if self.p.hand.value() > 21:
            print("monster wins")
            return

        ps = self.p.hand.value()
        self.m.turn(self.deck, ps)

        self.result()

    def result(self):
        p = self.p.hand.value()
        m = self.m.hand.value()

        print("\nresult")
        self.p.hand.show("Player")
        self.m.hand.show("Monster")

        if p > 21:
            print("monster wins")
        elif m > 21:
            print("player wins")
        elif p > m:
            print("player wins")
        elif m > p:
            print("monster wins")
        else:
            print("tie")

if __name__ == "__main__":
    g = Game()
    g.start()