import string
import random
import math

class Card:
    VALUES = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    SUITS = ("H", "D", "C", "S")

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        if self.rank == 11:
            rank = "J"
        elif self.rank == 12:
            rank = "Q"
        elif self.rank == 13:
            rank = "K"
        elif self.rank == 14:
            rank = "A"
        else:
            rank = self.rank
        return str(rank) + self.suit
    
    def __eq__(self, other):
        return self.rank == other.rank
    
    def __ne__(self, other):
        return self.rank != other.rank
    
    def __lt__(self, other):
        return self.rank < other.rank
    
    def __le__(self, other):
        return self.rank <= other.rank
    
    def __gt__(self, other):
        return self.rank > other.rank
    
    def __ge__(self, other):
        return self.rank >= other.rank
    
class Deck:
    def __init__(cls):
        cls.deck = []
        for suit in Card.SUITS:
            for value in Card.VALUES:
                card = Card(value, suit)
                cls.deck.append(card)
    
    def shuffle(cls):
        random.shuffle(cls.deck)
    
    def __len__(cls):
        return len(cls.deck)

    def deal (cls):
        return cls.deck.pop(len(cls.deck) - 1)

class FiveCardDraw:
    def __init__(self, deck):
        self.cards = []
        for i in range(5):
            self.cards.append(deck.deal())
    
    def __str__(self):
        return ", ".join([str(card) for card in self.cards])
    
    def discard(self, deck):
        if self.cards.value == "A":
            max_discard = 4
        else: 
            max_discard = 3
        discard_input = eval (input("Select the cards you would like to discard: "))
        discard_indices = [int(i) for i in discard_input.split()]
        if len(discard_indices) > max_discard:
            for i in discard_indices:
                self.cards[i] = deck.deal()
            while len(self.cards) < 5:
                self.cards.append(deck.deal())

    def has_pair(self):
        for i in range(5):
            for j in range(i+1, 5):
                if self.cards[i].value == self.cards[j].value:
                    return True
        return False
    
    def has_two_pair(self):
        pairs = 0
        for i in range(5):
            for j in range(i+1, 5):
                if self.cards[i].value == self.cards[j].value:
                    pairs += 1
        if pairs == 2:
            return True
        return False
    
    def has_three_of_a_kind(self):
        for i in range(5):
            for j in range(i+1, 5):
                for k in range(j+1, 5):
                    if self.cards[i].value == self.cards[j].value == self.cards[k].value:
                        return True
        return False
    
    def has_straight(self):
        self.cards.sort()
        for i in range(1, 5):
            if self.cards[i-1].value + 1 != self.cards[i].value:
                return False
        return True
    
    def has_flush(self):
        for i in range(1, 5):
            if self.cards[i].suit != self.cards[0].suit:
                return False
        return True
    
    def has_full_house(self):
        return self.has_pair() and self.has_three_of_a_kind()
    
    def has_four_of_a_kind(self):
        for i in range(5):
            for j in range(i+1, 5):
                for k in range(j+1, 5):
                    for l in range(k+1, 5):
                        if self.cards[i].value == self.cards[j].value == self.cards[k].value == self.cards[l].value:
                            return True
        return False
    
    def has_straight_flush(self):
        return self.has_straight() and self.has_flush()
    
    def has_royal_flush(self):
        return self.has_straight_flush() and self.cards[0].value == 10
    
    def classify(self):
        if self.has_royal_flush():
            return "Royal Flush"
        elif self.has_straight_flush():
            return "Straight Flush"
        elif self.has_four_of_a_kind():
            return "Four of a Kind"
        elif self.has_full_house():
            return "Full House"
        elif self.has_flush():
            return "Flush"
        elif self.has_straight():
            return "Straight"
        elif self.has_three_of_a_kind():
            return "Three of a Kind"
        elif self.has_two_pair():
            return "Two Pair"
        elif self.has_pair():
            return "Pair"
        else:
            return "High Card"

class TexasHoldEm:
    def __init__(self, deck):
        self.cards = []
        for i in range(2):
            self.cards.append(deck.deal())
    
    def __str__(self):
        return ", ".join([str(card) for card in self.cards])  
    
    table = []
    def  __str__(table):
        return ", ".join([str(card) for card in table])

    def flop (deck, table):
        deck.pop(len(deck) - 1),
        for i in range(3):
            table.append(deck.deal())

    def turn (deck, table):
        deck.pop(len(deck) - 1),
        table.append(deck.deal())

    def river (deck, table):
        deck.pop(len(deck) - 1),
        table.append(deck.deal())
        


def main(self):
    deck = Deck()
    deck.shuffle()
    hand = self.cards
    print(hand)
    return(hand.classify())
