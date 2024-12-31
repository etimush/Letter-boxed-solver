from functools import reduce

all_words = open('words_alpha.txt').read().splitlines()


class Node():
    def __init__(self):
        self.children: list = [None] * 26
        self.parent :Node  = None
        self.word : str = ""
        self.value : str = ""
        self.depth = 0
        self.is_terminal = False
        self.wordcount : int = 0


def letter_index(letter, all_letter_set: list) -> set:
    return set([i for i in range(len(all_letter_set)) if letter in all_letter_set[i]])


def single_word_pass(all_letter_set: list, root : Node,  valid_words = [], valid_partial_words = []) -> tuple[list,list]:

    if  root.is_terminal and root.depth >= 3 :
        valid_partial_words.append(root.word)
        if all(l in root.word for l in reduce(lambda a, b: a | b, all_letter_set)):
            valid_words.append(root.word)


    for child in root.children:
        if (child is not None)  and (letter_index(root.value, all_letter_set) != letter_index(child.value, all_letter_set)) :
            single_word_pass(all_letter_set, child, valid_words, valid_partial_words)

    return valid_words, valid_partial_words


def solver(all_letter_set: list, root : Node) -> list:
    all_pairs = []
    one_words, all_words = single_word_pass(all_letter_set, root, valid_words= [],valid_partial_words=[])
    if len(one_words) >= 1:
        return one_words

    for word in all_words:
        rl = word[-1]
        _, subwords = single_word_pass(all_letter_set, root.children[ord(rl) - ord("a")], valid_words= [],valid_partial_words=[])
        for w2 in subwords:
            if all(l in word+w2 for l in reduce(lambda a, b: a | b, all_letter_set)):
                all_pairs.append((word, w2))


    return all_pairs


def insert_word(root: Node, word: str) -> None:
    current_node = root
    for l in word:
        if current_node.children[ord(l) -  ord('a')] == None:
            new_node = Node()
            current_node.children[ord(l) - ord('a')] = new_node
            new_node.parent = current_node
            new_node.value = l
            new_node.depth = current_node.depth + 1
        current_node = current_node.children[ord(l) - ord('a')]
    current_node.word = word
    current_node.wordcount += 1
    current_node.is_terminal = True



all_letter_set = [{"n", "h", "a"}, {"c", "i", "l"}, {"s", "o", "y"}, {"r", "v","u" }]
culled_dictionary  = [word  for word in all_words if set(word).issubset(reduce(lambda a, b: a | b, all_letter_set))]
root = Node()
for word in culled_dictionary:
    insert_word(root, word)


twd = solver(all_letter_set, root)
print(twd)
