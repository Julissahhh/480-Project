import os
from typing import List, Optional
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
        self.verbose = True

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def place_bets(self) -> None:
        if self.verbose:
            print(f"True Count: {self.env.true_count:.2f}")
        for agent in self.agents:
            bet = agent.place_bet(self.env.true_count)
            if self.verbose:
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
            if self.verbose:
                print(f"\n--- Player {agent.id}'s Turn ---")
            actions = agent.play_turn(dealer_upcard, self.env)
            if self.verbose:
                print(f"Actions taken: {actions}")
                for i, hand in enumerate(agent.hands):
                    self.ui.display_hand(hand, f"Player {agent.id} Hand {i + 1}")

    def play_dealer_turn(self) -> None:
        if self.verbose:
            print("\n--- Dealer's Turn ---")
        self.env.update_count(self.dealer_hand[0])
        dealer_score = hand_value(self.dealer_hand)
        if self.verbose:
            print(f"Dealer reveals: {self.dealer_hand[0]} (Total: {dealer_score})")
        if dealer_score == 21 and len(self.dealer_hand) == 2:
            return

        # stand on soft 17
        while dealer_score < 17:
            new_card = self.env.deal()
            self.dealer_hand.append(new_card)
            dealer_score = hand_value(self.dealer_hand)
            if self.verbose:
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
                # Update per-hand stats
                if result in (1, 1.5):
                    agent.stats['wins'] += 1
                elif result == -1:
                    agent.stats['losses'] += 1
                else:
                    agent.stats['pushes'] += 1
            # Update per-round stats
            agent.stats['total_profit'] += total_win
            agent.stats['rounds_played'] += 1
            agent.stats['bankroll_history'].append(agent.bankroll)
            agent.adjust_bankroll(total_win)
            if self.verbose:
                self.ui.show_round_result(agent.id, agent_results, agent.hand_bets, agent.bankroll)
            agent.clear_bets()

    def remove_broke_agents(self, round_num: int) -> None:
        remaining = []
        for agent in self.agents:
            if agent.bankroll <= 0:
                agent.broke_round = round_num
                if self.verbose:
                    print(f"Player {agent.id} went broke in round {round_num}!")
                self.dropped_agents.append(agent)
            else:
                remaining.append(agent)
        self.agents = remaining

    # game.py
    def run_simulation(self, num_rounds: Optional[int] = None, sim_id: int = 0) -> None:
        round_num = 1
        while (num_rounds is None or round_num <= num_rounds) and self.agents:
            if self.verbose:
                print(f"\n======== Round {round_num} ========")
            self.place_bets()
            dealer_upcard = self.initialize_new_round()
            if self.verbose:
                self.ui.show_dealer_upcard(dealer_upcard)
            self.play_agent_turns(dealer_upcard)
            self.play_dealer_turn()
            self.finalize_round(round_num)
            round_num += 1
        if self.verbose:
            print("\n======== Game Summary ========")
            for agent in self.dropped_agents:
                print(f"Player {agent.id} went broke in round {agent.broke_round}.")
            for agent in self.agents:
                print(f"Player {agent.id} finished with bankroll: ${agent.bankroll:.2f}")

        # Print statistics
        print("\n======== Statistics ========")
        all_agents = self.agents + self.dropped_agents
        for agent in all_agents:
            total_hands = agent.stats['wins'] + agent.stats['losses'] + agent.stats['pushes']
            if total_hands == 0:
                continue
            win_rate = agent.stats['wins'] / total_hands
            loss_rate = agent.stats['losses'] / total_hands
            push_rate = agent.stats['pushes'] / total_hands
            avg_profit = agent.stats['total_profit'] / agent.stats['rounds_played'] if agent.stats[
                'rounds_played'] else 0
            print(f"Player {agent.id}:")
            print(f"  Win Rate: {win_rate:.2%}")
            print(f"  Loss Rate: {loss_rate:.2%}")
            print(f"  Push Rate: {push_rate:.2%}")
            print(f"  Total Profit: ${agent.stats['total_profit']:.2f}")
            print(f"  Avg Profit/Round: ${avg_profit:.2f}")
            print(f"  Final Bankroll: ${agent.bankroll:.2f}\n")

        # Write to CSV with append mode and conditional header
        filename = "strat_comparisons.csv"
        header_exists = os.path.exists(filename) and os.stat(filename).st_size > 0

        with open(filename, "a", newline="") as f:
            # Write header only if file is new/empty
            if not header_exists:
                f.write(
                    "Sim ID,Sample,Agent ID,Strategy,Wins,Losses,Pushes,Total Profit,Avg Profit/Round,Final Bankroll\n")

            # Write data rows for all agents
            for agent in all_agents:
                total_hands = agent.stats['wins'] + agent.stats['losses'] + agent.stats['pushes']
                if total_hands == 0:
                    continue

                avg_profit = agent.stats['total_profit'] / agent.stats['rounds_played'] if agent.stats[
                    'rounds_played'] else 0

                # Get strategy type (placeholder for future implementation)
                strategy = getattr(agent, "strategy", "basic")

                f.write(
                    f"{sim_id},"
                    f"{num_rounds},"  # Sample size
                    f"{agent.id},"
                    f"{strategy},"
                    f"{agent.stats['wins']},"
                    f"{agent.stats['losses']},"
                    f"{agent.stats['pushes']},"
                    f"{agent.stats['total_profit']:.2f},"
                    f"{avg_profit:.2f},"
                    f"{agent.bankroll:.2f}\n"
                )


def simulate_games(num_sims: int, rounds_per: int) -> None:
    for sim_id in range(num_sims):
        env = BlackjackEnvironment()
        agents = [BlackjackAgent(strategy='unskilled'), BlackjackAgent(strategy='basic'),
                  BlackjackAgent(strategy='counting')]
        game = BlackjackGame(env, agents)
        game.set_verbose(False)
        game.run_simulation(rounds_per, sim_id=sim_id)


def play_game(num_rounds: int, num_agents: int) -> None:
    env = BlackjackEnvironment()
    agents = [HumanAgent(), *[BlackjackAgent() for _ in range(num_agents)]]
    game = BlackjackGame(env, agents)
    game.run_simulation(num_rounds)


def main():
    print("Blackjack Game")
    choice = input("Choose mode (0=Play, 1=One sim, 2=Multiple sims): ")

    if choice == "0":
        env = BlackjackEnvironment()
        agents = [HumanAgent(), BlackjackAgent()]
        game = BlackjackGame(env, agents)
        game.run_simulation(num_rounds=5)
    elif choice == "1":
        env = BlackjackEnvironment()
        agents = [BlackjackAgent(strategy='unskilled'), BlackjackAgent(strategy='basic'), BlackjackAgent(strategy='counting')]
        game = BlackjackGame(env, agents)
        game.run_simulation(num_rounds=10)
    else:
        simulate_games(4000, 2000)


if __name__ == "__main__":
    main()
