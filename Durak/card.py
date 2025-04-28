

class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.values = [6, 7, 8, 9, 10, "В", "Д", "K", "Т"]

        self.is_trump = False

    def __repr__(self):
        return f'|{self.value}{self.suit}|'

    def __gt__(self, other):

        result = None
        if self.suit == other.suit:
            if self.values.index(self.value) > self.values.index(other.value):
                result = True
            else:
                result = False
        elif self.is_trump is True and other.is_trump is False:
            result = True
        else:
            result = False

        return result

    def __lt__(self, other):

        result = None
        if self.suit == other.suit:
            if self.values.index(self.value) < self.values.index(other.value):
                result = True
            else:
                result = False
        elif self.is_trump is True and other.is_trump is False:
            result = False
        else:
            result = False

        return result

    def __eq__(self, other):

        result = None
        if self is not None and other is not None:
            if self.value == other.value:
                result = True
            else:
                result = False
        else:
            result = False

        return result









































