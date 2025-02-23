"""
Игра "проверь удачу", где вы бросаете кости, чтобы собрать как можно больше звёзд.
Вы можете бросать кости сколько угодно раз, но если выпадет три черепа, вы теряете все звёзды.

Игра вдохновлена настольной игрой Zombie Dice - смотреть здесь https://tesera.ru/game/zombie-dice/
"""
import random

from dice import (
    QUESTION_FACE,
    SKULL_FACE,
    STAR_FACE,
    GOLD,
    SILVER,
    BRONZE,
)

print(
    """Игра "проверь удачу", в которой вы бросаете кости с изображениями 
    звезд, черепов и вопросительных знаков.
    
    На своём ходу вы достаёте три случайные кости из кубка и бросаете их. 
    Вы можете бросить кости снова или завершить ход.
    Если выпадет три черепа, вы теряете все свои звезды и завершаете ход.
    
    Когда один из игроков наберет 13 очков, игра завершается. 
    Побеждает игрок с наибольшим количеством очков.
    
    В кубке 6 золотых, 4 серебряных и 3 бронзовых костей. 
    Золотые кости содержат больше звёзд, бронзовые - больше черепов, 
    а серебряные сбалансированы.
    """
)


def get_players_count() -> int:
    """Цикл до тех пор, пока пользователь не введет число."""
    print('How many players are there?')
    while True:

        response = input('> ')
        if response.isdecimal() and int(response) > 1:
            num_players = int(response)
            break
        print('Please enter a number larger than 1.')

    return num_players


def fill_names_and_scores(data: list[str],
                          names: list[str],
                          scores: dict[str, int]) -> None:
    # names.extend(data)
    # temp_score: dict[str, int] = dict.fromkeys(data, 0)
    for name in data:
        names.append(name)
        scores[name] = 0


def get_players_names(players_count: int) -> list[str]:
    """Цикл до тех пор, пока не введено имя."""
    names: list[str] = []
    for i in range(players_count):
        while True:
            print('What is player #' + str(i + 1) + '\'s name?')
            name = input('> ')
            if name and name not in names:
                names.append(name)
                break
            print('Please enter a name.')
    print()

    return names


def fill_rolls(roll_results, hand):
    stars: int = 0
    skulls: int = 0
    for curr_dice in hand:
        roll = random.randint(1, 6)
        if curr_dice == GOLD:
            if 1 <= roll <= 3:
                roll_results.append(STAR_FACE)
                stars += 1
            elif 4 <= roll <= 5:
                roll_results.append(QUESTION_FACE)
            else:
                roll_results.append(SKULL_FACE)
                skulls += 1
        if curr_dice == SILVER:
            if 1 <= roll <= 2:
                roll_results.append(STAR_FACE)
                stars += 1
            elif 3 <= roll <= 4:
                roll_results.append(QUESTION_FACE)
            else:
                roll_results.append(SKULL_FACE)
                skulls += 1
        if curr_dice == BRONZE:
            if roll == 1:
                roll_results.append(STAR_FACE)
                stars += 1
            elif 2 <= roll <= 4:
                roll_results.append(QUESTION_FACE)
            else:
                roll_results.append(SKULL_FACE)
                skulls += 1
    return stars, skulls
