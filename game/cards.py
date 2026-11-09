import random

class Deck:
    values = [ '2' , '3', '4' , '5' , '6' , '7' , '8' , '9' , '10' , 'J' , 'Q' , 'K' , 'A' ]
    suits = [ 'C' , 'D' , 'H' , 'S' ]
    deck = []

    @staticmethod
    def newDeck(): #create a new clean ordered deck, 2C-AS
        Deck.deck = []
        for suit in Deck.suits:
            for value in Deck.values:
                Deck.deck.append(value+suit)

    @staticmethod
    def shuffle(): #randomly move cards to temp deck, then make temp deck the game deck
        random.shuffle(Deck.deck)

    @staticmethod
    def deal(): #return top card
        if not Deck.deck:
            raise ValueError("ERROR: No cards in deck")
        return Deck.deck.pop(0)

class Player:
    def __init__(self, name: str, chips=1000):
        self.name = name
        self.hand = []
        self.chips = chips
        self.current_bet = 0

    def bet(self, amount):
        if amount <= 0:
            raise ValueError("Bet must be greater than zero")
        if amount > self.chips:
            raise ValueError("Not enough chips")
        self.chips -= amount
        self.current_bet += amount

    def deltCard(self, newCard: str):
        self.hand.append(newCard)

    def clearHand(self):
        self.hand = []
        self.current_bet = 0
