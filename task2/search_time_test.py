import copy
import timeit
import random

# with open(file_result_name, "w", encoding="utf-8") as file:
#     previous_word = ""
#     while my_stack_result:
#         word = my_stack_result.pop()
#         if word != previous_word:
#             file.write(word + "\n")
#         previous_word = word
from linkedbst import LinkedBST


def read_dictionary(read_filename):
    """
    Read files
    """
    with open(read_filename, "r", encoding="utf-8") as file:
        list_en = []
        random_words = []
        n_random_words = 900
        all_words = 1000
        pos_random = 0

        random_list = []
        for i in range(0, n_random_words):
            random_list.append(random.randint(0, all_words))

        for n_line, line in enumerate(file):
            word = line.strip().split()[0]

            if word.startswith("+cs="):
                word = word[4:]

            list_en.append(word)
            if n_random_words > 0:
                if n_line in random_list:
                    pos_random += 1
                    random_words.append(word)

                    n_random_words -= 1

            all_words -= 1
            if all_words == 0:
                break

    return list_en, random_words


def test_list(lst_words, random_lst):
    for word in random_lst:
        lst_words.index(word)


def test_bst_ordered(tree, random_lst):
    for word in random_lst:
        tree.find(word)


def test_all():
    test_names = ["test_list", "test_bst_ordered", "test_bst_disordered", "test_bst_balanced"]
    # test_names = ["test_bst_balanced"]
    for test_name in test_names:
        if test_name == "test_bst_disordered":
            lst_test1 = timeit.repeat('test_bst_ordered(tree_random, random_lst)',
                                      'from __main__ import test_bst_ordered, tree_random, random_lst',
                                      number=100, repeat=5)

        elif test_name == "test_bst_balanced":
            lst_test1 = timeit.repeat('test_bst_ordered(tree_balanced, random_lst)',
                                      'from __main__ import test_bst_ordered,'
                                      ' tree_balanced, random_lst',
                                      number=100, repeat=5)

        elif test_name == "test_bst_ordered":
            lst_test1 = timeit.repeat('{}(tree, random_lst)'.format(test_name),
                                      'from __main__ import {}, tree, random_lst'.format(test_name),
                                      number=100, repeat=5)

        else:
            lst_test1 = timeit.repeat('{}(lst_words, random_lst)'.format(test_name),
                                      'from __main__ import {}, lst_words, random_lst'.format(test_name),
                                      number=100, repeat=5)

        average_test_list = sum(lst_test1) / len(lst_test1)

        print(average_test_list)


if __name__ == '__main__':
    lst_words, random_lst = read_dictionary("words.txt")
    lst_words_random = copy.copy(lst_words)
    random.shuffle(lst_words_random)

    tree_random = LinkedBST()
    for word in lst_words_random:
        tree_random.add(word)

    tree = LinkedBST()
    for word in lst_words:
        tree.add(word)

    tree_balanced = tree.rebalance()
    test_all()
