import random
from utils import CARD_VALUES, HI_LO_VALUES

class BlackjackEnvironment:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.deck = []
        self.running_count = 0
        self.cards_seen = 0
        self.reset()
    
    def reset(self):
        self.deck = [c for c in CARD_VALUES for _ in range(4)] * self.num_decks
        random.shuffle(self.deck)
        self.running_count = 0
        self.cards_seen = 0
        
    def deal(self, reveal=True):
        card = self.deck.pop()
        self.cards_seen += 1
        if reveal:
            self.update_count(card)
        return card
    
    def update_count(self, card):
        self.running_count += HI_LO_VALUES.get(card, 0)
        
    @property
    def true_count(self):
        remaining = max(len(self.deck) / 52, 0.5)  # Avoid division by zero
        return self.running_count / remaining
    
    def remaining_cards(self):
        return len(self.deck)