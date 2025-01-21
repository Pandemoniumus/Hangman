import re
from random import choice
from resources import hangman, mask_sign, separator
from messages import USER_MESSAGES


attempts_quantity = len(hangman) - 2    # количество попыток в игре в зависимости от количества состояний виселицы

def get_new_word(file_url: str = 'russian-nouns.txt') -> str | None:
    """
        Возвращает случайное слово из файла.

        :param file_url: Путь и название файла со словами
        :return: Слово в верхнем регистре или None, если файл отсутствует
        """
    try:
        with open(file_url, 'r', encoding='utf-8') as file:
            words = [word.strip() for word in file if word.strip()]
            if not words:           # проверка на пустой файл
                raise FileNotFoundError
            new_word = choice(words)
            return new_word.upper()
    except FileNotFoundError:
        raise FileNotFoundError('Упс, кажется я не могу придумать ни одного слова. '
                                'Файл со словами потерялся или поврежден. Пожалуйста, свяжитесь с разработчиком.')


def show_guessed_word(guessed_word: str) -> str:
    """
    Форматирует и возвращает сообщение с загаданным словом.

    :param guessed_word: Загаданное слово, которое будет выведено.
    :return: Строка с сообщением о загаданном слове.
    """
    return f"Загаданное слово: {guessed_word}"


def get_hangman_status(key: int | str = 0) -> str:
    """
    Возвращает графическое отображение виселицы в зависимости от количества ошибок или поздравление с победой.

    :param key: Количество ошибок (целое число от 0 до количества состояний виселицы) или слово 'win' для отображения победного состояния.
    :return: Строка с ASCII-символами, представляющими состояние виселицы или поздравление с победой.
    """

    return ''.join(hangman[key])


def update_masked_word(guessed_word: str, inputted_letter: str, masked_word: str) -> str:
    """
    Проверяет наличие введенной буквы в загаданном слове, открывает ее в маске слова и возвращает обновленную маску слова.

    :param guessed_word: Загаданное слово, в котором нужно искать букву.
    :param inputted_letter: Введенная пользователем буква, которую нужно проверить.
    :param masked_word: Текущее состояние слова с угаданными буквами (маска).
    :return: Обновленное состояние слова с открытой(ыми) угаданной(ыми) буквой(ами).
    """
    result_word = masked_word
    if inputted_letter in guessed_word:     #TODO: уточнить необходимость данной проверки и исключить при ненадобности
        for i in range(len(guessed_word)):
            if guessed_word[i] == inputted_letter:
                result_word = result_word[:i] + inputted_letter + result_word[i + 1:]
    return result_word


def start_or_quit_game() -> bool:
    """
    Предлагает игроку выбрать между началом новой игры или выходом.

    :return: True - если игрок выбрал начать новую игру; False - если игрок выбрал выход.
    """
    while True:
        try:
            player_choice = (input(f"Для начала новой игры введите цифру 1"
                                   f"\nДля выхода из игры введите цифру 0"
                                   f"\n"))
            match player_choice:
                case "1":
                    return True
                case "0":
                    print(USER_MESSAGES['GAME_OVER'])
                    return False
                case _:
                    raise ValueError
        except ValueError:
            print("Вы ввели некорректные данные.")


def is_cyrillic_char(inputted_letter: str) -> bool:
    """
    Проверяет, является ли введённый символ одной русской буквой (заглавной).

    :param inputted_letter: Буква для проверки.
    :return: True, если символ соответствует одной заглавной русской букве, иначе False.
    """

    return bool(re.fullmatch(r'[А-ЯЁ]', inputted_letter))


def show_game_result(masked_word: str, new_word: str, faults: int) -> None:
    """
    Отображает результат игры (победа или поражение).

    :param masked_word: Текущее состояние слова с угаданными буквами (маска).
    :param new_word: Загаданное слово.
    :param faults: Количество ошибок, допущенных игроком.
    :return: None
    """
    if mask_sign not in masked_word:
        # Победа
        print(get_hangman_status('win'),
              USER_MESSAGES['WIN'], show_guessed_word(new_word),
              sep='\n')
    else:
        # Поражение
        print(get_hangman_status(faults),
              USER_MESSAGES['LOSS'] + ' ' + show_guessed_word(new_word),
              sep='\n')

    # Разделитель для оформления вывода
    print(separator['tilda'])


def start_game() -> None:
    """
    Запускает игру 'Виселица' с основным игровым циклом.

    Последовательность действий:
    - Приветствие игрока.
    - Выбор начала новой игры или выхода через меню.
    - Считывание случайного слова из файла.
    - Основной игровой процесс с вводом букв, проверкой слова и отображением состояния виселицы.
    - Вывод результата (победа или поражение).

    :return: None
    """

    print(USER_MESSAGES['GREETING'])

    while start_or_quit_game():
        try:
            guessed_word = get_new_word()
        except FileNotFoundError as e:
            print(e)
            return
        masked_word = mask_sign * len(guessed_word)
        wrong_letters = []
        faults = 0

        while faults < attempts_quantity:

            # Выводим текущий статус виселицы и загаданного слова
            print(get_hangman_status(faults))
            print('СЛОВО: ', ' '.join(masked_word))

            while True:
                inputted_letter = input('Введите одну русскую букву: ').upper()

                if is_cyrillic_char(inputted_letter):
                    if not inputted_letter in guessed_word and not inputted_letter in wrong_letters:
                        faults += 1
                        wrong_letters.append(inputted_letter)
                        print(f"Такой буквы в слове нет.")
                    else:
                        masked_word = update_masked_word(guessed_word, inputted_letter, masked_word)
                    break
                else:
                    print('Вы ввели некорректные данные!')

            # Выводим количество ошибок и вводимые неправильные буквы
            print(f'ОШИБКИ: ({faults} из {attempts_quantity}) \033[31m{", ".join(sorted(wrong_letters)) if wrong_letters else ''}\033[0m')
            # \033[31m - красный цвет, \033[0m - сброс цвета
            print(separator['plus'])

            # Проверка на выход из цикла в случае, если Пользователь угадал слово целиком
            if not mask_sign in masked_word:
                break

        show_game_result(masked_word, guessed_word, faults)


if __name__ == '__main__':
    start_game()
