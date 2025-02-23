from utils import hand_value, basic_strategy

class BlackjackAgent:
    def __init__(self, bankroll=1000, base_bet=100):
        self.bankroll = bankroll
        self.base_bet = base_bet
        self.hand = []
        
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