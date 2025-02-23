from utils import hand_value

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
        self.env.update_count(self.dealer_hand[0])
        dealer_score = hand_value(self.dealer_hand)
        if dealer_score == 21 and len(self.dealer_hand) == 2:
            return  # Dealer has natural, no action needed
        
        while dealer_score < 17:
            self.dealer_hand.append(self.env.deal())
            dealer_score = hand_value(self.dealer_hand)
            
    def resolve_bets(self):
        dealer_score = hand_value(self.dealer_hand)
        dealer_has_natural = len(self.dealer_hand) == 2 and dealer_score == 21
        results = []
        
        for agent in self.agents:
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
        for _ in range(num_rounds):
            # first things first, place the bets
            bets = [agent.place_bet(self.env.true_count) for agent in self.agents]

            # then, deal each player and the dealer their cards, this is done
            # in the new_round function
            dealer_upcard = self.new_round()

            # let each player decide their action
            for agent in self.agents:
                agent.play_turn(dealer_upcard, self.env)

            # dealer reveals their card, draws till 17
            self.play_dealer_hand()

            # check everyone's results
            results = self.resolve_bets()
            for i, result in enumerate(results):
                if result == 1:
                    self.agents[i].bankroll += bets[i] * 2
                elif result == 1.5:
                    self.agents[i].bankroll += bets[i] * 2.5  # 3:2 payout
                elif result == 0:
                    self.agents[i].bankroll += bets[i]

if __name__ == "__main__":
    from environment import BlackjackEnvironment
    from agent import BlackjackAgent
    env = BlackjackEnvironment()
    agents = [BlackjackAgent() for _ in range(2)]
    game = BlackjackGame(env, agents)
    game.run_simulation(num_rounds=10)