"""
Игра "проверь удачу", где вы бросаете кости, чтобы собрать как можно больше звёзд.
Вы можете бросать кости сколько угодно раз, но если выпадет три черепа, вы теряете все звёзды.

Игра вдохновлена настольной игрой Zombie Dice - смотреть здесь https://tesera.ru/game/zombie-dice/
"""

import random
from dice import *

print(
    """Игра "проверь удачу", в которой вы бросаете кости с изображениями звезд,
      черепов и вопросительных знаков.

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

print('How many players are there?')
while True:  # Цикл до тех пор, пока пользователь не введет число.
    response = input('> ')
    if response.isdecimal() and int(response) > 1:
        num_players = int(response)
        break
    print('Please enter a number larger than 1.')

player_names = []  # Список имен игроков.
player_scores = {}  # Имена игроков как ключи, очки как значения.

for i in range(num_players):
    while True:  # Цикл до тех пор, пока не введено имя.
        print('What is player #' + str(i + 1) + '\'s name?')
        response = input('> ')
        if response != '' and response not in player_names:
            player_names.append(response)
            player_scores[response] = 0
            break
        print('Please enter a name.')
print()

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

        rollResults = []
        for dice in hand:
            roll = random.randint(1, 6)
            if dice == GOLD:
                if 1 <= roll <= 3:
                    rollResults.append(STAR_FACE)
                    stars += 1
                elif 4 <= roll <= 5:
                    rollResults.append(QUESTION_FACE)
                else:
                    rollResults.append(SKULL_FACE)
                    skulls += 1
            if dice == SILVER:
                if 1 <= roll <= 2:
                    rollResults.append(STAR_FACE)
                    stars += 1
                elif 3 <= roll <= 4:
                    rollResults.append(QUESTION_FACE)
                else:
                    rollResults.append(SKULL_FACE)
                    skulls += 1
            if dice == BRONZE:
                if roll == 1:
                    rollResults.append(STAR_FACE)
                    stars += 1
                elif 2 <= roll <= 4:
                    rollResults.append(QUESTION_FACE)
                else:
                    rollResults.append(SKULL_FACE)
                    skulls += 1

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
