# Hi-Lo Card Counting System
HI_LO_VALUES = {
    '2': +1, '3': +1, '4': +1, '5': +1, '6': +1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

class CardCounter:
    """ Implements the Hi-Lo card counting system for Blackjack. """

    def __init__(self, num_decks):
        """
        Initializes the counter.
        :param num_decks: Number of decks in play.
        """
        self.running_count = 0
        self.num_decks = num_decks
        self.cards_seen = 0

    def update_count(self, card):
        """
        Updates the running count based on the dealt card.
        :param card: Card dealt.
        """
        self.running_count += HI_LO_VALUES.get(card, 0)
        self.cards_seen += 1

    def true_count(self):
        """
        Computes the true count by normalizing the running count.
        :return: True count, adjusted for remaining decks.
        """
        remaining_decks = max(self.num_decks - self.cards_seen / 52, 1)
        return self.running_count / remaining_decks
