from utils import hand_value
from environment import BlackjackEnvironment
from agent import BlackjackAgent, HumanAgent

class BlackjackGame:
    def __init__(self, env, agents):
        self.env = env
        self.agents = agents
        self.dealer_hand = []
        
    def new_round(self):
        if self.env.remaining_cards() < 52:
            self.env.reset()
            
        # Deal initial cards
        self.dealer_hand = [
            self.env.deal(reveal=False),  # Hole card
            self.env.deal()               # Upcard (revealed)
        ]
        dealer_upcard = self.dealer_hand[1]
        
        for agent in self.agents:
            agent.hand = [
                self.env.deal(),
                self.env.deal()
            ]
            
        return dealer_upcard
    
    def play_dealer_hand(self):
        # Reveal hole card and update count
        print("\n--- Dealer's Turn ---")
        self.env.update_count(self.dealer_hand[0])
        dealer_score = hand_value(self.dealer_hand)
        print(f"Dealer reveals: {self.dealer_hand[0]} (Total: {dealer_score})")
        if dealer_score == 21 and len(self.dealer_hand) == 2:
            return  # Dealer has natural, no action needed
        
        while dealer_score < 17:
            new_card = self.env.deal()
            self.dealer_hand.append(new_card)
            dealer_score = hand_value(self.dealer_hand)
            print(f"Dealer draws: {new_card} (Total: {dealer_score})")
            
    def resolve_bets(self):
        dealer_score = hand_value(self.dealer_hand)
        dealer_has_natural = len(self.dealer_hand) == 2 and dealer_score == 21
        results = []
        for i, agent in enumerate(self.agents):
            player_score = hand_value(agent.hand)
            player_has_natural = len(agent.hand) == 2 and player_score == 21
            if player_score > 21:
                results.append(-1)
            elif dealer_has_natural:
                results.append(0 if player_has_natural else -1)
            elif player_has_natural:
                results.append(1.5)  # 3:2 payout
            elif dealer_score > 21 or player_score > dealer_score:
                results.append(1)
            elif player_score < dealer_score:
                results.append(-1)
            else:
                results.append(0)
        return results
    
    def run_simulation(self, num_rounds=10):
        for round_num in range(1, num_rounds + 1):
            print(f"\n===== ROUND {round_num} =====")
            print(f"True Count: {self.env.true_count:.2f}")
            # first things first, place the bets
            bets = [agent.place_bet(self.env.true_count) for agent in self.agents]
            for i, bet in enumerate(bets):
                print(f"Player {i+1} bets: ${bet}")

            # then, deal each player and the dealer their cards, this is done
            # in the new_round function
            dealer_upcard = self.new_round()
            print(f"\nDealer's upcard: {dealer_upcard}")

            # let each player decide their action
            for i, agent in enumerate(self.agents):
                print(f"\n--- Player {i + 1}'s Turn ---")
                actions = agent.play_turn(dealer_upcard, self.env)
                print(f"Actions: {actions}")
                print(f"Player {i+1} Final hand: {agent.hand} (Value: {hand_value(agent.hand)})")

            # dealer reveals their card, draws till 17
            self.play_dealer_hand()

            # check everyone's results
            print(f"\n--- Round {round_num} Results ---")
            results = self.resolve_bets()
            for i, result in enumerate(results):
                print(f"Player {i+1}", end=" ")
                if result == 1:
                    self.agents[i].bankroll += bets[i] * 2
                    print(f"-> Win! Won ${bets[i]},", end=" ")
                elif result == 1.5:
                    self.agents[i].bankroll += bets[i] * 2.5  # 3:2 payout
                    print(f"-> Blackjack! Won ${bets[i]* 2.5},", end=" ")
                elif result == 0:
                    self.agents[i].bankroll += bets[i]
                    print(f"-> Push! Bet returned: ${bets[i]},", end=" ")
                else:
                    print(f"Lost ${bets[i]},", end=" ")
                print(f"bankroll after round: {self.agents[i].bankroll}")

def simulate_game(num_rounds, num_agents):
    env = BlackjackEnvironment()
    agents = [BlackjackAgent() for _ in range(num_agents)]
    game = BlackjackGame(env, agents)
    game.run_simulation(num_rounds)

def play_game(num_rounds, num_agents):
    env = BlackjackEnvironment()
    agents = [HumanAgent(), *[BlackjackAgent() for _ in range(num_agents)]]
    game = BlackjackGame(env, agents)
    game.run_simulation(num_rounds)

if __name__ == "__main__":
    play_game(3, 1)