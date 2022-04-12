from bisect import bisect_left

from letters import points

DICTIONARY_PATH = './dictionary.txt'


def read_words(dictionary_path):
    with open(dictionary_path) as file:
        return sorted([line.strip() for line in file])


def read_letters():
    return list(input('Your letters: ').upper())


def stringify_menu(menu):
    str = ''
    for key, val in menu.items():
        str += f"{key}: {val}\n"
    return str


def generate_subsets(letters, current_subsets = []):
    subsets = []
    for letter in letters:
        to_append = []
        for subset in subsets:
            for i in range(len(subset)+1):
                to_append.append(subset[:i] + [letter] + subset[i:])
        subsets.extend(to_append)
        subsets.append([letter])
    return list(set([''.join(subset) for subset in subsets]))


def binary_search(a, x, lo=0, hi=None):
    if hi is None: hi = len(a)
    pos = bisect_left(a, x, lo, hi)                  # find insertion position
    return True if pos != hi and a[pos] == x else False  # don't walk off the end


def filter_valid_words(valid_words, words):
    return filter(lambda word: binary_search(valid_words, word), words)


def filter_containing_subword(scored, subword):
    return list(filter(lambda word: subword in word[1] and subword != word[1], scored))


def score_word(word):
    score = 0
    for letter in word:
        score += points[letter]
    return score


def score_words(words):
    scored = []
    for word in words:
        scored.append((score_word(word), word))
    scored.sort(reverse=True)
    return scored


def generate_from_letters(words, letters):
    return score_words(filter_valid_words(words, generate_subsets(letters)))


menu = {
    'x': 'Exit',
    'u': 'Update letters',
    'a': 'Any word using letters',
    's': 'Enter subword finding mode (0 to exit)'
}


if __name__ == '__main__':
    words = read_words(DICTIONARY_PATH)
    letters = []

    exit = False
    while not exit:
        print(stringify_menu(menu))
        option = input('What do you want to do? ')
        match option:
            case 'x':
                exit = True
            case 'u':
                letters = read_letters()
            case 'a':
                print(generate_from_letters(words, letters))
            case 's':
                subword_exit = False
                while not subword_exit:
                    subword = input('Subword: ').upper()
                    if subword == '0':
                        subword_exit = True
                    else:
                        print(filter_containing_subword(generate_from_letters(words, letters + [subword]), subword))
            case _:
                print('Wrong option!')

