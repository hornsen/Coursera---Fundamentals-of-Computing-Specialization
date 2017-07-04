# Mini-project #6 - Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

#import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")   

CARD_BACK_COLOR = "blue" 

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand=[]
        
    def __str__(self):
        # return a string representation of a hand
        card_hand=""
        for card in range(len(self.hand)):
            card_hand+= str(self.hand[card]) + " "
            
        return str("Hand contains %s" % (card_hand) )
        
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
		# count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
		total_hand_value=0
		ace=False
		if(len(self.hand) == 0):
			return 0
		else:
			for i in range(len(self.hand)):
				total_hand_value += VALUES[ self.hand[i][1] ]
			
				if(self.hand[i][1] == "A"):
					ace=True
				
			if(ace==True and total_hand_value <= 11):
				total_hand_value += 10
				
			return total_hand_value

    def draw(self, canvas, pos):
		# draw a hand on the canvas, use the draw method for cards        
		
		for i in range(len(self.hand)):
			show_hand = Card(self.hand[0+i][0], self.hand[0+i][1])
			show_hand.draw(canvas, [pos[0]+100*i, pos[1]])
   
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
		self.deck=[]
		
		for SUIT in SUITS:
			for RANK in RANKS:
				self.deck.append( SUIT + RANK )

    def shuffle(self):
        # shuffle the deck 
        deck=random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
		full_deck_list=""
		for card in range(len(self.deck)):
			full_deck_list += self.deck[card] + " "
		
		return str(full_deck_list)

#define event handlers for buttons
def deal():
	global outcome, in_play, deck, player, dealer
	
	outcome= "Hit or stand?"
	deck = Deck()
	deck.shuffle()
	player=Hand()
	dealer=Hand()
	
	player.add_card( deck.deal_card() )
	player.add_card( deck.deal_card() )
	dealer.add_card( deck.deal_card() )
	dealer.add_card( deck.deal_card() )

	
	print("*** NEW GAME ***")
	print("Player's hand %s and player's hand value %s" % (player, player.get_value() ))
	in_play = True

def hit():
	# if the hand is in play, hit the player and if busted, assign a message to outcome, update in_play and score

	global in_play, outcome, score, winner_text

	if(in_play==True):
		if(player.get_value() <= 21):
			player.add_card( deck.deal_card() )
			print("Player's hand %s and player's hand value %s" % (player, player.get_value() ))
			
			if(player.get_value() <= 21):
				outcome= "Hit or stand?"
			else:
				outcome= "New deal?"
				winner_text='You went bust and lose.'
				print("\n\n")
				
				in_play = False
				score-=1
       
def stand():
	# if hand is in play, repeatedly hit dealer until his hand has value 17 or more
	
	global in_play, outcome, winner_text, score

	if(in_play==True):	
		while(dealer.get_value() <= 17):
			dealer.add_card( deck.deal_card() )

		if(player.get_value() <= dealer.get_value() <= 21):
			winner_text='You went bust and lose.'
			score-=1
		else:
			winner_text='You win!'
			score+=1
		
		print("\nDealer's hand %s and dealer's hand value %s \n\n" % (dealer, dealer.get_value() ))
	
	in_play=False
	outcome= "New deal?"


# draw handler    
def draw(canvas):
	
	# Text
	canvas.draw_text('Blackjack', (90, 80), 50, 'Turquoise')
	canvas.draw_text( str('Score %s' % score), (425, 80), 30, 'Black')
	canvas.draw_text(outcome, (250, 375), 30, 'Black')
	
	if(in_play == False):
		canvas.draw_text(winner_text, (250, 175), 30, 'Black')

	# Dealer hand
	canvas.draw_text('Dealer', (80, 175), 30, 'Black')
	dealer.draw(canvas,[80, 200])
	
	# Player hand
	canvas.draw_text('Player', (80, 375), 30, 'Black')
	player.draw(canvas,[80, 400])

	# Dealer card back
	if(in_play == True):
		if(CARD_BACK_COLOR == "blue"):
			canvas.draw_image(card_back, [ CARD_BACK_CENTER[0], CARD_BACK_CENTER[1] ], CARD_BACK_SIZE, (216, 248), (72, 96))
		else:
			canvas.draw_image(card_back, [ CARD_BACK_CENTER[0]+72, CARD_BACK_CENTER[1] ], CARD_BACK_SIZE, (216, 248), (72, 96))

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
