from cards import Deck, Player
from engine import GameEngine

communityCards = False
dealerPlay = False
cardsPerHand = 0
#----------------------------------------#   #---game-setting-input---#
availableVarients = [ "Texas Holdem" , "Blackjack" , "Draw" , "Stud" ]
print("------------------------------------------")
print("    Select poker varient")
print("    --------------------")
for index, varient in enumerate(availableVarients, start=1):
    print(f"{index}-{varient}")
print()
varient = input("enter number: ")
if varient not in range(1,len(availableVarients)+1):
    raise ValueError("Invalid game selection")
selectedVarient = availableVarients[varient-1]
print("------------------------------------------")
numPlayers = int(input("    Input number of players"))
if numPlayers <1:
    raise ValueError("You need at least one player")

if variant == 1: #Texas Holdem
    cardsPerHand = 2
    communityCards = True
elif variant == 2: #Blackjack
    cardsPerHand = 2
    dealerPlay = True
elif variant == 3: #Draw
    cardsPerHand = int(input("Cards per hand: "))
elif variant ==4: #Stud
    cardsPerHand = int(input("Cards per hand: "))

players = []

for index in range(numPlayers):
    name = input(f"Enter name for player {index+1}: ")
    players.append(Player(name))

if dealerPlay:
    players.append(Player("Dealer"))
#----------------------------------------#   #---start---#
def startGame(): #init hands for all players
    Deck.newDeck()
    Deck.shuffle()
    for player in players:
        player.clearHand()

    for _ in range(cardsPerHand):
        for player in players:
            card = Deck.deal()
            player.deltCard(card)

    print("\n----------- DEALT HANDS ------------")

    for player in players:
        print(f"\n{player.name}: {player.hand}")
    print("\nCards remaining: ", len(Deck.deck))

game = GameEngine(
    players=players,
    cards_per_hand=cardsPerHand,
    community_cards=communityCards,
    dealer_play=dealerPlay
)

game.initialize_game()
game.deal_hands()

if selectedVarient == "Texas Holdem":

    game.deal_flop()
    game.deal_turn()
    game.deal_river()

game.show_game_state()
