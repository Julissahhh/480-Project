import random
from utils import hand_value
from card_counter import CardCounter

# Card values for Blackjack
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11  # Aces can be 1 or 11 (handled separately)
}

class BlackjackEnvironment:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.deck = self.create_deck()
        self.counter = CardCounter(num_decks)
    
    def create_deck(self):
        deck = [card for card in CARD_VALUES.keys()] * 4 * self.num_decks
        random.shuffle(deck)
        return deck
    
    def deal_card(self):
        return self.deck.pop()
    
    def reset(self):
        self.deck = self.create_deck()
        self.counter = CardCounter(self.num_decks)
    
    def play_dealer_hand(self, dealer_upcard):
        dealer_hand = [dealer_upcard]
        while hand_value(dealer_hand) < 17:
            new_card = self.deal_card()
            dealer_hand.append(new_card)
            self.counter.update_count(new_card)
        return dealer_hand
