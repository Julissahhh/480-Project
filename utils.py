from typing import List
from environment import Card
from enum import Enum

class Action(str, Enum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"

class GameState(str, Enum):
    BETTING = "betting"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    RESOLUTION = "resolution"
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


def basic_strategy(player_hand: List[Card], dealer_card: Card) -> Action:
    """Simplified basic strategy implementation"""
    total = hand_value(player_hand)
    dealer_val = dealer_card.value()

    # Pair splitting
    if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
        if player_hand[0].face == 1:  # Aces
            return Action.SPLIT
        if player_hand[0].face == 8:  # Eights
            return Action.SPLIT

    # Soft totals (Ace + other card)
    if any(c.is_ace() for c in player_hand) and len(player_hand) == 2:
        if total >= 19:
            return Action.STAND
        if total == 18 and dealer_val >= 9:
            return Action.STAND
        return Action.HIT

    # Hard totals
    if total >= 17:
        return Action.STAND
    if 13 <= total <= 16:
        return Action.STAND if dealer_val <= 6 else Action.HIT
    if total == 12:
        return Action.STAND if 4 <= dealer_val <= 6 else Action.HIT
    if total == 11:
        return Action.DOUBLE
    if total == 10:
        return Action.DOUBLE if dealer_val <= 9 else Action.HIT
    return Action.HIT
