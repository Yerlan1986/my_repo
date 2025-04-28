

class Player:

    def __init__(self, name):
        self.name = name
        self.cards = []

        self.attack = False
        self.defend = False
        self.is_winner = False

    def take_cards(self, card):
        self.cards.append(card)

    def make_move(self, number):
        return self.cards.pop(number-1)

    def pick_up_cards(self, cards):
        for c in cards:
            self.cards.append(c)

    def my_cards(self):
        return self.cards

    def print_cards(self):
        print("=================================================================")
        for number in range(len(self.cards)):
            print(f"{number+1}-{self.cards[number]}", end = " ")
        print(f"--- Карты игрока - {self.name}")
















