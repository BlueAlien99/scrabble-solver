from bisect import bisect_left
import re

from letters import points

DICTIONARY_PATH = './dictionary.txt'


def read_words(dictionary_path):
    with open(dictionary_path) as file:
        return sorted([line.strip().upper() for line in file])


def read_letters():
    return list(input('Your letters (blank=_): ').upper())


def stringify_menu(menu):
    str = ''
    for key, val in menu.items():
        str += f"{key}: {val}\n"
    return str


def generate_subsets(tokens: list[str]):
    subsets = []
    for token in tokens:
        to_append = []
        temp_tokens = [f"_{key}_" for key in points.keys()] if token == '_' else [token]
        for temp_token in temp_tokens:
            for subset in subsets:
                for i in range(len(subset)+1):
                    to_append.append(subset[:i] + [temp_token] + subset[i:])
            to_append.append([temp_token])
        subsets.extend(to_append)
    return list(set([''.join(subset) for subset in subsets]))


def is_valid_word(dictionary: list[str], word: str):
    clean_word = word.replace('_', '')
    pos = bisect_left(dictionary, clean_word)
    return True if pos != len(dictionary) and dictionary[pos] == clean_word else False


def filter_valid_words(dictionary: list[str], words: list[str]):
    return list(filter(lambda word: is_valid_word(dictionary, word), words))


def filter_containing_subword(scored, subword):
    return list(filter(lambda word: subword in word[1] and subword != word[1], scored))


def score_word(word: str):
    score = 0
    for letter in re.sub(r"_._", "", word):
        score += points[letter]
    return score


def score_words(words: list[str]):
    scored = [(score_word(word), word) for word in words]
    scored.sort(reverse=True)
    return scored


def generate_from_tokens(dictionary: list[str], tokens: list[str]):
    return score_words(filter_valid_words(dictionary, generate_subsets(tokens)))


menu = {
    '/': 'Exit',
    'u': 'Update letters',
    'a': 'Any word using letters',
    's': 'Enter subword finding mode (/ to exit)'
}


def main():
    dictionary = read_words(DICTIONARY_PATH)
    letters = []

    should_exit = False
    while not should_exit:
        print(stringify_menu(menu))
        option = input('What do you want to do? ')
        match option:
            case '/':
                should_exit = True
            case 'u':
                letters = read_letters()
            case 'a':
                print(generate_from_tokens(dictionary, letters))
            case 's':
                subword_exit = False
                while not subword_exit:
                    subword = input('Subword: ').upper()
                    if subword == '/':
                        subword_exit = True
                    else:
                        print(filter_containing_subword(generate_from_tokens(dictionary, letters + [subword]), subword))
            case _:
                print('Wrong option!')


if __name__ == '__main__':
    main()
