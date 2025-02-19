# Card values for Blackjack
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11  # Aces can be 1 or 11 (handled separately)
}

# Basic Strategy (Partial Example)
BASIC_STRATEGY = {
    (8, '2'): 'H', (16, '10'): 'S', (11, '6'): 'D'  # Add full strategy table...
}

def hand_value(hand):
    """
    Calculates the best possible hand value in Blackjack.
    Handles Aces as either 1 or 11.
    :param hand: List of card values.
    :return: Best possible hand value.
    """
    value = sum(CARD_VALUES[card] for card in hand)
    num_aces = hand.count('A')
    
    # Convert Aces from 11 to 1 if necessary to avoid busting
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def basic_strategy(player_hand, dealer_upcard):
    """
    Determines the optimal move based on basic Blackjack strategy.
    :param player_hand: List of player's cards.
    :param dealer_upcard: Dealer's visible card.
    :return: Suggested move ('H' = Hit, 'S' = Stand, 'D' = Double Down, etc.).
    """
    player_total = hand_value(player_hand)
    return BASIC_STRATEGY.get((player_total, dealer_upcard), 'H')
