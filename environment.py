import random
from typing import List


class Card:
    """
    A playing card with 1-based indexing for suits and faces:
      suit in {1..4}, face in {1..13}
    Where face=1 => Ace, 2..10 => 2..10, 11 => Jack, 12 => Queen, 13 => King.
    """
    # For human-readable printing: index 1 => Ace
    FACES_HUMAN = [None, 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    # Index 1 => spade, 2 => heart, 3 => diamond, 4 => club
    SUITS_HUMAN = [None, u"\u2660", u"\u2665", u"\u2666", u"\u2663"]

    def __init__(self, suit: int, face: int) -> None:
        """
        suit: int in [1..4]
        face: int in [1..13]
        """
        self.suit: int = suit
        self.face: int = face

    def is_ace(self) -> bool:
        return self.face == 1

    def get_face(self) -> str:
        return Card.FACES_HUMAN[self.face]

    def get_suit(self) -> str:
        return Card.SUITS_HUMAN[self.suit]

    def value(self) -> int:
        """
        Returns the *initial* blackjack value of the card:
          - Ace as 11
          - 2..10 as 2..10
          - J, Q, K as 10
        """
        if self.face == 1:
            return 11  # Ace initially as 11
        elif 2 <= self.face <= 10:
            return self.face
        else:
            return 10  # J, Q, K

    def hi_lo_value(self) -> int:
        """
        Returns the Hi-Lo count contribution:
          - 2..6 => +1
          - 7..9 => 0
          - 10..13 => -1
          - Ace => -1
        """
        if 2 <= self.face <= 6:
            return 1
        elif 7 <= self.face <= 9:
            return 0
        else:
            return -1

    def __str__(self) -> str:
        face_symbol = Card.FACES_HUMAN[self.face]
        suit_symbol = Card.SUITS_HUMAN[self.suit]
        return f"{suit_symbol}{face_symbol}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        # For blackjack splitting, cards are considered equal if their face is equal.
        return self.face == other.face

    def __hash__(self) -> int:
        return hash(self.face)


class BlackjackEnvironment:
    """
    Environment that constructs a shoe (deck) of Card objects
    and manages dealing and the Hi-Lo running count.
    """

    def __init__(self, num_decks: int = 4) -> None:
        self.num_decks: int = num_decks
        self.deck: List[Card] = []
        self.running_count: int = 0
        self.cards_seen: int = 0
        self.reset()

    def reset(self) -> None:
        self.deck = []
        # For each deck in the shoe:
        for _ in range(self.num_decks):
            for suit in range(1, 5):
                for face in range(1, 14):
                    self.deck.append(Card(suit, face))
        random.shuffle(self.deck)
        self.running_count = 0
        self.cards_seen = 0

    def deal(self, reveal: bool = True) -> Card:
        card = self.deck.pop()
        self.cards_seen += 1
        if reveal:
            self.update_count(card)
        return card

    def update_count(self, card: Card) -> None:
        self.running_count += card.hi_lo_value()

    @property
    def true_count(self) -> float:
        remaining_decks = max(len(self.deck) / 52.0, 0.5)
        return self.running_count / remaining_decks

    def remaining_cards(self) -> int:
        return len(self.deck)
