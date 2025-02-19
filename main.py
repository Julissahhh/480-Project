import random
from environment import BlackjackEnvironment
from agent import BlackjackAgent
from utils import hand_value, basic_strategy

if __name__ == "__main__":
    # Initialize Blackjack environment and agents (players)
    env = BlackjackEnvironment()
    players = [BlackjackAgent(env) for _ in range(2)]  # Supports multiple players

    # Run 100 simulated rounds
    for _ in range(100):
        hands = []
        bets = []
        dealer_upcard = None

        # Each player places a bet and plays a hand
        for player in players:
            player_hand, dealer_upcard, bet = player.play_hand()
            hands.append((player, player_hand))
            bets.append(bet)

        # Dealer plays their hand
        dealer_hand = env.play_dealer_hand(dealer_upcard)
        dealer_score = hand_value(dealer_hand)

        # Determine results for each player
        for i, (player, player_hand) in enumerate(hands):
            player_score = hand_value(player_hand)
            bet = bets[i]

            # Check game outcome and update bankroll
            if player_score > 21 or (dealer_score <= 21 and dealer_score > player_score):
                player.bankroll -= bet
            elif dealer_score > 21 or player_score > dealer_score:
                player.bankroll += bet

            print(f"Player {i+1} Bankroll: {player.bankroll}, True Count: {env.counter.true_count():.2f}")
