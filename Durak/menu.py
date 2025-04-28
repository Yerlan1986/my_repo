
from pack import Pack
from player import Player
from game import Game

print("Игра в дурака!")
name_1 = input(f"Укажите имя 1-го игрока: ")
player_1 = Player(name_1)
name_2 = input(f"Укажите имя 2-го игрока: ")
player_2 = Player(name_2)

game = Game("new_game", player_1, player_2)   # создаем новую игру
pack = Pack()                                           # создаем колоду
pack.shuffle_pack(game.cards)                           # перемешиваем карты
pack.get_trumps()                                       # выбираем козырную карту
game.first_round()

while True:
    print(len(pack.pack))
    game.dealing_cards(pack)
    print(len(pack.pack))

    while True:

        attack = None
        defend = None

        if player_1.attack is True:
            attack = player_1
        else:
            attack = player_2

        if player_1.defend is True:
            defend = player_1
        else:
            defend = player_2

        print("=================================================================")
        print(f"{pack.trump} - Козырная карта! {len(pack.pack)} карт(-ы) осталось в колоде")
        if game.to_attack(attack, defend) is True:
            break

        print("=================================================================")
        print(f"{pack.trump} - Козырная карта! {len(pack.pack)} карт(-ы) осталось в колоде")
        if game.to_defend(defend, attack) is True:
            break

        game.verify_cards(attack, defend)

    if len(player_1.cards) == 0 and len(pack.pack) == 0:
        game.winner = player_1
        break
    if len(player_2.cards) == 0 and len(pack.pack) == 0:
        game.winner = player_2
        break

print("=================================================================")
print(f"                  Победитель! - *{game.winner.name}*")
print("=================================================================")

game.record_the_results()




















