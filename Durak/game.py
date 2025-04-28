
from card import Card
from datetime import datetime


class Game:

    def __init__(self, new_game, player_1, player_2) :
        print("=================================================================")
        print("                        Игра началась!")
        self.new_game = new_game
        self.player_1 = player_1
        self.player_2 = player_2

        self.status_message_1 = True
        self.status_message_2 = False
        self.status_message_3 = False
        self.message = ''

        self.winner = ''

        self.cards_on_table = []
        self.cards_in_game = []

        self.suits = [0x2660, 0x2665, 0x2666, 0x2663]
        self.values = [6, 7, 8, 9, 10, "В", "Д", "K", "Т"]
        self.cards = []

        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(chr(suit), value)) # создаем колоду из набора карт

    def first_round(self):

        self.player_1.attack = True
        self.player_1.defend = False

        self.player_2.attack = False
        self.player_2.defend = True

    def verify_cards(self, at, df):
        if len(self.cards_in_game) > 0 and len(self.cards_in_game) % 2 == 0:
            if self.cards_in_game[-1] > self.cards_in_game[-2]:
                self.status_message_3 = False
                self.status_message_2 = True
                self.status_message_1 = False
                for c in self.cards_in_game:
                    self.cards_on_table.append(c)
                self.cards_in_game.clear()
            else:
                self.status_message_3 = True
                self.status_message_2 = False
                self.status_message_1 = False
                if at.attack is True:
                    at.take_cards(self.cards_in_game.pop())
                    at.attack = True
                    at.defend = False
                    df.attack = False
                    df.defend = True
                else:
                    df.take_cards(self.cards_in_game.pop())
                    df.attack = False
                    df.defend = True
                    at.attack = True
                    at.defend = False

    def print_table(self):

        if self.status_message_1:
            self.message = "Ваша карта"
        elif self.status_message_2:
            self.message = "Соперник отбил вашу карту!"
        elif self.status_message_3:
            self.message = "Недопустимый ход! Попробуйте выбрать другую карту"

        print(f"\n{self.cards_on_table} - Карты на столе")
        print(f"{self.cards_in_game} - {self.message}")
        self.status_message_3 = False
        self.status_message_2 = False
        self.status_message_1 = True

    def cards_in_game(self, card):
        self.cards_in_game.append(card)

    def dealing_cards(self, pack):  # раздаем карты игрокам

        print("Зашел")
        cnt_1 = 0
        cnt_2 = 0
        while len(self.player_1.my_cards()) < 6:
            card_1 = pack.get_card()
            if card_1 is not None:
                self.player_1.take_cards(card_1)
            else:
                break
        print(cnt_1)
        while len(self.player_2.my_cards()) < 6:
            card_2 = pack.get_card()
            if card_2 is not None:
                self.player_2.take_cards(card_2)
            else:
                break
        print(cnt_2)

    def to_attack(self, at, df):

        next_round = False

        while True:
            self.print_table()
            at.print_cards()
            user_input = input('Выберите карту или укажите "z", чтобы выбрать ход "PASS": ')

            if user_input.isdigit():
                card = at.make_move(int(user_input))
                self.cards_in_game.append(card)
                break

            elif user_input == "z":
                at.attack = False
                at.defend = True
                df.attack = True
                df.defend = False

                self.cards_on_table.clear()

                next_round = True

                break

            if len(at.cards) == 0:
                at.attack = False
                at.defend = True
                df.attack = True
                df.defend = False

                next_round = True

                break

            else:
                print("Данная команда не поддерживается!")
                continue

        return next_round

    def to_defend(self, df, at):

        next_round = False

        while True:
            self.print_table()
            df.print_cards()
            user_input = input('Выберите карту или укажите "z", чтобы поднять карты со стола: ')

            if user_input.isdigit():
                card = df.make_move(int(user_input))
                self.cards_in_game.append(card)
                break

            elif user_input == "z":
                for c in self.cards_in_game:
                    self.cards_on_table.append(c)
                self.cards_in_game.clear()
                self.throw_the_cards(at, df)
                df.pick_up_cards(self.cards_on_table)
                self.cards_on_table.clear()

                df.attack = False
                df.defend = True
                at.attack = True
                at.defend = False

                next_round = True

                break

            if len(df.cards) == 0:
                df.attack = True
                df.defend = False
                at.attack = False
                at.defend = True

                break

            else:
                print("Данная команда не поддерживается!")
                continue

        return next_round

    def throw_the_cards(self, df, at):

        th_cards = []
        for c in df.cards:
            if c in self.cards_on_table:
                th_cards.append(c)
        while len(th_cards) > 0:
            self.print_table()

            print("=================================================================")
            print(df.my_cards())
            for number in range(len(th_cards)):
                print(f"{number+1}-{th_cards[number]}", end = " ")
            print(f"--- {at.name} поднимает. {df.name} вы можете подкинуть. Вот возможные варианты.")

            user_input = input('Выберите карту или укажите "z": ')
            if user_input.isdigit():
                card = th_cards.pop(int(user_input)-1)
                df.cards.remove(card)
                self.cards_on_table.append(card)

            elif user_input == "z":
                break

            else:
                print("Данная команда не поддерживается!")
                continue

    def record_the_results(self):
        date_now = datetime.now()
        today_date = datetime.strftime(date_now, '%Y-%m-%d')
        now_time = datetime.strftime(date_now, '%H.%M.%S')

        with open('./game_results.txt', 'a', encoding='utf-8') as file:
            file.write(f"\nДата - {today_date}; Время - {now_time}"
                       f"\nИгрок 1 - {self.player_1.name}; Игрок 2 - {self.player_2.name}"
                       f"\nПобедитель! - {self.winner.name}\n\n\n")






