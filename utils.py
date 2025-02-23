CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

BASIC_STRATEGY = {
    # Expanded basic strategy table
    (8, '2'): 'H', (16, '10'): 'S', (11, '6'): 'D',
    # ... rest of strategy implementation
}

def hand_value(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    aces = hand.count('A')
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value

def basic_strategy(player_hand, dealer_card):
    total = hand_value(player_hand)
    return BASIC_STRATEGY.get((total, dealer_card), 'H')