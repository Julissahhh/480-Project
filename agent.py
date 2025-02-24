from utils import hand_value, basic_strategy
from abc import ABC, abstractmethod
import time

class Agent(ABC):
    def __init__(self, bankroll=1000, base_bet=100):
        self.bankroll = bankroll
        self.base_bet = base_bet
        self.hand = []
        self.current_bet = 0
    
    @abstractmethod
    def place_bet(self, true_count):
        pass

    @abstractmethod
    def play_turn(self, dealer_upcard, env):
        pass

class BlackjackAgent(Agent):        
    def place_bet(self, true_count):
        bet = self.base_bet * max(1, round(true_count))
        self.bankroll -= bet
        return bet
        
    def play_turn(self, dealer_upcard, env):
        actions = []
        while hand_value(self.hand) < 21:
            action = basic_strategy(self.hand, dealer_upcard)
            actions.append(action)
            if action == 'H':
                self.hand.append(env.deal())
            else:
                break
        return actions

class HumanAgent(Agent):
    def place_bet(self, true_count):
        print(f"True Count: {true_count}")
        while True:
            try:
                print(f"\nCurrent bankroll: ${self.bankroll}")
                bet = int(input("Enter your bet: "))
                if 0 < bet <=self.bankroll:
                    self.bankroll -= bet
                    self.current_bet = bet
                    return bet
                print(f"Invalid bet! Must be between 1 and {self.bankroll}")
            except ValueError:
                print("Please enter a valid number")
    def play_turn(self, dealer_upcard, env):
        actions = []
        while hand_value(self.hand) < 21:
            print(f"\nYour hand: {self.hand} ({hand_value(self.hand)})")
            print(f"Dealer's upcard: {dealer_upcard}")
            action = input("Action (H=Hit, S=Stand, D=Double...): ").upper()

            if action not in ['H', 'S']:
                print("Action not implemented")
                continue
                
            actions.append(action)

            if action == 'H':
                self.hand.append(env.deal())
            elif action == 'D':
                if len(self.hand) == 2 and self.bankroll >= self.current_bet:
                    self.bankroll -= self.current_bet
                    self.current_bet *= 2
                    self.hand.append(env.deal())
                    break
                else:
                    print("Can only doubl on initial two cards with sufficient funds")
                    actions.pop()
            else: # Stand
                break
        time.sleep(1)
        return actions