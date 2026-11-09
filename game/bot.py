import random
from engine import evaluate_hand, RANKS

class PokerBot:
    def __init__(self, name="Poker Bot", chips=1000,aggression=0.5):

        self.name = name
        self.chips = chips
        self.hand = []
        self.current_bet = 0

        # 0.0 = passive
        # 0.5 = balanced
        # 1.0 = aggressive

        self.aggression = max(0, min(1, aggression))
        self.last_action = None

    def clearHand(self):
        self.hand = []
        self.current_bet = 0

    def deltCard(self, card):
        self.hand.append(card)
    #/*--------------HAND STRENGTH--------------*/#
    def get_hand_strength(self, community_cards):
        cards = self.hand + community_cards
        if len(cards) < 5:
            return 0
        ranking = evaluate_hand(cards)
        return ranking[0] / 8
    #/*----------STARTING HAND STRENGTH---------*/#
    def starting_strength(self):
        if len(self.hand) < 2:
            return 0
        first = RANKS[self.hand[0][:-1]]
        second = RANKS[self.hand[1][:-1]]
        suited = self.hand[0][-1] == self.hand[1][-1]
        paired = first == second
        high = max(first, second)
        low = min(first, second)
        score = (high + low) / 28
        if paired:
            score += 0.35
        if suited:
            score += 0.08
        if high - low <= 2:
            score += 0.08
        return min(score, 1.0)
    #/*------------DECISION ENGINE----------*/#
    def make_decision(self, community_cards,
                      pot, current_bet):
        if len(community_cards) >= 3:
            strength = self.get_hand_strength(community_cards)
        else:
            strength = self.starting_strength()

        strength += random.uniform(-0.05, 0.05)
        strength = max(0, min(1, strength))
        call_amount = max(0, current_bet - self.current_bet)
        if call_amount > self.chips:
            call_amount = self.chips
        pot_odds = (call_amount / (pot + call_amount) if pot + call_amount > 0 else 0)
        #/*---------NO BET TO CALL-----------*/#
        if call_amount == 0:
            if strength > 0.75:
                return "raise"
            if strength > 0.35:
                return "check"
            if self.aggression > 0.7:
                return "raise"
            return "check"
        #/*----------FOLD DECISION------------*/#
        if strength < 0.20 and pot_odds > 0.15:
            return "fold"
        #/*---------CALL DECISION---------------*/#
        if strength > pot_odds + 0.15:
            if strength > 0.75 and self.aggression > 0.4:
                return "raise"
            return "call"
        #/*---------AGGRESSIVE PLAY-----------*/#
        if strength > 0.65 and self.aggression > 0.6:
            return "raise"
        #/*---------FINAL DECISION-------------*/#
        if strength > 0.35:
            return "call"
        return "fold"
    #/*--------------BET SIZING--------------*/#
    def calculate_bet(self, pot, current_bet):
        strength = self.starting_strength()
        bet_size = int(pot * (0.25 + strength * self.aggression))
        bet_size = max(1, bet_size)
        return min(bet_size, self.chips)
    #/*------------EXECUTE ACTION-------------*/#
    def play_turn(self, community_cards, pot, current_bet):
        action = self.make_decision(community_cards, pot, current_bet)
        call_amount = max(0, current_bet - self.current_bet)
        print(f"\n{self.name} is thinking...")
        if action == "fold":
            print(f"{self.name} folds.")
            self.last_action = "fold"
            return ("fold", 0)
        elif action == "check":
            print(f"{self.name} checks.")
            self.last_action = "check"
            return ("check", 0)
        elif action == "call":
            amount = min(call_amount, self.chips)
            print(f"{self.name} calls {amount}.")
            self.last_action = "call"
            return ("call", amount)
        elif action == "raise":
            amount = self.calculate_bet(pot, current_bet)
            amount = min(self.chips, call_amount + amount)
            print(f"{self.name} raises {amount}.")
            self.last_action = "raise"
            return ("raise", amount)
        return ("check", 0)
