import random

from dice import (
    FACE_HEIGHT,
    FACE_WIDTH,
    QUESTION_FACE,
    GOLD,
    SILVER,
    BRONZE,
)
from game import (
    get_players_count,
    get_players_names,
    fill_names_and_scores,
    fill_rolls
)

num_players: int | None = get_players_count()

player_names: list[str] = []
player_scores: dict[str, int] = {}

fill_names_and_scores(
    get_players_names(num_players),
    player_names,
    player_scores
)


def game_logic():
    turn = 0  # Первый ход у игрока player_names[0].
    # (!) Раскомментируйте, чтобы игрок с именем 'Al' начал с тремя очками:
    # player_scores['Al'] = 3
    endGameWith = None
    while True:  # Основной игровой цикл.
        print()
        print('SCORES: ', end='')
        for i, name in enumerate(player_names):
            print(name + ' = ' + str(player_scores[name]), end='')
            if i != len(player_names) - 1:
                # Все имена игроков кроме последнего разделяются запятыми.
                print(', ', end='')
        print('\n')

        stars = 0  # Счетчик собранных звезд.
        skulls = 0  # Счетчик собранных черепов.
        cup = ([GOLD] * 6) + ([SILVER] * 4) + ([BRONZE] * 3)  # Кубок с костями.
        hand = []  # Игрок начинает с пустой руки.
        print('It is ' + player_names[turn] + '\'s turn.')
        while True:  # Цикл бросков костей.
            print()

            if (3 - len(hand)) > len(cup):  # Проверка на наличие костей в кубке.
                print('There aren\'t enough dice left in the cup to '
                      + 'continue ' + player_names[turn] + '\'s turn.')
                break

            random.shuffle(cup)  # Перемешивание костей в кубке.
            while len(hand) < 3:
                hand.append(cup.pop())

            rollResults: list[list[str]] = []

            stars, skulls = fill_rolls(rollResults, hand)

            for lineNum in range(FACE_HEIGHT):
                for diceNum in range(3):
                    print(rollResults[diceNum][lineNum] + ' ', end='')
                print()  # Новая строка.

            for diceType in hand:
                print(diceType.center(FACE_WIDTH) + ' ', end='')
            print()  # Новая строка.

            print('Stars collected:', stars, '  Skulls collected:', skulls)

            if skulls >= 3:
                print('3 or more skulls means you\'ve lost your stars!')
                input('Press Enter to continue...')
                break

            print(player_names[turn] + ', do you want to roll again? Y/N')
            while True:  # Цикл до ввода Y или N:
                response = input('> ').upper()
                if response != '' and response[0] in ('Y', 'N'):
                    break
                print('Please enter Yes or No.')

            if response.startswith('N'):
                print(player_names[turn], 'got', stars, 'stars!')
                player_scores[player_names[turn]] += stars

                if (endGameWith == None and player_scores[player_names[turn]] >= 13):
                    print('\n\n' + ('!' * 60))
                    print(player_names[turn] + ' has reached 13 points!!!')
                    print('Everyone else will get one more turn!')
                    print(('!' * 60) + '\n\n')
                    endGameWith = player_names[turn]
                input('Press Enter to continue...')
                break

            nextHand = []
            for i in range(3):
                if rollResults[i] == QUESTION_FACE:
                    nextHand.append(hand[i])  # Сохранение вопросительных знаков.
            hand = nextHand

        turn = (turn + 1) % num_players  # Переход хода к следующему игроку.

        if endGameWith == player_names[turn]:  # Завершение игры.
            break

    print('The game has ended...')

    print()
    print('SCORES: ', end='')
    for i, name in enumerate(player_names):
        print(name + ' = ' + str(player_scores[name]), end='')
        if i != len(player_names) - 1:
            print(', ', end='')
    print('\n')

    highestScore = 0
    winners = []
    for name, score in player_scores.items():
        if score > highestScore:
            highestScore = score
            winners = [name]
        elif score == highestScore:
            winners.append(name)

    if len(winners) == 1:
        print('The winner is ' + winners[0] + '!!!')
    else:
        print('The winners are: ' + ', '.join(winners))

    print('Thanks for playing!')


if __name__ == '__main__':
    game_logic()
