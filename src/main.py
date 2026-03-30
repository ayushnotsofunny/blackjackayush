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

    def get_value(self):
        total = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == "A")

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def show(self, name):
        if not self.cards:
            print(f"{name}: No cards")
            return

        cards_text = ", ".join(str(card) for card in self.cards)
        print(f"{name}: {cards_text} | Score: {self.get_value()}")


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def take_turn(self, deck):
        while True:
            print()
            self.hand.show(self.name)

            if self.hand.get_value() > 21:
                print(f"{self.name} busted!")
                return

            choice = input("Type 'hit' or 'stand': ").strip().lower()

            if choice == "stand":
                print(f"{self.name} stands.")
                return

            if choice == "hit":
                drawn_card = deck.draw()
                print(f"{self.name} drew: {drawn_card}")

                if drawn_card.suit == "Hearts":
                    result = self.handle_heart_card(drawn_card, deck)
                    if result == "stop":
                        return
                else:
                    self.hand.add_card(drawn_card)

            else:
                print("Invalid input. Please type 'hit' or 'stand'.")

    def handle_heart_card(self, heart_card, deck):
        print("\nHeart card special choice:")
        print("1. Keep the card")
        print("2. Discard the card and redraw once")
        print("3. Stop turn without counting this Heart card")

        while True:
            choice = input("Choose 1, 2, or 3: ").strip()

            if choice == "1":
                self.hand.add_card(heart_card)
                print(f"You kept {heart_card}.")
                return "continue"

            if choice == "2":
                print(f"You discarded {heart_card}.")
                new_card = deck.draw()
                print(f"You redrew: {new_card}")
                self.hand.add_card(new_card)
                return "continue"

            if choice == "3":
                print(f"You stopped. {heart_card} was not counted.")
                return "stop"

            print("Invalid choice. Enter 1, 2, or 3.")


class Monster(Player):
    def __init__(self):
        super().__init__("Monster")

    def take_turn(self, deck, player_score):
        print("\n--- Monster Turn ---")
        time.sleep(2)

        while True:
            self.hand.show(self.name)
            current_score = self.hand.get_value()

            if current_score > 21:
                print("Monster busted!")
                return

            if current_score >= player_score and current_score >= 17:
                time.sleep(2)
                print("Monster stands.")
                return

            print("Monster is thinking...")
            time.sleep(2)

            drawn_card = deck.draw()
            print(f"Monster drew: {drawn_card}")
            time.sleep(2)

            if drawn_card.suit == "Hearts":
                result = self.handle_heart_ai(drawn_card, deck, player_score)
                if result == "stop":
                    return
            else:
                self.hand.add_card(drawn_card)

    def handle_heart_ai(self, heart_card, deck, player_score):
        current_score = self.hand.get_value()
        keep_score = current_score + heart_card.value

        if heart_card.rank == "A" and keep_score > 21:
            keep_score -= 10

        print("Monster is deciding about the Heart card...")
        time.sleep(2)

        if keep_score == 21:
            self.hand.add_card(heart_card)
            print(f"Monster kept {heart_card} and reached 21!")
            time.sleep(2)
            return "continue"

        if keep_score > 21:
            print(f"Monster discarded {heart_card} because it would bust.")
            time.sleep(2)
            redraw = deck.draw()
            print(f"Monster redrew: {redraw}")
            time.sleep(2)
            self.hand.add_card(redraw)
            return "continue"

        if current_score >= player_score and current_score >= 18:
            print(f"Monster stopped and did not count {heart_card}.")
            time.sleep(2)
            return "stop"

        self.hand.add_card(heart_card)
        print(f"Monster kept {heart_card}.")
        time.sleep(2)
        return "continue"


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.monster = Monster()

    def start(self):
        print("=== Blackjack: Heart Twist ===")

        # 1 starting card each
        self.player.hand.add_card(self.deck.draw())
        self.monster.hand.add_card(self.deck.draw())

        print("\n--- Starting Hands ---")
        self.player.hand.show("Player")
        self.monster.hand.show("Monster")

        # Player turn
        print("\n--- Player Turn ---")
        self.player.take_turn(self.deck)

        if self.player.hand.get_value() > 21:
            print("\nMonster wins automatically because the player exceeded 21.")
            return

        # Monster turn
        player_score = self.player.hand.get_value()
        self.monster.take_turn(self.deck, player_score)

        # Final result
        self.show_result()

    def show_result(self):
        player_score = self.player.hand.get_value()
        monster_score = self.monster.hand.get_value()

        print("\n--- Final Result ---")
        self.player.hand.show("Player")
        self.monster.hand.show("Monster")

        if player_score > 21:
            print("Monster wins!")
        elif monster_score > 21:
            print("Player wins!")
        elif player_score > monster_score:
            print("Player wins!")
        elif monster_score > player_score:
            print("Monster wins!")
        else:
            print("It's a tie!")


if __name__ == "__main__":
    game = Game()
    game.start()

