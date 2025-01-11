import re
from random import choice

def game():
    game_session = 0

    # Генератор нового слова
    def get_new_word():
        file_url = 'russian-nouns.txt'
        try:
            with open(file_url, 'r', encoding='utf-8') as file:
                words = file.readlines()
                new_word = choice(words).strip()
                return new_word.upper()
        except FileNotFoundError:
            raise FileNotFoundError('Упс, кажется я не могу придумать ни одного слова. '
                  'Файл со словами потерялся или поврежден. Пожалуйста, свяжитесь с разработчиком.')

    # Описание и графический вывод Виселицы
    def get_hangman_status(key: int|str = 0):
        hangman = {
            0: [
                f"\033[1m{'_':2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            1: [
                f"\033[1m{'_':2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            2: [
                f"\033[1m{'_':2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):6}\033[33m{chr(124)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            3: [
                f"\033[1m{'_':2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[33m{chr(47)}{chr(124)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            4: [
                f"\033[1m{'_':2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[33m{chr(47)}{chr(124)}{chr(92)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            5: [
                f"\033[1m{'_':2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[33m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[33m{chr(47)}{chr(124)}{chr(92)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[33m{chr(47):2}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            6: [
                f"\033[1m{'_':2}\033[0m" * 4,
                f"\n\033[1m{chr(124):6}\033[0m{chr(166)}",
                f"\n\033[1m{chr(124):6}\033[31m{chr(111)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[31m{chr(47)}{chr(124)}{chr(92)}\033[0m",
                f"\n\033[1m{chr(124):5}\033[31m{chr(47):2}{chr(92)}\033[0m",
                f"\n\033[1m{chr(124)}\033[0m{chr(46) * 8}\n"
            ],
            'win': [
                '(\\___/)',
                f"\n(='.'=)",
                f'\n(")_(")'
            ]
        }
        return ''.join(hangman[key])

    # Проверка введенной буквы в слове
    def check_letter(word: str, letter, masked_word: str):
        result_word = masked_word
        if letter in word:
            for i in range(len(word)):
                if word[i] == letter:
                    result_word = result_word[:i] + letter + result_word[i+1:]
        return result_word

    # Меню (игра или выход)
    def start_or_exit_menu():
        while True:
            try:
                player_choice = (input(f"Для начала новой игры введите цифру 1"
                                          f"\nДля выхода из игры введите цифру 0"
                                          f"\n"))
                match player_choice:
                    case "1":
                        return True
                    case "0":
                        print('КОНЕЦ ИГРЫ')
                        return False
                    case _:
                        raise ValueError
            except ValueError as e:
                print("Вы ввели некорректные данные.")

    # Запуск игры
    def start():
        nonlocal game_session
        # проверяем, первый ли запуск игры пользователем (session) - для вывода приветствия
        if game_session == 0:
            print(f'Привет, искатель приключений!')
            print('Это игра ВИСЕЛИЦА! Твоя задача отгадать задуманное мной слово по буквам. Поехали?')
            print('~' * 20)

        while start_or_exit_menu():

            try:
                new_word = get_new_word()
            except FileNotFoundError as e:
                print(e)
                return
            masked_word = '_' * len(new_word)
            wrong_letters = []
            faults = 0

            while faults < 6:

                print(get_hangman_status(faults))
                print('СЛОВО: ', ' '.join(masked_word))

                # Проверка на вводимые символы (должна быть только 1 русская буква)
                is_cyr_char = lambda char: bool(re.fullmatch(r'[А-ЯЁ]', char))
                while True:
                    current_letter = input('Введите одну русскую букву: ').upper()

                    if is_cyr_char(current_letter):
                        if not current_letter in new_word and not current_letter in wrong_letters:
                            faults += 1
                            wrong_letters.append(current_letter)
                            print(f"Такой буквы в слове нет.")
                        else:
                            masked_word = check_letter(new_word, current_letter, masked_word)
                        break
                    else:
                        print('Вы ввели некорректные данные!')

                # Выводим количество ошибок и вводимые неправильные буквы
                print(f'ОШИБКИ: ({faults} из 6) \033[31m{", ".join(wrong_letters) if wrong_letters else ''}\033[0m')
                print(f'+ ' * 20)

                # Проверка на выход из цикла в случае, если Пользователь угадал слово целиком
                if not '_' in masked_word:
                    break

            # Выводим итоговую виселицу и результат
            if not '_' in masked_word:
                print(get_hangman_status('win'),
                      f'Вы выиграли, поздравляю! Загаданное слово - {new_word}', sep='\n')
            else:
                print(get_hangman_status(faults),
                      f'Вы проиграли. Загаданное слово - {new_word}', sep='\n')
            print('~' * 20)

            game_session += 1
            # start()     # Предлагаем сыграть еще или выйти из игры

    return start()

game()