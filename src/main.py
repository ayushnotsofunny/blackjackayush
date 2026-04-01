import os
import sys
import random
import textwrap
import pygame

GAME_PATH=os.path.dirname(os.path.abspath(__file__))

def get_asset_path(filename: str) -> str:
    return os.path.join(GAME_PATH, "assets",filename)

#This is the Window Setup Dimensions and Game Name 
WIDTH, HEIGHT=1280,820
FPS=60
TITLE="Kumari Vs Malla King"

#This is the Card Layot
CARD_W, CARD_H=100, 140
CARD_GAP=112

#Color Red Black & Grey: Newari Traditional Colors
RED=(160,35,35)
BLACK = (20, 20, 20)
GREY = (155, 155, 155)
LIGHT_GREY = (235, 235, 235)
DARK_GREY = (90, 90, 90)
WHITE = (248, 248, 248)

#This is a cultural disclaimer so no one would get offended for the storyline of the game in future
DISCLAIMER_TITLE="Cultural Disclaimer"
DISCLAIMER_PARAGRAPHS=[
        (
        "This game is inspired by the rich traditions and legends of Nepal, "
        "including the sacred relationship between the Living Goddess Kumari and "
        "the goddess Taleju Bhawani. It draws loosely from stories associated with "
        "the Malla kings and the origins of the Kumari tradition."
    ),
    (
        "The storyline, characters, and outcomes in this game are fictional and "
        "reimagined for creative and entertainment purposes. They are not intended "
        "to represent or alter the authentic religious beliefs, historical accounts, "
        "or cultural practices connected to the Kumari or Taleju Bhawani."
    ),
    (
        "We deeply respect the cultural and spiritual significance of the Kumari "
        "tradition in Nepal and encourage players to learn about its true history "
        "and meaning beyond this game."
    ),
    "Player discretion and cultural sensitivity are appreciated.",

]

HISTORY_PARAGRAPHS = [
    (
        "Legend says the Kumari is the living goddess, a symbol of grace, power, "
        "and divine protection in Newar culture."
    ),
    (
        "Taleju Bhawani is revered as a powerful goddess connected to the old "
        "Malla courts and the sacred stories of the valley."
    ),
    (
        "In this game, Kumari faces the Malla King in a symbolic card duel. It is "
        "a fictional retelling made with respect, not a literal history lesson."
    ),
]

class Button:
    def __init__(self, rect, text, font, bg=LIGHT_GREY, fg=BLACK):
        self.rect=pygame.Rect(rect)
        self.text=text
        self.font=font
        self.bg=bg
        self.fg=fg

    def draw(self, screen, mouse_pos):
        hover=self.rect.collidepoint(mouse_pos)
        color=tuple(max(0,c-15) for c in self.bg) if hover else self.bg
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen,BLACK,self.rect, width=2,border_radius=12)
        label=self.font.render(self.text, True,self.fg)
        screen.blit(label,label.get_rect(center=self.rect.center))

    def clicked(self,event):
        return (
            event.type==pygame.MOUSEBUTTONDOWN
            and event.button==1
            and self.rect.collidepoint(event.pos)
        )
    
class Card:
    def __init__(self,suit,rank,value):
        self.suit=suit
        self.rank=rank
        self.value=value

    def __str(self):
        return f"{self.rank} of {self.suit}"
    
    def color(self):
        return RED if self.suit in ("Hearts","Diamonds") else BLACK
    
    def suit_symbol(self):
         return {
            "Hearts": "♥",
            "Diamonds": "♦",
            "Clubs": "♣",
            "Spades": "♠",
        }[self.suit]
    
class Deck:
    def __init__(self):
        self.cards=[]
        suits=["Hearts","Diamonds","Clubs","Spades"]
        ranks={
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
            "J": 10,
            "Q": 10,
            "K": 10,
        }
        for suit in suits:
            for rank, value in ranks.items():
                self.cards.append(Card(suit,rank,value))

        random.shuffle(self.cards)

    def draw(self):
        #This is to make new deck if the old one runs out. So that the game never ends
        if not self.cards:
            self.__init__()
        return self.cards.pop()
    
class Hand:
    def __init__(self):
        self.cards=[]

    def add(self,card):
        self.cards.append(card)

    def value(self):
        return sum(card.value for card in self.cards)
    
