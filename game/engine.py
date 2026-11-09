from itertools import combinations
from cards import Deck, Player

#/*-----------HAND EVALUATION-----------*/#
RANKS = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12,"K": 13, "A": 14}
HAND_NAMES = ["High Card","One Pair","Two Pair","Three of a Kind","Straight","Flush","Full House","Four of a Kind","Straight Flush"]

def card_rank(card):
    return RANKS[card[:-1]]

def evaluate_five(cards):
    ranks = sorted([card_rank(card) for card in cards], reverse=True)
    counts = {}
    for rank in ranks:
        counts[rank] = counts.get(rank, 0) + 1
    groups = sorted([(count, rank) for rank, count in counts.items()],reverse=True)
    flush = len(set(card[-1] for card in cards)) == 1
    unique = sorted(set(ranks), reverse=True)
    straight_high = 0
    if len(unique) == 5:
        if unique[0] - unique[-1] == 4:
            straight_high = unique[0]
        elif unique == [14, 5, 4, 3, 2]:
            straight_high = 5
    if flush and straight_high:
        return (8, straight_high)
    if groups[0][0] == 4:
        return (7, groups[0][1], groups[1][1])
    if groups[0][0] == 3 and groups[1][0] == 2:
        return (6, groups[0][1], groups[1][1])
    if flush:
        return (5, *ranks)
    if straight_high:
        return (4, straight_high)
    if groups[0][0] == 3:
        kickers = sorted([r for r in ranks if r != groups[0][1]],reverse=True)
        return (3, groups[0][1], *kickers)
    if groups[0][0] == 2 and groups[1][0] == 2:
        pairs = sorted([g[1] for g in groups if g[0] == 2],reverse=True)
        kicker = max(r for r in ranks if r not in pairs)
        return (2, *pairs, kicker)
    if groups[0][0] == 2:
        pair = groups[0][1]
        kickers = sorted([r for r in ranks if r != pair], reverse=True)
        return (1, pair, *kickers)
    return (0, *ranks)

def evaluate_hand(cards):
    if len(cards) < 5:
        raise ValueError("At least five cards are required.")
    return max(evaluate_five(combo) for combo in combinations(cards, 5))

#/*------------------GAME ENGINE-------------------*/#

