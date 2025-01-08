import re
from random import choice

class Word:
    fileURL = 'russian-nouns.txt'
    with open(fileURL, 'r', encoding='utf-8') as file:
        words = file.readlines()

    @staticmethod
    def new_word():
        word = choice(Word.words).strip()
        return word.upper()


class Game:
    # в случае, если потребуется доработка с инициализацией пользователя (имя и тд)
    def __init__(self, player_name = 'искатель приключений', game_session = 0):
        self.player_name = player_name
        self.game_session = game_session
        self.choice = None

    # Выход из игры
    @staticmethod
    def stop():
        print('КОНЕЦ ИГРЫ')

    # Описание и графический вывод Виселицы
    @staticmethod
    def display_graph(key: int  = 0):
        hangman = {
            0: [
                f"\033[1m{chr(95):2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            1: [
                f"\033[1m{chr(95):2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            2: [
                f"\033[1m{chr(95):2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):6}\033[33m{chr(124)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            3: [
                f"\033[1m{chr(95):2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[33m{chr(47)}{chr(124)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            4: [
                f"\033[1m{chr(95):2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[33m{chr(47)}{chr(124)}{chr(92)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            5: [
                f"\033[1m{chr(95):2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[33m{chr(47)}{chr(124)}{chr(92)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[33m{chr(47):2}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            6: [
                f"\033[1m{chr(95):2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[31m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[31m{chr(47)}{chr(124)}{chr(92)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[31m{chr(47):2}{chr(92)}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ]
        }
        return ''.join(hangman[key])

    # проверка буквы в слове
    @staticmethod
    def check_letter(word: str, letter, curr_word: str):
        result_word = curr_word
        if letter in word:
            for i in range(len(word)):
                if word[i] == letter:
                    result_word = result_word[:i] + letter + result_word[i+1:]
        return result_word

    # Запрашиваем Пользователя о начале игры или выходе
    def start_or_exit(self):
        try:
            player_choice = int(input(f"Для начала новой игры введите цифру 1"
                                      f"\nДля выхода из игры введите цифру 0"
                                      f"\n"))
            if player_choice == 1:
                self.choice = True
                return None
            elif player_choice == 0:
                self.choice = False
                return None
            else:
                raise ValueError
        except ValueError as e:
            print("Для продолжения введите число 1 или 0 (новая игра или выход, соответственно)")
            self.start_or_exit()

    # Запуск игры
    def start(self):
        # проверяем, первый ли запуск игры пользователем (session) - для вывода приветствия
        if self.game_session == 0:
            print(f'Привет, {self.player_name}!')
            print('Это игра ВИСЕЛИЦА! Твоя задача отгадать задуманное мной слово по буквам. Поехали?')
            print('~' * 20)

        # предлагаем новую игру или выход
        self.start_or_exit()

        # в случае выхода - завершаем игру
        if not self.choice:
            self.stop()
        # в случае продолжения - начинаем игру
        else:
            # запускаем счетчик сессий (игр) текущего игрока
            self.game_session += 1

            # генерируем новое загаданное слово
            new_word = Word.new_word()

            # формируем текущее отображение слова
            curr_word = chr(95) * len(new_word)

            # текущая буква, введенная пользователем
            letters = []

            # Текущее кол-во ошибок
            faults = 0

            # Запускаем цикл в пределах допустимого кол-ва ошибок
            while faults < 6:

                # Выводим виселицу
                print(self.display_graph(faults))

                # Выводим загадываемое слово
                print('СЛОВО: ', ' '.join(curr_word))

                # Проверка на вводимые символы (должны быть только русские буквы)
                is_cyr_char = lambda char: bool(re.fullmatch(r'[А-ЯЁ]', char))
                while True:
                    current_letter = input('Введите одну русскую букву: ').upper()

                    if is_cyr_char(current_letter):
                        if not current_letter in new_word and not current_letter in letters:
                            faults += 1
                            letters.append(current_letter)
                        else:
                            curr_word = self.check_letter(new_word, current_letter, curr_word)
                        break

                # Выводим количество ошибок и вводимые неправильные буквы
                print(f'ОШИБОК: ({faults} из 6) \033[31m{", ".join(letters) if letters else ''}\033[0m')

                print(f'+ ' * 20)

                # Проверка на выход из цикла в случае, если Пользователь угадал слово целиком
                if not chr(95) in curr_word:
                    break

            # Выводим итоговую виселицу и результат
            print(self.display_graph(faults))
            if not chr(95) in curr_word:
                print(f'Вы выиграли, поздравляю! Загаданное слово - {new_word}')
            else:
                print(f'Вы проиграли. Загаданное слово - {new_word}')
            print('~' * 20)

            # Предлагаем сыграть еще или выйти из игры
            self.start()



new_game = Game()
new_game.start()