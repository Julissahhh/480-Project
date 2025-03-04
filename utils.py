from typing import List
from environment import Card

# We wil probably need multiple 2D tables later
# using a simplified strategy function for now
BASIC_STRATEGY = {
    (8, '2'): 'hit',
    (16, '10'): 'stand',
    (11, '6'): 'double',
    # ... rest of strategy implementation
}

def hand_value(hand: List[Card]) -> int:
    total: int = 0
    aces: int = 0
    for c in hand:
        if c.is_ace():
            aces += 1
        total += c.value() # 11 for ace by default
    while total > 21 and aces > 0:
        # calculating soft total if hard total is > 21
        total -= 10
        aces -= 1
    return total

def basic_strategy(player_hand: List[Card], dealer_card: Card) -> str:
    # refactor this later to use proper strategy
    # this is very simple and not optimal
    total: int = hand_value(player_hand)
    dealer_val: int = dealer_card.value()

    # Check for pairs and allow splitting Aces or 8s.
    if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
        if player_hand[0].get_face() in ['A', '8']:
            return "split"

    # For totals 17 or more, stand.
    if total >= 17:
        return "stand"
    # For totals between 13 and 16, stand if dealer shows a weak card (2–6), otherwise hit.
    if 13 <= total <= 16:
        return "stand" if 2 <= dealer_val <= 6 else "hit"
    # For a total of 12, stand if dealer shows 4–6, otherwise hit.
    if total == 12:
        return "stand" if 4 <= dealer_val <= 6 else "hit"
    # In all other cases, hit.
    return "hit"
