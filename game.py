from typing import List
from ui import ConsoleUI
from utils import hand_value
from environment import BlackjackEnvironment, Card
from agent import BlackjackAgent, HumanAgent, Agent

class BlackjackGame:
    def __init__(self, env: BlackjackEnvironment, agents: List[Agent]) -> None:
        self.env: BlackjackEnvironment = env
        self.agents: List[Agent] = agents
        self.dropped_agents: List[Agent] = []  # Track agents that go broke
        self.dealer_hand: List[Card] = []
        self.ui = ConsoleUI()

    def place_bets(self) -> None:
        print(f"True Count: {self.env.true_count:.2f}")
        for agent in self.agents:
            bet = agent.place_bet(self.env.true_count)
            print(f"Player {agent.id} bets: ${bet}")

    def initialize_new_round(self) -> Card:
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


    def play_agent_turns(self, dealer_upcard: Card):
        for agent in self.agents:
            print(f"\n--- Player {agent.id}'s Turn ---")
            actions = agent.play_turn(dealer_upcard, self.env)
            print(f"Actions taken: {actions}")
            for i, hand in enumerate(agent.hands):
                self.ui.display_hand(hand, f"Player {agent.id} Hand {i+1}")

    def play_dealer_turn(self) -> None:
        print("\n--- Dealer's Turn ---")
        self.env.update_count(self.dealer_hand[0])
        dealer_score = hand_value(self.dealer_hand)
        print(f"Dealer reveals: {self.dealer_hand[0]} (Total: {dealer_score})")
        if dealer_score == 21 and len(self.dealer_hand) == 2:
            return

        # stand on soft 17
        while dealer_score < 17:
            new_card = self.env.deal()
            self.dealer_hand.append(new_card)
            dealer_score = hand_value(self.dealer_hand)
            self.ui.show_dealer_action("draws", new_card, dealer_score)

    def finalize_round(self, round_num: int) -> None:
        results = self.resolve_bets()
        self.process_payouts(results)
        self.remove_broke_agents(round_num)

    def resolve_bets(self) -> List[List[float]]:
        dealer_score = hand_value(self.dealer_hand)
        dealer_blackjack = len(self.dealer_hand) == 2 and dealer_score == 21
        results = []

        for agent in self.agents:
            agent_results = []
            for hand in agent.hands:
                player_score = hand_value(hand)
                player_blackjack = len(hand) == 2 and player_score == 21

                if player_score > 21:
                    agent_results.append(-1)
                elif dealer_blackjack:
                    agent_results.append(0 if player_blackjack else -1)
                elif player_blackjack:
                    agent_results.append(1.5)
                elif dealer_score > 21 or player_score > dealer_score:
                    agent_results.append(1)
                elif player_score < dealer_score:
                    agent_results.append(-1)
                else:
                    agent_results.append(0)
            results.append(agent_results)
        return results

    def process_payouts(self, results: List[List[float]]) -> None:
        for agent, agent_results in zip(self.agents, results):
            total_win = 0
            for i, result in enumerate(agent_results):
                bet = agent.hand_bets[i]
                payout = round(bet * result)
                total_win += payout
            agent.adjust_bankroll(total_win)
            self.ui.show_round_result(agent.id, agent_results, agent.hand_bets, agent.bankroll)
            agent.clear_bets()

    def remove_broke_agents(self, round_num: int) -> None:
        remaining = []
        for agent in self.agents:
            if agent.bankroll <= 0:
                agent.broke_round = round_num
                print(f"Player {agent.id} went broke in round {round_num}!")
                self.dropped_agents.append(agent)
            else:
                remaining.append(agent)
        self.agents = remaining


    def run_simulation(self, num_rounds: int = 10) -> None:
        round_num = 1
        while round_num <= num_rounds and self.agents:
            print(f"\n======== Round {round_num} ========")
            self.place_bets()
            dealer_upcard = self.initialize_new_round()
            self.ui.show_dealer_upcard(dealer_upcard)
            self.play_agent_turns(dealer_upcard)
            self.play_dealer_turn()
            self.finalize_round(round_num)
            round_num += 1

        print("\n======== Game Summary ========")
        for agent in self.dropped_agents:
            print(f"Player {agent.id} went broke in round {agent.broke_round}.")
        for agent in self.agents:
            print(f"Player {agent.id} finished with bankroll: ${agent.bankroll:.2f}")

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

def main():
    print("Blackjack Game")
    choice = input("Choose mode (0=Play, 1=Simulate): ")

    env = BlackjackEnvironment()
    if choice == "0":
        agents = [HumanAgent(), BlackjackAgent(), BlackjackAgent(strategy='counting')]
        game = BlackjackGame(env, agents)
        game.run_simulation(num_rounds=5)
    else:
        agents = [BlackjackAgent() for _ in range(3)]
        agents.append(BlackjackAgent(strategy='counting'))
        game = BlackjackGame(env, agents)
        game.run_simulation(num_rounds=40)

if __name__ == "__main__":
    main()