class Player:
    def __init__(self,name):
        self.name=name
        self.hand=Hand()

class MallaKing(Player):
    def __init__(self):
        super().__init__("Malla King")

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen=pygame.display.set_mode((Width,HEIGHT))
        self.clock=pygame.time.Clock()
        self.title_font=pygame.font.SysFont("dejavusans",34,bold=True)
        self.section_font=pygame.font.SysFont("dejavusans",28,bold=True)
        self.font=pygame.font.SysFont("dejavusans", 22, bold=True)
        self.small_font = pygame.font.SysFont("dejavusans", 18)
        self.tiny_font = pygame.font.SysFont("dejavusans", 15)
        self.symbol_font = pygame.font.SysFont("dejavusans", 40, bold=True)
        self.intro_body_font = pygame.font.SysFont("dejavusans", 17)
        self.intro_small_font = pygame.font.SysFont("dejavusans", 16)
        self.hit_btn = Button((70, 700, 120, 50), "Hit", self.font, bg=LIGHT_GREY)
        self.stand_btn = Button((205, 700, 130, 50), "Stand", self.font, bg=GREY)
        self.restart_btn = Button((1020, 40, 190, 50), "Play Again", self.font, bg=RED, fg=WHITE)
        self.start_btn = Button((465, 728, 350, 54), "Enter the Kingdom", self.font, bg=RED, fg=WHITE)
        self.keep_btn = Button((910, 484, 125, 48), "Keep", self.font, bg=RED, fg=WHITE)
        self.discard_btn = Button((1050, 484, 145, 48), "Discard", self.font, bg=GREY)
        self.running = True
        self.show_intro = True
        self.reset_round()

    def reset_round(self):
        self.deck=Deck()
        self.player=Player("Kumari")
        self.monster=MallaKing()
        self.player.hand=Hand()
        self.monster.hand=Hand()
        self.player.hand.add(self.deck.draw())
        self.monster.hand.add(self.deck.draw())
        self.state="player_turn"
        self.pending_heart=None
        self.message="Kumari's turn. Choose wisely: Hit or Stand"
        self.result_text=""
        self.result_subtext=""
        self.monster_timer=0

    def draw_text(self,text,font,color,x,y,center=False):
        surf=font.render(text,True,color)
        rect=surf.get_rect(center=(x,y)) if center else surf.get_rect(topleft=(x,y))
        self.screen.blit(surf, rect)

    def draw_paragrapgh(self,text,font,color,rect,line_gap=6):
        words=text.split()
        lines=[]
        current=""

        for word in words:
            test=word if not current else f"{current}{word}"
            if font.size(test)[0]<=rect.width:
                current=test
            else:
                lines.append(current)
                current=word
        
        if current:
            lines.append(current)

        y=rect.y
        for line in lines:
            surf=font.render(line,True,color)
            self.screen.blit(srf,(rect.x,y))
            y+=surf.get_height()+line_gap
        return y
    
    def draw_intro_screen(self):
        self.screen.fill(GREY)
        panel=pygame.Rect(36,24,WIDTH-72,HEIGHT-48)
        pygame.draw.rect(self.screem,WHITE,panel,border_radius=24)
        pygame.draw.rect(self.screem,BLACK,panel,width=4,border_radius=24)
        self.draw_text(TITLE,self.title_font,RED,WIDTH//2,54,center=True)
        left_x=78
        right_margin=WIDTH-78
        content_w=right_margin-left_x
        self.draw_text(DISCLAIMER_TITLE,self.section_font,BLACK,left_x,108)
        y=152
        for paragraph in DISCLAIMER_PARAGRAPHS:
            y=self.draw_paragrapgh(
                paragraph,
                self.intro_body_font,
                BLACK,
                pygame.Rect(left_x,y,content_w-10,120),
                line_gap=4,
            )
            y+=14

            history_box=pygame.Rect(68,540,WIDTH-136,150)
            pygame.draw.rect(self.screen,LIGHT_GREY,history_box,border_radius=18)
            pygame.draw.rect(self.screen,RED,history_box,width=3,border_radius=18)
            self.draw_text("A Short Story Before the Game")

# import random
# # test 1
# # test 2
# import time

# class Card:
#     def __init__(self, suit, rank, value):
#         self.suit = suit
#         self.rank = rank
#         self.value = value

#     def __str__(self):
#         return f"{self.rank} of {self.suit}"

# class Deck:
#     def __init__(self):
#         self.cards = []
#         suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
#         ranks = {
#             "A": 1, "2": 2, "3": 3, "4": 4, "5": 5,
#             "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
#             "J": 10, "Q": 10, "K": 10
#         }
#         for s in suits:
#             for r, v in ranks.items():
#                 self.cards.append(Card(s, r, v))
#         random.shuffle(self.cards)

#     def draw(self):
#         return self.cards.pop()

# class Hand:
#     def __init__(self):
#         self.cards = []

#     def add(self, c):
#         self.cards.append(c)

#     def value(self):
#         return sum(c.value for c in self.cards)

#     def show(self, name):
#         if not self.cards:
#             print(name + ": No cards")
#             return
#         print(name + ": " + ", ".join(str(c) for c in self.cards) + " | " + str(self.value()))

# class Player:
#     def __init__(self, name):
#         self.name = name
#         self.hand = Hand()

#     def turn(self, deck):
#         while True:
#             print()
#             self.hand.show(self.name)

#             if self.hand.value() > 21:
#                 print(self.name + " busted")
#                 return

#             x = input("hit or stand: ").strip().lower()

#             if x == "stand":
#                 print(self.name + " stands")
#                 return

#             elif x == "hit":
#                 c = deck.draw()
#                 print(self.name + " drew " + str(c))

#                 if c.suit == "Hearts":
#                     self.heart(c, deck)
#                 else:
#                     self.hand.add(c)
#             else:
#                 print("type hit or stand")

#     def heart(self, c, deck):
#         print("heart card")
#         print("1 keep  2 discard")

#         while True:
#             x = input("choose: ").strip()

#             if x == "1":
#                 self.hand.add(c)
#                 print("kept " + str(c))
#                 return

#             elif x == "2":
#                 print("discarded " + str(c))
#                 n = deck.draw()
#                 print("new card " + str(n))
#                 self.hand.add(n)
#                 return

#             else:
#                 print("choose 1 or 2")

# class Monster(Player):
#     def __init__(self):
#         super().__init__("Monster")

#     def turn(self, deck, ps):
#         print("\nmonster turn")
#         time.sleep(2)

#         while True:
#             self.hand.show("Monster")
#             s = self.hand.value()

#             if s > 21:
#                 print("monster busted")
#                 return

#             if s >= ps and s >= 17:
#                 print("monster stands")
#                 return

#             print("monster thinking...")
#             time.sleep(2)

#             c = deck.draw()
#             print("monster drew " + str(c))
#             time.sleep(2)

#             if c.suit == "Hearts":
#                 self.heart_ai(c, deck, ps)
#             else:
#                 self.hand.add(c)

#     def heart_ai(self, c, deck, ps):
#         s = self.hand.value()
#         ns = s + c.value

#         print("monster deciding...")
#         time.sleep(2)

#         if ns <= 21:
#             self.hand.add(c)
#             print("monster keeps " + str(c))
#         else:
#             print("monster discards " + str(c))
#             n = deck.draw()
#             print("monster new card " + str(n))
#             self.hand.add(n)

# class Game:
#     def __init__(self):
#         self.deck = Deck()
#         self.p = Player("Player")
#         self.m = Monster()

#     def start(self):
#         print("blackjack heart")

#         self.p.hand.add(self.deck.draw())
#         self.m.hand.add(self.deck.draw())

#         print("\nstart")
#         self.p.hand.show("Player")
#         print("Monster: hidden")

#         print("\nplayer turn")
#         self.p.turn(self.deck)

#         if self.p.hand.value() > 21:
#             print("monster wins")
#             return

#         ps = self.p.hand.value()
#         self.m.turn(self.deck, ps)

#         self.result()

#     def result(self):
#         p = self.p.hand.value()
#         m = self.m.hand.value()

#         print("\nresult")
#         self.p.hand.show("Player")
#         self.m.hand.show("Monster")

#         if p > 21:
#             print("monster wins")
#         elif m > 21:
#             print("player wins")
#         elif p > m:
#             print("player wins")
#         elif m > p:
#             print("monster wins")
#         else:
#             print("tie")

# if __name__ == "__main__":
#     g = Game()
#     g.start()