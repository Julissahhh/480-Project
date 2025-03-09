from typing import List
from environment import Card
from utils import Action, hand_value

# A bit of an experiment
class ConsoleUI:
    @staticmethod
    def prompt_bet(bankroll: int) -> int:
        while True:
            try:
                bet = int(input(f"Enter your bet (1-{bankroll}): "))
                if 1 <= bet <= bankroll:
                    return bet
                print(f"Invalid bet! Must be between 1 and {bankroll}")
            except ValueError:
                print("Please enter a valid number")

    @staticmethod
    def prompt_action(valid_actions: List[Action]) -> Action:
        while True:
            action_str = input(f"Action ({'/'.join(a.value for a in valid_actions)}): ").lower()
            try:
                return Action(action_str)
            except ValueError:
                print("Invalid action! Please choose a valid option.")

    @staticmethod
    def display_hand(hand: List[Card], title: str) -> None:
        print(f"{title}: {hand} (Value: {hand_value(hand)})")

    @staticmethod
    def show_dealer_upcard(card: Card) -> None:
        print(f"\nDealer's Upcard: {card}")

    @staticmethod
    def show_dealer_action(action: str, card: Card, total: int) -> None:
        print(f"Dealer {action}: {card} (Total: {total})")

    @staticmethod
    def show_round_result(agent_id: int, results: List[float], bets: List[int], bankroll: float) -> None:
        print(f"\nPlayer {agent_id} Results:")
        for i, result in enumerate(results):
            bet = bets[i]
            payout = bet * result
            if result == 1.5:
                print(f"Hand {i+1}: Blackjack! Bet: ${bet} -> Payout: ${payout}")
            elif result == 1:
                print(f"Hand {i+1}: Win! Bet: ${bet} -> Payout: ${payout}")
            elif result == 0:
                print(f"Hand {i+1}: Push! Bet returned: ${bet}")
            elif result == -1:
                print(f"Hand {i+1}: Loss! Lost: ${bet}")
            else:
                print(f"Hand {i+1}: Unknown result multiplier: {result}")
        print(f"New Bankroll: ${bankroll:.2f}")
