import random
from utils import hand_value
from card_counter import CardCounter

# Card values for Blackjack
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11  # Aces can be 1 or 11 (handled separately)
}

class BlackjackEnvironment:
    """
    Simulates a Blackjack game environment with multiple decks.
    """

    def __init__(self, num_decks=6):
        """
        Initializes the Blackjack environment.
        :param num_decks: Number of decks used in the game.
        """
        self.num_decks = num_decks
        self.deck = self.create_deck()
        self.counter = CardCounter(num_decks)

    def create_deck(self):
        """
        Creates and shuffles a new deck.
        :return: Shuffled deck list.
        """
        deck = [card for card in CARD_VALUES.keys()] * 4 * self.num_decks
        random.shuffle(deck)
        return deck

    def deal_card(self):
        """ Deals a single card from the deck. """
        return self.deck.pop()

    def reset(self):
        """ Resets the deck and card counter. """
        self.deck = self.create_deck()
        self.counter = CardCounter(self.num_decks)

    def play_dealer_hand(self, dealer_upcard):
        """
        Plays the dealer's hand based on Blackjack rules.
        Dealer must hit until reaching at least 17.
        :param dealer_upcard: The dealer's visible card.
        :return: Final dealer hand.
        """
        dealer_hand = [dealer_upcard]
        while hand_value(dealer_hand) < 17:
            new_card = self.deal_card()
            dealer_hand.append(new_card)
            self.counter.update_count(new_card)
        return dealer_hand
