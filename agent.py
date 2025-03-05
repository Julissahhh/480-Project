from abc import ABC, abstractmethod
import time
from typing import List, Optional
from environment import Card, BlackjackEnvironment
from ui import ConsoleUI
from utils import Action, hand_value, basic_strategy


class Agent(ABC):
    _id_counter: int = 1
    def __init__(self, bankroll: int = 1000, base_bet: int = 100) -> None:
        self.id: int = Agent._id_counter
        Agent._id_counter += 1
        self.bankroll: int = bankroll
        self.base_bet: int = base_bet
        self.hands: List[List[Card]] = []
        self.hand_bets: List[int] = []
        self.broke_round: Optional[int] = None

    def adjust_bankroll(self, amount: float) -> None:
        self.bankroll += amount

    def can_split(self, hand: List[Card], hand_index: int) -> bool:
        return (len(hand) == 2 and 
                hand[0] == hand[1] and 
                self.bankroll >= self.hand_bets[hand_index])
    
    def split_hand(self, hand_index: int, env: BlackjackEnvironment) -> None:
        original_hand = self.hands[hand_index]
        split_card = original_hand.pop()
        new_hand = [split_card, env.deal()]
        self.hands.append(new_hand)
        original_hand.append(env.deal())
        self.adjust_bankroll(-self.hand_bets[hand_index])
        self.hand_bets.append(self.hand_bets[hand_index])
    
    def double_hand(self, hand_index: int, env: BlackjackEnvironment) -> None:
        self.adjust_bankroll(-self.hand_bets[hand_index])
        self.hand_bets[hand_index] *= 2
        self.hands[hand_index].append(env.deal())
    
    def can_double(self, hand: List[Card], hand_index: int) -> bool:
        return len(hand) == 2 and self.bankroll >= self.hand_bets[hand_index]   
    
    @abstractmethod
    def place_bet(self, true_count: float) -> int:
        pass

    @abstractmethod
    def play_turn(self, dealer_upcard: Card, env: BlackjackEnvironment) -> List[List[str]]:
        pass


class BlackjackAgent(Agent):
    def place_bet(self, true_count: float) -> int:
        bet = self.base_bet * max(1, round(true_count))
        self.bankroll -= bet
        self.hand_bets.append(bet)  # Track current bet
        return bet

    def play_turn(self, dealer_upcard: Card, env: BlackjackEnvironment) -> List[List[str]]:
        all_actions: List[List[str]] = []
        i = 0
        # We may have to add hands in a single turn
        while i < len(self.hands):
            hand = self.hands[i]
            actions: List[str] = []
            while hand_value(hand) < 21:
                action = basic_strategy(hand, dealer_upcard)
                actions.append(action)
                if action == Action.HIT:
                    hand.append(env.deal())
                elif action == Action.SPLIT:
                    # Check split conditions: using Card.__eq__ (which compares faces)
                    if self.can_split(hand, i):
                        self.split_hand(i, env)
                    else:
                        # Fallback to hit if split not possible
                        actions[-1] = Action.HIT
                        hand.append(env.deal())
                elif action == Action.DOUBLE:
                    if self.can_double(hand, i):
                        self.double_hand(i, env)
                        break  # Stop taking actions after doubling down
                    else:
                        # Fall back to stand if could not double
                        actions[-1] = Action.STAND
                        break
                elif action == Action.STAND:
                    break
                else:
                    break  # eventually handle other actions
            all_actions.append(actions)
            i += 1
        return all_actions


class HumanAgent(Agent):
    def __init__(self, bankroll: int = 1000, base_bet: int = 100):
        super().__init__(bankroll, base_bet)
        self.ui = ConsoleUI()

    def place_bet(self, true_count: float) -> float:
        print(f"Current True Count: {true_count:.2f}")
        bet = self.ui.prompt_bet(int(self.bankroll))
        self.adjust_bankroll(-bet)
        self.hand_bets.append(bet)
        return bet

    def play_turn(self, dealer_upcard: Card, env: BlackjackEnvironment) -> List[List[str]]:
        all_actions: List[List[str]] = []
        i = 0
        while i < len(self.hands):
            hand = self.hands[i]
            actions: List[str] = []
            while hand_value(hand) < 21:
                self.ui.display_hand(hand, f"Your Hand {i+1}")
                valid_actions = self.get_valid_actions(hand, i)
                action = self.ui.prompt_action(valid_actions)
                actions.append(action)

                if action == Action.HIT:
                    hand.append(env.deal())
                elif action == Action.SPLIT and Action.SPLIT in valid_actions:
                    self.split_hand(i, env)
                    break
                elif action == Action.DOUBLE and Action.DOUBLE in valid_actions:
                    self.double_hand(i, env)
                    break
                else:
                    break  # STAND
            all_actions.append(actions)
            i += 1
        return all_actions
    
    def get_valid_actions(self, hand: List[Card], hand_index: int) -> List[Action]:
        valid = [Action.HIT, Action.STAND]
        if self.can_double(hand, hand_index):
            valid.append(Action.DOUBLE)
        if self.can_split(hand, hand_index):
            valid.append(Action.SPLIT)
        return valid

    def split_hand(self, hand_index: int, env: BlackjackEnvironment) -> None:
        super().split_hand(hand_index, env)
        print(f"Split hand into {len(self.hands)} hands")

    def double_hand(self, hand_index: int, env: BlackjackEnvironment) -> None:
        super().double_hand(hand_index, env)
        print(f"Doubled bet to ${self.hand_bets[hand_index]:.2f}")