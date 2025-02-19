import random

# Card values for Blackjack
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11  # Aces can be 1 or 11 (handled separately)
}

# Hi-Lo Card Counting System
HI_LO_VALUES = {
    '2': +1, '3': +1, '4': +1, '5': +1, '6': +1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Basic Strategy (Partial Example)
BASIC_STRATEGY = {
    (8, '2'): 'H', (16, '10'): 'S', (11, '6'): 'D'  # Add full strategy table...
}

# Create a deck and shuffle
def create_deck(num_decks=1):
    deck = [card for card in CARD_VALUES.keys()] * 4 * num_decks
    random.shuffle(deck)
    return deck

# Deal a card
def deal_card(deck):
    return deck.pop()

# Calculate hand value
def hand_value(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    num_aces = hand.count('A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

# Get AI decision based on Basic Strategy
def basic_strategy(player_hand, dealer_upcard):
    player_value = hand_value(player_hand)
    return BASIC_STRATEGY.get((player_value, dealer_upcard), 'H')

# Card Counter class
class CardCounter:
    def __init__(self, num_decks):
        self.running_count = 0
        self.num_decks = num_decks
        self.cards_seen = 0

    def update_count(self, card):
        self.running_count += HI_LO_VALUES.get(card, 0)
        self.cards_seen += 1

    def true_count(self):
        remaining_decks = max(self.num_decks - self.cards_seen / 52, 1)
        return self.running_count / remaining_decks

# AI playing logic
def play_blackjack():
    deck = create_deck(num_decks=6)
    counter = CardCounter(num_decks=6)
    bankroll = 1000
    base_bet = 10

    for _ in range(100):  # Play 100 hands
        if len(deck) < 15:
            deck = create_deck(num_decks=6)
            counter = CardCounter(num_decks=6)

        bet = base_bet * max(1, round(counter.true_count()))
        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_upcard = deal_card(deck)
        
        for card in player_hand + [dealer_upcard]:
            counter.update_count(card)

        while hand_value(player_hand) < 21:
            move = basic_strategy(player_hand, dealer_upcard)
            if move == 'H':
                new_card = deal_card(deck)
                player_hand.append(new_card)
                counter.update_count(new_card)
            else:
                break

        dealer_hand = [dealer_upcard]
        while hand_value(dealer_hand) < 17:
            new_card = deal_card(deck)
            dealer_hand.append(new_card)
            counter.update_count(new_card)

        player_score = hand_value(player_hand)
        dealer_score = hand_value(dealer_hand)

        if player_score > 21 or (dealer_score <= 21 and dealer_score > player_score):
            bankroll -= bet
        elif dealer_score > 21 or player_score > dealer_score:
            bankroll += bet

        print(f"Bankroll: {bankroll}, True Count: {counter.true_count():.2f}")

if __name__ == "__main__":
    play_blackjack()