class GameEngine:
    def __init__(self, players, game_type="Texas Holdem"):
        self.players = players
        self.game_type = game_type
        self.community_cards = []
        self.pot = 0
        self.game_active = False
        self.status = {}
        self.round_bets = {}
        self.total_contributions = {}
    #/*--------INITIALIZATION----------*/#
    def initialize_game(self):
        Deck.newDeck()
        Deck.shuffle()
        self.community_cards = []
        self.pot = 0
        for player in self.players:
            player.clearHand()
            self.status[player] = "active"
            self.round_bets[player] = 0
            self.total_contributions[player] = 0
        self.game_active = True
    #/*-----------DEALING--------------*/#
    def deal_hands(self, amount):
        for _ in range(amount):
            for player in self.players:
                if self.status[player] == "active":
                    player.deltCard(Deck.deal())

    def burn_card(self):
        Deck.deal()

    def deal_flop(self):
        self.burn_card()

        for _ in range(3):
            self.community_cards.append(Deck.deal())

        self.show_community()

    def deal_turn(self):
        self.burn_card()
        self.community_cards.append(Deck.deal())
        self.show_community()

    def deal_river(self):
        self.burn_card()
        self.community_cards.append(Deck.deal())
        self.show_community()

    def show_community(self):
        print("\nCommunity Cards:", self.community_cards)
    #/*-----------PLAYER STATUS------------*/#
    def active_players(self):
        return [p for p in self.players if self.status[p] in ("active", "all-in")]

    def fold(self, player):
        self.status[player] = "folded"
    #/*--------------BETTING---------------*/#
    def contribute(self, player, amount):
        if amount <= 0 or amount > player.chips:
            raise ValueError("Invalid bet amount.")
        player.chips -= amount
        player.current_bet += amount
        self.round_bets[player] += amount
        self.total_contributions[player] += amount
        self.pot += amount
        if player.chips == 0:
            self.status[player] = "all-in"

    def reset_bets(self):
        for player in self.players:
            self.round_bets[player] = 0
            player.current_bet = 0

    def betting_round(self):
        current_bet = max(self.round_bets.values(), default=0)
        pending = [
            p for p in self.players
            if self.status[p] == "active"]
        while pending:
            player = pending.pop(0)
            if self.status[player] != "active":
                continue
            if len(self.active_players()) <= 1:
                break
            to_call = current_bet - self.round_bets[player]
            print(f"\n{player.name}'s turn")
            print("Chips:", player.chips)
            print("Pot:", self.pot)
            print("To call:", to_call)
            action = input(
                "fold / check / call / raise / all-in: ").lower().strip()
            if action == "fold":
                self.fold(player)
            elif action == "check":
                if to_call != 0:
                    print("Cannot check. You must call or fold.")
                    pending.append(player)
            elif action == "call":
                amount = min(to_call, player.chips)
                if amount:
                    self.contribute(player, amount)
            elif action == "all-in":
                amount = player.chips
                if amount:
                    self.contribute(player, amount)
                    if self.round_bets[player] > current_bet:
                        current_bet = self.round_bets[player]
                        pending = [p for p in self.players if self.status[p] == "active" and p != player]
            elif action == "raise":
                try:
                    amount = int(input(
                        "Additional chips to contribute: "))
                    if amount <= to_call or amount > player.chips:
                        raise ValueError
                    self.contribute(player, amount)
                    if self.round_bets[player] > current_bet:
                        current_bet = self.round_bets[player]
                        pending = [p for p in self.players if self.status[p] == "active" and p != player]
                except ValueError:
                    print("Invalid raise.")
                    pending.append(player)
            else:
                print("Invalid action.")
                pending.append(player)
        self.reset_bets()
    #/*-----------------UNCONTESTED POT------------------*/#
    def award_uncontested(self):
        winners = [
            p for p in self.players
            if self.status[p] != "folded"]
        if len(winners) == 1:
            winner = winners[0]
            winner.chips += self.pot
            print(f"\n{winner.name} wins {self.pot} chips!")
            self.pot = 0
            self.game_active = False
            return True
        return False
    #/*---------------SHOWDOWN------------*/#
    def showdown(self, use_community=False):
        rankings = {}
        print("\n========== SHOWDOWN ==========")
        for player in self.players:
            if self.status[player] == "folded":
                continue
            cards = player.hand.copy()
            if use_community:
                cards += self.community_cards
            ranking = evaluate_hand(cards)
            rankings[player] = ranking
            print(
                f"{player.name}: "
                f"{HAND_NAMES[ranking[0]]}")
        if not rankings:
            return
        best = max(rankings.values())
        winners = [
            player for player, ranking in rankings.items()
            if ranking == best]
        share, remainder = divmod(
            self.pot, len(winners))
        for player in winners:
            player.chips += share
        for player in winners[:remainder]:
            player.chips += 1
        print("\nWinner(s):")
        for player in winners:
            print(player.name)
        self.pot = 0
        self.game_active = False
    #/*---------TEXAS HOLD'EM-------------*/#
    def play_holdem(self):
        if len(self.players) < 2:
            raise ValueError("Hold'em requires two players.")
        self.initialize_game()
        self.deal_hands(2)
        print("\n--- PRE-FLOP ---")
        self.betting_round()
        if self.award_uncontested():
            return
        print("\n--- FLOP ---")
        self.deal_flop()
        self.betting_round()
        if self.award_uncontested():
            return
        print("\n--- TURN ---")
        self.deal_turn()
        self.betting_round()
        if self.award_uncontested():
            return
        print("\n--- RIVER ---")
        self.deal_river()
        self.betting_round()
        if self.award_uncontested():
            return
        self.showdown(use_community=True)
    #/*----------FIVE-CARD DRAW------------*/#
    def play_draw(self):
        self.initialize_game()
        self.deal_hands(5)
        print("\n--- FIRST BETTING ROUND ---")
        self.betting_round()
        if self.award_uncontested():
            return
        for player in self.players:
            if self.status[player] != "active":
                continue
            print(f"\n{player.name}: {player.hand}")
            choice = input(
                "Discard positions 1-5, separated by commas: ")
            if not choice.strip():
                continue
            try:
                positions = sorted(set(
                    int(x.strip()) - 1
                    for x in choice.split(",")))
                if any(x < 0 or x >= 5 for x in positions):
                    raise ValueError
                for index in reversed(positions):
                    player.hand.pop(index)
                for _ in positions:
                    player.deltCard(Deck.deal())
            except ValueError:
                print("Invalid selection. No cards discarded.")
        print("\n--- FINAL BETTING ROUND ---")
        self.betting_round()
        if not self.award_uncontested():
            self.showdown()
    #/*-------------------FIVE-CARD STUD--------------------------*/#
    def play_stud(self):
        if len(self.players) < 2:
            raise ValueError("Stud requires two players.")
        self.initialize_game()
        for player in self.players:
            player.deltCard(Deck.deal())
        for round_number in range(4):
            print(f"\n--- STUD ROUND {round_number + 1} ---")
            for player in self.players:
                if self.status[player] == "active":
                    player.deltCard(Deck.deal())
            for player in self.players:
                if self.status[player] == "active":
                    print(
                        f"{player.name}: "
                        f"[Hidden] {player.hand[1:]}")
            self.betting_round()
            if self.award_uncontested():
                return
        self.showdown()
    #/*-----------------------BLACKJACK---------------------------*/#
    @staticmethod
    def blackjack_value(hand):
        total = 0
        aces = 0
        for card in hand:
            rank = card[:-1]
            if rank in ("J", "Q", "K"):
                total += 10
            elif rank == "A":
                total += 11
                aces += 1
            else:
                total += int(rank)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total
    def play_blackjack(self):
        self.initialize_game()
        dealer = Player("Dealer")
        self.players.append(dealer)
        self.status[dealer] = "active"
        self.round_bets[dealer] = 0
        self.total_contributions[dealer] = 0
        wagers = {}
        for player in self.players[:-1]:
            while True:
                try:
                    wager = int(input(
                        f"{player.name}, wager: "
                    ))
                    if 0 < wager <= player.chips:
                        break
                except ValueError:
                    pass
                print("Invalid wager.")
            player.chips -= wager
            wagers[player] = wager
            player.deltCard(Deck.deal())
            player.deltCard(Deck.deal())
        dealer.deltCard(Deck.deal())
        dealer.deltCard(Deck.deal())
        print("\nDealer shows:", dealer.hand[0])
        for player in self.players[:-1]:
            print(f"\n{player.name}: {player.hand}")
            while self.blackjack_value(player.hand) < 21:
                action = input("Hit or stand? ").lower()
                if action == "hit":
                    player.deltCard(Deck.deal())
                    print(player.hand)
                elif action == "stand":
                    break
                else:
                    print("Invalid action.")
            if self.blackjack_value(player.hand) > 21:
                print("Bust!")
        print("\nDealer hand:", dealer.hand)
        while self.blackjack_value(dealer.hand) < 17:
            dealer.deltCard(Deck.deal())
        dealer_total = self.blackjack_value(dealer.hand)
        for player, wager in wagers.items():
            player_total = self.blackjack_value(player.hand)
            if player_total > 21:
                print(player.name, "loses.")
            elif dealer_total > 21 or player_total > dealer_total:
                player.chips += wager * 2
                print(player.name, "wins!")
            elif player_total == dealer_total:
                player.chips += wager
                print(player.name, "pushes.")
            else:
                print(player.name, "loses.")
        self.players.remove(dealer)
        self.game_active = False
    #/*-------------------GAME DISPATCHER---------------*/#
    def play(self):
        if self.game_type == "Texas Holdem":
            self.play_holdem()
        elif self.game_type == "Blackjack":
            self.play_blackjack()
        elif self.game_type == "Draw":
            self.play_draw()
        elif self.game_type == "Stud":
            self.play_stud()
        else:
            raise ValueError("Unknown game type.")
    #/*---------------------GAME STATE-------------------*/#
    def show_game_state(self):
        print("\n========== GAME STATE ==========")
        print("Game:", self.game_type)
        print("Pot:", self.pot)
        print("Community:", self.community_cards)
        for player in self.players:
            print("\nPlayer:", player.name)
            print("Hand:", player.hand)
            print("Chips:", player.chips)
            print("Status:", self.status[player])
        print("================================")
