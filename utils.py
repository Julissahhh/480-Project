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
    # Hard totals
    (8, '2'): 'hit', (8, '3'): 'hit', (8, '4'): 'hit', (8, '5'): 'hit', (8, '6'): 'hit', (8, '7'): 'hit', (8, '8'): 'hit', (8, '9'): 'hit', (8, '10'): 'hit', (8, 'A'): 'hit',
    (9, '2'): 'hit', (9, '3'): 'double', (9, '4'): 'double', (9, '5'): 'double', (9, '6'): 'double', (9, '7'): 'hit', (9, '8'): 'hit', (9, '9'): 'hit', (9, '10'): 'hit', (9, 'A'): 'hit',
    (10, '2'): 'double', (10, '3'): 'double', (10, '4'): 'double', (10, '5'): 'double', (10, '6'): 'double', (10, '7'): 'double', (10, '8'): 'double', (10, '9'): 'double', (10, '10'): 'hit', (10, 'A'): 'hit',
    (11, '2'): 'double', (11, '3'): 'double', (11, '4'): 'double', (11, '5'): 'double', (11, '6'): 'double', (11, '7'): 'double', (11, '8'): 'double', (11, '9'): 'double', (11, '10'): 'double', (11, 'A'): 'double',
    (12, '2'): 'hit', (12, '3'): 'hit', (12, '4'): 'stand', (12, '5'): 'stand', (12, '6'): 'stand', (12, '7'): 'hit', (12, '8'): 'hit', (12, '9'): 'hit', (12, '10'): 'hit', (12, 'A'): 'hit',
    (13, '2'): 'stand', (13, '3'): 'stand', (13, '4'): 'stand', (13, '5'): 'stand', (13, '6'): 'stand', (13, '7'): 'hit', (13, '8'): 'hit', (13, '9'): 'hit', (13, '10'): 'hit', (13, 'A'): 'hit',
    (14, '2'): 'stand', (14, '3'): 'stand', (14, '4'): 'stand', (14, '5'): 'stand', (14, '6'): 'stand', (14, '7'): 'hit', (14, '8'): 'hit', (14, '9'): 'hit', (14, '10'): 'hit', (14, 'A'): 'hit',
    (15, '2'): 'stand', (15, '3'): 'stand', (15, '4'): 'stand', (15, '5'): 'stand', (15, '6'): 'stand', (15, '7'): 'hit', (15, '8'): 'hit', (15, '9'): 'hit', (15, '10'): 'surrender', (15, 'A'): 'hit',
    (16, '2'): 'stand', (16, '3'): 'stand', (16, '4'): 'stand', (16, '5'): 'stand', (16, '6'): 'stand', (16, '7'): 'hit', (16, '8'): 'hit', (16, '9'): 'hit', (16, '10'): 'surrender', (16, 'A'): 'hit',
    (17, '2'): 'stand', (17, '3'): 'stand', (17, '4'): 'stand', (17, '5'): 'stand', (17, '6'): 'stand', (17, '7'): 'stand', (17, '8'): 'stand', (17, '9'): 'stand', (17, '10'): 'stand', (17, 'A'): 'stand',
    
    # Soft totals
    ('A2', '2'): 'hit', ('A2', '3'): 'hit', ('A2', '4'): 'hit', ('A2', '5'): 'double', ('A2', '6'): 'double', ('A2', '7'): 'hit', ('A2', '8'): 'hit', ('A2', '9'): 'hit', ('A2', '10'): 'hit', ('A2', 'A'): 'hit',
    ('A3', '2'): 'hit', ('A3', '3'): 'hit', ('A3', '4'): 'hit', ('A3', '5'): 'double', ('A3', '6'): 'double', ('A3', '7'): 'hit', ('A3', '8'): 'hit', ('A3', '9'): 'hit', ('A3', '10'): 'hit', ('A3', 'A'): 'hit',
    ('A4', '2'): 'hit', ('A4', '3'): 'hit', ('A4', '4'): 'double', ('A4', '5'): 'double', ('A4', '6'): 'double', ('A4', '7'): 'hit', ('A4', '8'): 'hit', ('A4', '9'): 'hit', ('A4', '10'): 'hit', ('A4', 'A'): 'hit',
    ('A5', '2'): 'hit', ('A5', '3'): 'hit', ('A5', '4'): 'double', ('A5', '5'): 'double', ('A5', '6'): 'double', ('A5', '7'): 'hit', ('A5', '8'): 'hit', ('A5', '9'): 'hit', ('A5', '10'): 'hit', ('A5', 'A'): 'hit',
    ('A6', '2'): 'hit', ('A6', '3'): 'double', ('A6', '4'): 'double', ('A6', '5'): 'double', ('A6', '6'): 'double', ('A6', '7'): 'hit', ('A6', '8'): 'stand', ('A6', '9'): 'stand', ('A6', '10'): 'hit', ('A6', 'A'): 'hit',
    ('A7', '2'): 'stand', ('A7', '3'): 'double', ('A7', '4'): 'double', ('A7', '5'): 'double', ('A7', '6'): 'double', ('A7', '7'): 'stand', ('A7', '8'): 'stand', ('A7', '9'): 'stand', ('A7', '10'): 'hit', ('A7', 'A'): 'hit',
    
    # Pairs
    ('22', '2'): 'split', ('22', '3'): 'split', ('22', '4'): 'split', ('22', '5'): 'split', ('22', '6'): 'split', ('22', '7'): 'split', ('22', '8'): 'hit', ('22', '9'): 'hit', ('22', '10'): 'hit', ('22', 'A'): 'hit',
    ('88', '2'): 'split', ('88', '3'): 'split', ('88', '4'): 'split', ('88', '5'): 'split', ('88', '6'): 'split', ('88', '7'): 'split', ('88', '8'): 'split', ('88', '9'): 'split', ('88', '10'): 'split', ('88', 'A'): 'split',
    ('AA', '2'): 'split', ('AA', '3'): 'split', ('AA', '4'): 'split', ('AA', '5'): 'split', ('AA', '6'): 'split', ('AA', '7'): 'split', ('AA', '8'): 'split', ('AA', '9'): 'split', ('AA', '10'): 'split', ('AA', 'A'): 'split',
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
