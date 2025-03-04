from typing import List
from utils import hand_value
from environment import BlackjackEnvironment, Card
from agent import BlackjackAgent, HumanAgent, Agent


class BlackjackGame:
    def __init__(self, env: BlackjackEnvironment, agents: List[Agent]) -> None:
        self.env: BlackjackEnvironment = env
        self.agents: List[Agent] = agents
        self.dealer_hand: List[Card] = []

    def new_round(self) -> Card:
        if self.env.remaining_cards() < 52:
            self.env.reset()

        self.dealer_hand = [
            self.env.deal(reveal=False),
            self.env.deal()
        ]
        dealer_upcard: Card = self.dealer_hand[1]
        for agent in self.agents:
            agent.hands = [[self.env.deal(), self.env.deal()]]  # Initialize with one hand
        return dealer_upcard

    def play_dealer_hand(self) -> None:
        print("\n--- Dealer's Turn ---")
        self.env.update_count(self.dealer_hand[0])
        dealer_score = hand_value(self.dealer_hand)
        print(f"Dealer reveals: {self.dealer_hand[0]} (Total: {dealer_score})")
        if dealer_score == 21 and len(self.dealer_hand) == 2:
            return

        while dealer_score < 17:
            new_card = self.env.deal()
            self.dealer_hand.append(new_card)
            dealer_score = hand_value(self.dealer_hand)
            print(f"Dealer draws: {new_card} (Total: {dealer_score})")

    def resolve_bets(self) -> List[List[float]]:
        dealer_score = hand_value(self.dealer_hand)
        dealer_has_natural = len(self.dealer_hand) == 2 and dealer_score == 21
        all_results: List[List[float]] = []
        for agent in self.agents:
            agent_results: List[float] = []
            for j, hand in enumerate(agent.hands):
                player_score = hand_value(hand)
                player_has_natural = len(hand) == 2 and player_score == 21
                if player_score > 21:
                    agent_results.append(-1)
                elif dealer_has_natural:
                    agent_results.append(0 if player_has_natural else -1)
                elif player_has_natural:
                    agent_results.append(1.5)
                elif dealer_score > 21 or player_score > dealer_score:
                    agent_results.append(1)
                elif player_score < dealer_score:
                    agent_results.append(-1)
                else:
                    agent_results.append(0)
            all_results.append(agent_results)
        return all_results

    def run_simulation(self, num_rounds: int = 10) -> None:
        round_num = 1
        dropped_agents: List[Agent] = []
        while round_num <= num_rounds and self.agents:
            print(f"\n========== ROUND {round_num} ==========")
            print(f"True Count: {self.env.true_count:.2f}")

            # Ensure only agents with non-negative bankroll start the round.
            self.agents = [agent for agent in self.agents if agent.bankroll >= 0]
            if not self.agents:
                break

            # Each agent places their bet.
            for agent in self.agents:
                agent.hand_bets = []
                agent.place_bet(self.env.true_count)
                print(f"Player {agent.id} bets: ${agent.hand_bets[0]}")

            dealer_upcard = self.new_round()
            print(f"\nDealer's upcard: {dealer_upcard}")

            # Let each agent take their turn.
            for agent in self.agents:
                print(f"\n--- Player {agent.id}'s Turn ---")
                actions = agent.play_turn(dealer_upcard, self.env)
                print(f"Actions: {actions}")
                for j, hand in enumerate(agent.hands):
                    print(f"Player {agent.id} Hand {j + 1}: {hand} (Value: {hand_value(hand)})")

            # Dealer plays its hand.
            self.play_dealer_hand()

            # Resolve bets.
            print(f"\n--- Round {round_num} Results ---")
            results = self.resolve_bets()
            for i, agent in enumerate(self.agents):
                agent_results = results[i]
                total_win = 0
                print(f"Player {agent.id} Results:")
                for j, result in enumerate(agent_results):
                    bet = agent.hand_bets[j]
                    if result == 1:
                        total_win += bet * 2
                        print(f"-> Win! Won ${bet},")
                    elif result == 1.5:
                        total_win += bet * 2.5
                        print(f"-> Blackjack! Won ${bet * 2.5},")
                    elif result == 0:
                        total_win += bet
                        print(f"-> Push! Bet returned: ${bet},")
                    else:
                        total_win -= bet
                        print(f"Lost ${bet},")
                agent.bankroll += total_win
                print(f"-> Bankroll after round: {agent.bankroll}")

            # Check for agents that went broke (bankroll negative) and remove them.
            remaining_agents = []
            for agent in self.agents:
                if agent.bankroll < 0:
                    agent.broke_round = round_num
                    print(f"Player {agent.id} went broke in round {round_num}!")
                    dropped_agents.append(agent)
                else:
                    remaining_agents.append(agent)
            self.agents = remaining_agents

            if not self.agents:
                print("All agents have gone broke. Ending simulation.")
                break

            round_num += 1

        print("\n--- Game Summary ---")
        for agent in dropped_agents:
            print(f"Player {agent.id} went broke in round {agent.broke_round}.")
        for agent in self.agents:
            print(f"Player {agent.id} finished with bankroll: ${agent.bankroll}")


def simulate_game(num_rounds: int, num_agents: int) -> None:
    env = BlackjackEnvironment()
    agents = [BlackjackAgent() for _ in range(num_agents)]
    game = BlackjackGame(env, agents)
    game.run_simulation(num_rounds)


def play_game(num_rounds: int, num_agents: int) -> None:
    env = BlackjackEnvironment()
    agents = [HumanAgent(), *[BlackjackAgent() for _ in range(num_agents)]]
    game = BlackjackGame(env, agents)
    game.run_simulation(num_rounds)


if __name__ == "__main__":
    print("Would you like to run a simulation or play the game?")
    choice = input("Choice (0=Play, 1=Simulate): ")
    if choice == "0":
        play_game(4, 1)
    else:
        simulate_game(15, 3)
