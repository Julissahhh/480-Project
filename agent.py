from utils import hand_value, basic_strategy

class BlackjackAgent:
    def __init__(self, environment, bankroll=1000, base_bet=10):
        self.env = environment
        self.bankroll = bankroll
        self.base_bet = base_bet

    def place_bet(self):
        return self.base_bet * max(1, round(self.env.counter.true_count()))

    def play_hand(self):
        if len(self.env.deck) < 15:
            self.env.reset()

        bet = self.place_bet()
        player_hand = [self.env.deal_card(), self.env.deal_card()]
        dealer_upcard = self.env.deal_card()

        for card in player_hand + [dealer_upcard]:
            self.env.counter.update_count(card)

        while hand_value(player_hand) < 21:
            move = basic_strategy(player_hand, dealer_upcard)
            if move == 'H':
                new_card = self.env.deal_card()
                player_hand.append(new_card)
                self.env.counter.update_count(new_card)
            else:
                break

        return player_hand, dealer_upcard, bet
