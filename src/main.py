# Main game file for Kumari vs Malla King (Pygame-based card game)
import os
import sys
import random
import textwrap
import pygame

#Get current file directory to load assets correctly
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
        "We deeply respect the cultural significance of the Kumari "
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

#Button class for UI Interaction(draw+click detection)
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

# Represents a playing card with suit, rank, and value    
class Card:
    def __init__(self,suit,rank,value):
        self.suit=suit
        self.rank=rank
        self.value=value

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def color(self):
        return RED if self.suit in ("Hearts","Diamonds") else BLACK
    
    def suit_symbol(self):
         return{
            "Hearts": "♥",
            "Diamonds": "♦",
            "Clubs": "♣",
            "Spades": "♠",
        }[self.suit]

# Creates and shuffles a deck of cards
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

# Stores cards for a player    
class Hand:
    def __init__(self):
        self.cards=[]

    def add(self,card):
        self.cards.append(card)

    def value(self):
        return sum(card.value for card in self.cards)

# Player class holding name and hand
class Player:
    def __init__(self,name):
        self.name=name
        self.hand=Hand()

class MallaKing(Player):
    def __init__(self):
        super().__init__("Malla King")

# Main game controller handling UI, logic, and flow
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
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

    # Reset game state for a new round
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

    def draw_paragraph(self,text,font,color,rect,line_gap=6):
        words=text.split()
        lines=[]
        current=""

        for word in words:
            test = word if not current else f"{current} {word}"
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
            self.screen.blit(surf,(rect.x,y))
            y+=surf.get_height()+line_gap
        return y
    
    def draw_intro_screen(self):
        self.screen.fill(GREY)
        panel=pygame.Rect(36,24,WIDTH-72,HEIGHT-48)
        pygame.draw.rect(self.screen,WHITE,panel,border_radius=24)
        pygame.draw.rect(self.screen,BLACK,panel,width=4,border_radius=24)
        self.draw_text(TITLE,self.title_font,RED,WIDTH//2,54,center=True)
        left_x=78
        right_margin=WIDTH-78
        content_w=right_margin-left_x
        self.draw_text(DISCLAIMER_TITLE,self.section_font,BLACK,left_x,108)
        y=152
        for paragraph in DISCLAIMER_PARAGRAPHS:
            y=self.draw_paragraph(
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
        self.draw_text("A Short Story Before the Game",self.section_font,RED,90,558)

        story_y=596
        for paragraph in HISTORY_PARAGRAPHS:
            story_y=self.draw_paragraph(
                paragraph,
                self.intro_small_font,
                BLACK,
                pygame.Rect(92,story_y,WIDTH-184,70),
                line_gap=3
            )
            story_y+=8

        self.start_btn.draw(self.screen,pygame.mouse.get_pos())

    def draw_table(self):
        self.screen.fill(GREY)
        outer=pygame.Rect(18,18,WIDTH-36,HEIGHT-36)
        inner=pygame.Rect(28,28,WIDTH-56,HEIGHT-56)
        pygame.draw.rect(self.screen, BLACK, outer, border_radius=22)
        pygame.draw.rect(self.screen, LIGHT_GREY, inner, border_radius=20)
        pygame.draw.rect(self.screen, RED, inner, width=4, border_radius=20)


    def draw_card(self, card, x, y, hidden=False):
        rect = pygame.Rect(x, y, CARD_W, CARD_H)
        pygame.draw.rect(self.screen, WHITE if not hidden else DARK_GREY, rect, border_radius=14)
        pygame.draw.rect(self.screen, BLACK, rect, width=3, border_radius=14)

        if hidden:
            self.draw_text("?",self.title_font,WHITE,x+CARD_W//2,y+CARD_H//2,center=True)
            return
        
        color=card.color()
        symbol=card.suit_symbol()
        self.draw_text(card.rank,self.font,color,x+10,y+8)
        self.draw_text(symbol,self.symbol_font,color,x+CARD_W//2,y+CARD_H//2,center=True)
        self.draw_text(card.rank, self.font, color, x + CARD_W - 28, y + CARD_H - 34)
        self.draw_text(symbol, self.small_font, color, x + CARD_W - 24, y + CARD_H - 56)
    
    def draw_hand(self,hand,x,y,hide_first=False):
        for index,card in enumerate(hand.cards):
            card_x=x+index*CARD_GAP
            self.draw_card(card,card_x,y,hidden=(hide_first and index==0))

    def draw_hand_row(self,label,total_text,hand,x,y,hide_first=False):
        self.draw_text(label,self.section_font,BLACK,x,y)
        self.draw_text(f"Total: {total_text}",self.font,RED,x+2,y+36)
        self.draw_hand(hand,x,y+68,hide_first=hide_first)

    def draw_message_box(self):
        msg_box=pygame.Rect(365,692,850,74)
        pygame.draw.rect(self.screen,WHITE,msg_box,width=2,border_radius=14)
        pygame.draw.rect(self.screen,BLACK,msg_box,width=2,border_radius=14)
        self.draw_paragraph(self.message,self.small_font,BLACK,pygame.Rect(385,710,810,50),line_gap=2)
    
    def draw_heart_panel(self):
        panel=pygame.Rect(865,315,350,255)
        pygame.draw.rect(self.screen,WHITE,panel,width=3,border_radius=16)
        pygame.draw.rect(self.screen,RED,panel,width=3,border_radius=16)
        self.draw_text("Heart Card Choice",self.font,RED,1040,340,center=True)
        self.draw_paragraph(
            "Kumari may keep this blessing or discard it",
            self.small_font,
            BLACK,
            pygame.Rect(888,368,300,45),
            line_gap=2,
        )

        if self.pending_heart:
            self.draw_card(self.pending_heart, 886, 412)
            self.draw_text(str(self.pending_heart), self.small_font, BLACK, 1005, 430)
            self.draw_text("Choose one option below.", self.small_font, BLACK, 1005, 456)


        mouse_pos = pygame.mouse.get_pos()
        self.keep_btn.draw(self.screen, mouse_pos)
        self.discard_btn.draw(self.screen, mouse_pos)

    def draw_result_panel(self):
        panel=pygame.Rect(850,430,365,185)
        pygame.draw.rect(self.screen,WHITE,panel,border_radius=18)
        pygame.draw.rect(self.screen,RED,panel,border_radius=18)
        self.draw_text(self.result_text,self.title_font,RED,1032,480,center=True)
        self.draw_paragraph(
            self.result_subtext,
            self.small_font,
            BLACK,
            pygame.Rect(890,515,285,60),
            line_gap=3,
        )

    def player_total_for_display(self):
        return self.player.hand.value()
    
    def monster_total_for_display(self):
        if self.state in ("player_turn","heart_choice"):
            return "?"
        return str(self.monster.hand.value())
    
    def handle_player_hit(self):
        card=self.deck.draw()

        #it is about the special twist
        if card.suit=="Hearts":
            self.pending_heart=card
            self.state="heart_choice"
            self.message=f"Kumari drew {card}. Keep it, or discard it and trust destiny?"
            return
        
        self.player.hand.add(card)

        if self.player.hand.value()>21:
            self.message=f"Kumari drew {card} and the total went too far."
            self.end_round("malla")
        else:
            self.message=f"Kumari drew {card}. The kingdom still holds. Hit or Stand"

    def handle_player_stand(self):
        self.state="monster_turn"
        self.message="The Malla King now makes his move..."
        self.monster_timer=pygame.time.get_ticks()+900

    def handle_heart_keep(self):
        kept=self.pending_heart
        self.player.hand.add(kept)
        self.pending_heart=None

        if self.player.hand.value()>21:
            self.message=f"Kumari kept {kept}, but the blessing turned heavy"
            self.end_round("malla")
        else:
            self.state="player_turn"
            self.message=f"Kumari kept {kept}. The path is still open. Hit or Stand"



    def handle_heart_discard(self):
        old=self.pending_heart
        self.pending_heart=None
        new_card=self.deck.draw()
        self.player.hand.add(new_card)

        if self.player.hand.value()>21:
            self.message=f"Kumari discarded {old} and received {new_card}. It was too much."
            self.end_round("malla")
        else:
            self.state="player_turn"
            self.message=f"Kumari discarded {old} and received {new_card}. Hit or Stand."

    def run_monster_ai(self):
        now=pygame.time.get_ticks()
        if now<self.monster_timer:
            return
        total=self.monster.hand.value()
        player_score=self.player.hand.value()   

        if total>21:
            self.message="The Malla King overreached and fell"
            self.end_round("kumari")
            return
        
        if total>=17 and total>=player_score:
            self.message="The Malla King stands and waits for judgement."
            self.finish_winner()
            return
        
        card=self.deck.draw()

        if card.suit=="Hearts":
            next_total=total+card.value
            if next_total <= 21:
                self.monster.hand.add(card)
                self.message = f"The Malla King drew {card} and kept it."
            else:
                replacement = self.deck.draw()
                self.monster.hand.add(replacement)
                self.message = f"The Malla King rejected a Heart and drew {replacement} instead."
        else:
            self.monster.hand.add(card)
            self.message = f"The Malla King drew {card}."


        if self.monster.hand.value() > 21:
            self.message = "The Malla King's pride pushed him too far."
            self.end_round("kumari")
        else:
            self.monster_timer = now + 1100

    def finish_winner(self):
        p_total = self.player.hand.value()
        m_total = self.monster.hand.value()


        if p_total > 21:
            self.end_round("malla")
        elif m_total > 21:
            self.end_round("kumari")
        elif p_total > m_total:
            self.end_round("kumari")
        elif m_total > p_total:
            self.end_round("malla")
        else:
            self.end_round("tie")


    def end_round(self, winner):
        self.state = "round_over"


        if winner == "kumari":
            self.result_text = "Kumari won"
            self.result_subtext = "Peaceful Kumari Kingdom has been Established"
        elif winner == "malla":
            self.result_text = "Kumari Lost"
            self.result_subtext = "She will reborn as Tuleju Bhawani."
        else:
            self.result_text = "Sacred Draw"
            self.result_subtext = "Neither side claimed the valley today."
    def draw_ui(self):
        self.draw_table()
        self.draw_text(TITLE, self.title_font, RED, 56, 46)
        self.draw_text(
            "A respectful fictional card duel inspired by Newar culture",
            self.tiny_font,
            BLACK,
            58,
            84,
        )


        self.draw_hand_row(
            "Malla King",
            self.monster_total_for_display(),
            self.monster.hand,
            60,
            132,
            hide_first=(self.state in ("player_turn", "heart_choice")),
        )
        self.draw_hand_row("Kumari", self.player_total_for_display(), self.player.hand, 60, 430)


        self.draw_message_box()


        mouse_pos = pygame.mouse.get_pos()
        if self.state == "player_turn":
            self.hit_btn.draw(self.screen, mouse_pos)
            self.stand_btn.draw(self.screen, mouse_pos)
        elif self.state == "heart_choice":
            self.draw_heart_panel()
        elif self.state == "round_over":
            self.restart_btn.draw(self.screen, mouse_pos)
            self.draw_result_panel()


        help_text = "Heart twist: if Kumari draws a Heart, you may Keep or Discard it. Ace is always 1."
        self.draw_text(help_text, self.tiny_font, BLACK, 56, HEIGHT - 26)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False


            elif self.show_intro:
                if self.start_btn.clicked(event):
                    self.show_intro = False


            elif self.state == "player_turn":
                if self.hit_btn.clicked(event):
                    self.handle_player_hit()
                elif self.stand_btn.clicked(event):
                    self.handle_player_stand()


            elif self.state == "heart_choice":
                if self.keep_btn.clicked(event):
                    self.handle_heart_keep()
                elif self.discard_btn.clicked(event):
                    self.handle_heart_discard()


            elif self.state == "round_over":
                if self.restart_btn.clicked(event):
                    self.reset_round()


    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()


            if not self.show_intro and self.state == "monster_turn":
                self.run_monster_ai()


            if self.show_intro:
                self.draw_intro_screen()
            else:
                self.draw_ui()


            pygame.display.flip()


        pygame.quit()
        sys.exit()

                

if __name__=="__main__":
    Game().run()

