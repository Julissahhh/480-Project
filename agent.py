from utils import hand_value, basic_strategy

class BlackjackAgent:
    """
    Represents an AI player in the Blackjack simulation.
    """

    def __init__(self, environment, bankroll=1000, base_bet=10):
        """
        Initializes the Blackjack agent.
        :param environment: The game environment.
        :param bankroll: Starting bankroll for betting.
        :param base_bet: Minimum bet amount.
        """
        self.env = environment
        self.bankroll = bankroll
        self.base_bet = base_bet

    def place_bet(self):
        """
        Determines bet amount using card counting.
        Higher bets are placed when the count is in the player's favor.
        TODO: We have to figure out how card counting actually works
        :return: Bet amount.
        """
        return self.base_bet * max(1, round(self.env.counter.true_count()))

    def play_hand(self):
        """
        Simulates a player's turn, making decisions based on strategy.
        :return: Player's hand, dealer's upcard, and bet amount.
        """
        # Shuffle deck if it is nearly exhausted
        if len(self.env.deck) < 15:
            self.env.reset()

        bet = self.place_bet()
        player_hand = [self.env.deal_card(), self.env.deal_card()]
        dealer_upcard = self.env.deal_card()

        # Update count for initial cards
        for card in player_hand + [dealer_upcard]:
            self.env.counter.update_count(card)

        # Make decisions based on basic strategy
        while hand_value(player_hand) < 21:
            # TODO: Add other actions based on what move was chosen
            move = basic_strategy(player_hand, dealer_upcard)
            if move == 'H':  # Hit
                new_card = self.env.deal_card()
                player_hand.append(new_card)
                self.env.counter.update_count(new_card)
            else:  # Stand or other action
                break

        return player_hand, dealer_upcard, bet
