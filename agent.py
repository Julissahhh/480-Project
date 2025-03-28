import time
from abc import ABC, abstractmethod
from typing import List, Optional
from environment import Card, BlackjackEnvironment
from ui import ConsoleUI
from utils import Action, hand_value, recommend_action


class Agent(ABC):
    _id_counter: int = 1
    def __init__(self, bankroll: int = 2000, base_bet: int = 20) -> None:
        self.id: int = Agent._id_counter
        Agent._id_counter += 1
        self.bankroll: int = bankroll
        self.base_bet: int = base_bet
        self.hands: List[List[Card]] = []
        self.hand_bets: List[int] = []
        self.broke_round: Optional[int] = None
        self.stats = {
            'wins': 0,
            'losses': 0,
            'pushes': 0,
            'total_profit': 0,
            'rounds_played': 0,
            'bankroll_history': []
        }

    def adjust_bankroll(self, amount: float) -> None:
        self.bankroll += amount

    def clear_bets(self):
        self.hand_bets = []

    def can_split(self, hand: List[Card], hand_index: int) -> bool:
        split_cost = self.hand_bets[hand_index] * 2
        return (len(hand) == 2 and 
                hand[0] == hand[1] and 
                self.bankroll > split_cost)
    
    def split_hand(self, hand_index: int, env: BlackjackEnvironment) -> None:
        original_hand = self.hands[hand_index]
        split_card = original_hand.pop()
        new_hand = [split_card, env.deal()]
        self.hands.append(new_hand)
        original_hand.append(env.deal())
        self.hand_bets.append(self.hand_bets[hand_index])
    
    def double_hand(self, hand_index: int, env: BlackjackEnvironment) -> None:
        self.hand_bets[hand_index] *= 2
        self.hands[hand_index].append(env.deal())
    
    def can_double(self, hand: List[Card], hand_index: int) -> bool:
        double_cost = self.hand_bets[hand_index] * 2  # Cost of doubling
        return len(hand) == 2 and self.bankroll >= double_cost
    
    @abstractmethod
    def place_bet(self, true_count: float) -> int:
        pass

    @abstractmethod
    def play_turn(self, dealer_upcard: Card, env: BlackjackEnvironment) -> List[List[str]]:
        pass


class BlackjackAgent(Agent):
    def __init__(self, bankroll: int = 10000, base_bet: int = 30, strategy: str = 'basic'):
        super().__init__(bankroll, base_bet)
        self.strategy = strategy

    def place_bet(self, true_count: float) -> int:
        """Places a bet based on the agent's strategy."""

        if self.strategy in ["basic", "unskilled"]:
            bet = self.base_bet  # Always bet the base amount

        elif self.strategy == "counting":
            if true_count <= 1:
                bet_multiplier = 1
            elif 2 <= true_count < 3:
                bet_multiplier = 2  # Only double bet at TC 2
            elif 3 <= true_count < 5:
                bet_multiplier = 3  # Slight increase
            elif 5 <= true_count < 7:
                bet_multiplier = 5  # Mid-range jump
            else:
                bet_multiplier = 7  # Cap at 7x instead of 10x for safety

            if self.bankroll < 5000:  # If bankroll is below 50% of starting value
                bet_multiplier = max(1, bet_multiplier // 2)  # Halve the bet multiplier

            bet = self.base_bet * max(bet_multiplier, 1)

        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        # Ensure bet does not exceed available bankroll
        bet = min(bet, self.bankroll)
        bet = max(bet, 0)

        # Track the bet
        self.hand_bets.append(bet)

        return int(bet)  # Ensure bet is an integer (casinos require whole numbers)

    def play_turn(self, dealer_upcard: Card, env: BlackjackEnvironment) -> List[List[str]]:
        all_actions: List[List[str]] = []
        i = 0
        # We may have to add hands in a single turn
        while i < len(self.hands):
            hand = self.hands[i]
            actions: List[str] = []
            if hand_value(hand) == 21 and len(hand) == 2:
                actions.append(Action.STAND)
            while hand_value(hand) < 21:
                action = recommend_action(hand, dealer_upcard, env.true_count, self.strategy)
                actions.append(action)
                if action == Action.HIT:
                    hand.append(env.deal())
                elif action == Action.SPLIT:
                    if self.can_split(hand, i):
                        self.split_hand(i, env)
                    else:
                        # look up another option
                        other_action = recommend_action(hand, dealer_upcard, env.true_count, self.strategy, allow_split=False)
                        if other_action == Action.HIT:
                            hand.append(env.deal())
                        else:
                            other_action = Action.STAND
                        actions[-1] = other_action
                elif action in (Action.DOUBLE_HIT, Action.DOUBLE_STAND):
                    if self.can_double(hand, i):
                        self.double_hand(i, env)
                        break  # Stop taking actions after doubling down
                    else:
                        # Fall back to the recommended alternative if doubling is not possible
                        if action == Action.DOUBLE_HIT:
                            actions[-1] = Action.HIT
                            hand.append(env.deal())
                        elif action == Action.DOUBLE_STAND:
                            actions[-1] = Action.STAND
                elif action == Action.STAND:
                    break
                else:
                    break  # eventually handle other actions
            all_actions.append(actions)
            i += 1
        return all_actions


class HumanAgent(Agent):
    def __init__(self, bankroll: int = 10000, base_bet: int = 50):
        super().__init__(bankroll, base_bet)
        self.ui = ConsoleUI()

    def place_bet(self, true_count: float) -> int:
        print("--- betting ---")
        print(f"Current True Count: {true_count:.2f}")
        bet = self.ui.prompt_bet(int(self.bankroll))
        self.hand_bets.append(bet)
        return bet

    def play_turn(self, dealer_upcard: Card, env: BlackjackEnvironment) -> List[List[str]]:
        all_actions: List[List[str]] = []
        i = 0
        while i < len(self.hands):
            hand = self.hands[i]
            actions: List[str] = []
            while hand_value(hand) < 21:
                self.ui.display_hand(hand, f"Your Hand {i + 1}")
                valid_actions = self.get_valid_actions(hand, i)
                action = self.ui.prompt_action(valid_actions, hand, dealer_upcard)
                actions.append(action)

                if action == Action.HIT:
                    hand.append(env.deal())
                elif action == Action.SPLIT and Action.SPLIT in valid_actions:
                    self.split_hand(i, env)
                elif action == Action.DOUBLE and action in valid_actions:
                    if self.can_double(hand, i):
                        self.double_hand(i, env)
                        break
                    else:
                        if action == Action.DOUBLE_HIT:
                            hand.append(env.deal())
                        # For DOUBLE_STAND, fall back to standing (do nothing)
                        break
                else:
                    break  # STAND
            all_actions.append(actions)
            i += 1
            time.sleep(0.3)
        return all_actions
    
    def get_valid_actions(self, hand: List[Card], hand_index: int) -> List[Action]:
        valid = [Action.HIT, Action.STAND]
        if self.can_double(hand, hand_index):
            # Add both double variants as valid options.
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