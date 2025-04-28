
from random import shuffle, randint


class Pack:

    def __init__(self):
        self.pack = []
        self.trump = None
        self.trump_suit = None

    def shuffle_pack(self, cards):
        self.pack = cards
        shuffle(self.pack)

    def get_card(self):
        if len(self.pack) > 0:
            card = self.pack.pop()
        else:
            card = self.trump
            self.trump = None
        return card

    def get_trumps(self):
        self.trump = self.pack.pop(randint(1, 35))
        self.trump.is_trump = True
        self.trump_suit = self.trump.suit

        for card in self.pack:
            if card.suit == self.trump_suit:
                card.is_trump = True







