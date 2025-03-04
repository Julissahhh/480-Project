from abc import ABC, abstractmethod
import time
from typing import List, Optional
from environment import Card, BlackjackEnvironment
from utils import hand_value, basic_strategy


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
                if action == 'hit':
                    hand.append(env.deal())
                elif action == "split":
                    # Check split conditions: using Card.__eq__ (which compares faces)
                    if len(hand) == 2 and hand[0] == hand[1] and self.bankroll >= self.hand_bets[i]:
                        # Deduct bet and split
                        self.bankroll -= self.hand_bets[i]
                        self.hand_bets.append(self.hand_bets[i])
                        card = hand.pop()
                        new_hand = [card]
                        hand.append(env.deal())
                        new_hand.append(env.deal())
                        self.hands.append(new_hand)
                        break  # Reprocess hands after split
                    else:
                        # Fallback to hit if split not possible
                        actions[-1] = 'hit'
                        hand.append(env.deal())
                elif action == "double":
                    if len(hand) == 2 and self.bankroll >= self.hand_bets[i]:
                        self.bankroll -= self.hand_bets[i]
                        self.hand_bets[i] *= 2  # Double the bet
                        hand.append(env.deal())
                        break  # Stop taking actions after doubling down
                    else:
                        actions[-1] = 'hit'
                        hand.append(env.deal())
                elif action == "stand":
                    break
                else:
                    break  # eventually handle other actions
            all_actions.append(actions)
            i += 1
        return all_actions


class HumanAgent(Agent):
    def place_bet(self, true_count: float) -> int:
        print(f"True Count: {true_count}")
        while True:
            try:
                print(f"\nCurrent bankroll: ${self.bankroll}")
                bet = int(input("Enter your bet: "))
                if 0 < bet <= self.bankroll:
                    self.bankroll -= bet
                    self.hand_bets.append(bet)
                    return bet
                print(f"Invalid bet! Must be between 1 and {self.bankroll}")
            except ValueError:
                print("Please enter a valid number")

    def play_turn(self, dealer_upcard: Card, env: BlackjackEnvironment) -> List[List[str]]:
        all_actions: List[List[str]] = []
        i = 0
        while i < len(self.hands):
            hand = self.hands[i]
            actions: List[str] = []
            while hand_value(hand) < 21:
                print(f"\n--- Hand {i + 1} ---")
                print(f"Your hand: {hand} ({hand_value(hand)})")
                print(f"Dealer's upcard: {dealer_upcard}")

                # Show split option only if valid
                valid_actions = ['hit', 'stand', 'double']
                if len(hand) == 2 and hand[0] == hand[1] and self.bankroll >= self.hand_bets[i]:
                    valid_actions.append('split')

                action = input(f"Action ({'/'.join(valid_actions)}): ").lower()

                if action not in valid_actions:
                    print("Invalid action!")
                    continue

                actions.append(action)

                if action == 'hit':
                    hand.append(env.deal())
                elif action == 'double':
                    if len(hand) == 2 and self.bankroll >= self.hand_bets[i]:
                        self.bankroll -= self.hand_bets[i]
                        self.hand_bets[i] *= 2
                        hand.append(env.deal())
                        break  # Double only allows one card
                    else:
                        print("Cannot double!")
                        actions.pop()
                elif action == 'split':
                    # Split logic: check equality using Card.__eq__
                    if len(hand) == 2 and hand[0] == hand[1] and self.bankroll >= self.hand_bets[i]:
                        self.bankroll -= self.hand_bets[i]
                        split_card = hand.pop()
                        new_hand = [split_card, env.deal()]
                        self.hands.append(new_hand)
                        hand.append(env.deal())
                        print(f"Split into Hand {i + 1} and Hand {len(self.hands)}")
                    else:
                        print("Cannot split!")
                        actions.pop()
                else:  # Stand
                    break
            all_actions.append(actions)
            i += 1
        time.sleep(1)
        return all_actions
