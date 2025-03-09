from typing import List
from environment import Card
from enum import Enum

class GameState(str, Enum):
    BETTING = "betting"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    RESOLUTION = "resolution"

class Action(str, Enum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE_HIT = "double_hit"     # Dh = "Double if possible, otherwise Hit"
    DOUBLE_STAND = "double_stand" # Ds = "Double if possible, otherwise Stand"
    SPLIT = "split"

    def __repr__(self):
        return self.value

BASIC_STRATEGY = {
    # Hard totals
    (8, '2'): 'hit', (8, '3'): 'hit', (8, '4'): 'hit', (8, '5'): 'hit', (8, '6'): 'hit', (8, '7'): 'hit', (8, '8'): 'hit', (8, '9'): 'hit', (8, '10'): 'hit', (8, 'A'): 'hit',

    (9, '2'): 'hit', (9, '3'): 'double_hit', (9, '4'): 'double_hit', (9, '5'): 'double_hit', (9, '6'): 'double_hit', (9, '7'): 'hit', (9, '8'): 'hit', (9, '9'): 'hit', (9, '10'): 'hit', (9, 'A'): 'hit',

    (10, '2'): 'double_hit', (10, '3'): 'double_hit', (10, '4'): 'double_hit', (10, '5'): 'double_hit', (10, '6'): 'double_hit', (10, '7'): 'double_hit', (10, '8'): 'double_hit', (10, '9'): 'double_hit', (10, '10'): 'hit', (10, 'A'): 'hit',
    (11, '2'): 'double_hit', (11, '3'): 'double_hit', (11, '4'): 'double_hit', (11, '5'): 'double_hit', (11, '6'): 'double_hit', (11, '7'): 'double_hit', (11, '8'): 'double_hit', (11, '9'): 'double_hit', (11, '10'): 'hit', (11, 'A'): 'hit',

    (12, '2'): 'hit', (12, '3'): 'hit', (12, '4'): 'stand', (12, '5'): 'stand', (12, '6'): 'stand', (12, '7'): 'hit', (12, '8'): 'hit', (12, '9'): 'hit', (12, '10'): 'hit', (12, 'A'): 'hit',

    (13, '2'): 'stand', (13, '3'): 'stand', (13, '4'): 'stand', (13, '5'): 'stand', (13, '6'): 'stand', (13, '7'): 'hit', (13, '8'): 'hit', (13, '9'): 'hit', (13, '10'): 'hit', (13, 'A'): 'hit',
    (14, '2'): 'stand', (14, '3'): 'stand', (14, '4'): 'stand', (14, '5'): 'stand', (14, '6'): 'stand', (14, '7'): 'hit', (14, '8'): 'hit', (14, '9'): 'hit', (14, '10'): 'hit', (14, 'A'): 'hit',
    (15, '2'): 'stand', (15, '3'): 'stand', (15, '4'): 'stand', (15, '5'): 'stand', (15, '6'): 'stand', (15, '7'): 'hit', (15, '8'): 'hit', (15, '9'): 'hit', (15, '10'): 'hit', (15, 'A'): 'hit',
    (16, '2'): 'stand', (16, '3'): 'stand', (16, '4'): 'stand', (16, '5'): 'stand', (16, '6'): 'stand', (16, '7'): 'hit', (16, '8'): 'hit', (16, '9'): 'hit', (16, '10'): 'hit', (16, 'A'): 'hit',

    (17, '2'): 'stand', (17, '3'): 'stand', (17, '4'): 'stand', (17, '5'): 'stand', (17, '6'): 'stand', (17, '7'): 'stand', (17, '8'): 'stand', (17, '9'): 'stand', (17, '10'): 'stand', (17, 'A'): 'stand',

    # Soft totals
    ('A2', '2'): 'hit', ('A2', '3'): 'hit', ('A2', '4'): 'hit', ('A2', '5'): 'double_hit', ('A2', '6'): 'double_hit', ('A2', '7'): 'hit', ('A2', '8'): 'hit', ('A2', '9'): 'hit', ('A2', '10'): 'hit', ('A2', 'A'): 'hit',
    ('A3', '2'): 'hit', ('A3', '3'): 'hit', ('A3', '4'): 'hit', ('A3', '5'): 'double_hit', ('A3', '6'): 'double_hit', ('A3', '7'): 'hit', ('A3', '8'): 'hit', ('A3', '9'): 'hit', ('A3', '10'): 'hit', ('A3', 'A'): 'hit',

    ('A4', '2'): 'hit', ('A4', '3'): 'hit', ('A4', '4'): 'double_hit', ('A4', '5'): 'double_hit', ('A4', '6'): 'double_hit', ('A4', '7'): 'hit', ('A4', '8'): 'hit', ('A4', '9'): 'hit', ('A4', '10'): 'hit', ('A4', 'A'): 'hit',
    ('A5', '2'): 'hit', ('A5', '3'): 'hit', ('A5', '4'): 'double_hit', ('A5', '5'): 'double_hit', ('A5', '6'): 'double_hit', ('A5', '7'): 'hit', ('A5', '8'): 'hit', ('A5', '9'): 'hit', ('A5', '10'): 'hit', ('A5', 'A'): 'hit',

    ('A6', '2'): 'hit', ('A6', '3'): 'double_hit', ('A6', '4'): 'double_hit', ('A6', '5'): 'double_hit', ('A6', '6'): 'double_hit', ('A6', '7'): 'hit', ('A6', '8'): 'hit', ('A6', '9'): 'hit', ('A6', '10'): 'hit', ('A6', 'A'): 'hit',

    ('A7', '2'): 'stand', ('A7', '3'): 'double_stand', ('A7', '4'): 'double_stand', ('A7', '5'): 'double_stand', ('A7', '6'): 'double_stand', ('A7', '7'): 'stand', ('A7', '8'): 'stand', ('A7', '9'): 'hit', ('A7', '10'): 'hit', ('A7', 'A'): 'hit',

    ('A8', '2' ): 'stand',
    ('A8', '3' ): 'stand',
    ('A8', '4' ): 'stand',
    ('A8', '5' ): 'stand',
    ('A8', '6' ): 'stand',
    ('A8', '7' ): 'stand',
    ('A8', '8' ): 'stand',
    ('A8', '9' ): 'stand',
    ('A8', '10'): 'stand',
    ('A8', 'A' ): 'stand',

    # Pairs
    ('22', '2'): 'split', ('22', '3'): 'split', ('22', '4'): 'split', ('22', '5'): 'split', ('22', '6'): 'split', ('22', '7'): 'split', ('22', '8'): 'hit', ('22', '9'): 'hit', ('22', '10'): 'hit', ('22', 'A'): 'hit',
    ('33', '2'): 'split', ('33', '3'): 'split', ('33', '4'): 'split', ('33', '5'): 'split', ('33', '6'): 'split', ('33', '7'): 'split', ('33', '8'): 'hit', ('33', '9'): 'hit', ('33', '10'): 'hit', ('33', 'A'): 'hit',

    ('44', '2'): 'hit',
    ('44', '3'): 'hit',
    ('44', '4'): 'hit',
    ('44', '5'): 'split',
    ('44', '6'): 'split',
    ('44', '7'): 'hit',
    ('44', '8'): 'hit',
    ('44', '9'): 'hit',
    ('44', '10'): 'hit',
    ('44', 'A'): 'hit',

    ('55', '2'): 'double_hit',
    ('55', '3'): 'double_hit',
    ('55', '4'): 'double_hit',
    ('55', '5'): 'double_hit',
    ('55', '6'): 'double_hit',
    ('55', '7'): 'double_hit',
    ('55', '8'): 'double_hit',
    ('55', '9'): 'double_hit',
    ('55', '10'): 'hit',
    ('55', 'A'): 'hit',

    ('66', '2'): 'split',
    ('66', '3'): 'split',
    ('66', '4'): 'split',
    ('66', '5'): 'split',
    ('66', '6'): 'split',
    ('66', '7'): 'hit',
    ('66', '8'): 'hit',
    ('66', '9'): 'hit',
    ('66', '10'): 'hit',
    ('66', 'A'): 'hit',

    ('77', '2'): 'split',
    ('77', '3'): 'split',
    ('77', '4'): 'split',
    ('77', '5'): 'split',
    ('77', '6'): 'split',
    ('77', '7'): 'split',
    ('77', '8'): 'hit',
    ('77', '9'): 'hit',
    ('77', '10'): 'hit',
    ('77', 'A'): 'hit',


    ('88', '2'): 'split', ('88', '3'): 'split', ('88', '4'): 'split', ('88', '5'): 'split', ('88', '6'): 'split', ('88', '7'): 'split', ('88', '8'): 'split', ('88', '9'): 'split', ('88', '10'): 'hit', ('88', 'A'): 'hit',

    ('99', '2'): 'split',
    ('99', '3'): 'split',
    ('99', '4'): 'split',
    ('99', '5'): 'split',
    ('99', '6'): 'split',
    ('99', '7'): 'stand',
    ('99', '8'): 'split',
    ('99', '9'): 'split',
    ('99', '10'): 'stand',
    ('99', 'A'): 'stand',

    # 10,10
    ('TT', '2'): 'stand',
    ('TT', '3'): 'stand',
    ('TT', '4'): 'stand',
    ('TT', '5'): 'stand',
    ('TT', '6'): 'stand',
    ('TT', '7'): 'stand',
    ('TT', '8'): 'stand',
    ('TT', '9'): 'stand',
    ('TT', '10'): 'stand',
    ('TT', 'A'): 'stand',

    ('AA', '2'): 'split', ('AA', '3'): 'split', ('AA', '4'): 'split', ('AA', '5'): 'split', ('AA', '6'): 'split', ('AA', '7'): 'split', ('AA', '8'): 'split', ('AA', '9'): 'split', ('AA', '10'): 'split', ('AA', 'A'): 'hit',
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
    """Determines the action based on the player's hand and dealer's upcard using the basic strategy table."""
    total = hand_value(player_hand)
    dealer_val = dealer_card.get_face()  # Convert to human-readable face value (e.g., '2', '3', ..., '10', 'A')
    if dealer_val in ['10', 'J', "Q", "K"]:
        # all face cards worth 10
        dealer_val = '10'
    # Format the player's hand for lookup
    if len(player_hand) == 2 and player_hand[0] == player_hand[1]:  # Pair splitting case
        face = player_hand[0].get_face()
        if face in ['10', 'J', "Q", "K"]:
            face = "T"
        hand_key = (f"{face}{face}", dealer_val)

    elif any(c.is_ace() for c in player_hand) and len(player_hand) == 2:  # Soft total case
        non_ace_card = next(c for c in player_hand if not c.is_ace())
        face = non_ace_card.get_face()
        if non_ace_card.value() > 8:
            # default to the same behavior for soft totals above 18
            face = "8"
        hand_key = (f"A{face}", dealer_val)

    else:  # Hard total case
        if total < 8:
            # all values under 8 do the same thing
            hand_key = (8, dealer_val)
        elif total > 17:
            # stand for greater than 17
            hand_key = (17, dealer_val)
        else:
            hand_key = (total, dealer_val)

    # Look up the action in BASIC_STRATEGY; default to 'stand' if not found
    return Action(BASIC_STRATEGY.get(hand_key, 'stand'))
