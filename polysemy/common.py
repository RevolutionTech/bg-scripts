from wordfreq import top_n_list

from polysemy.constants import MOST_COMMON_WORDS_REMOVED


def get_common_words():
    top_10000 = top_n_list("en", 10000)
    super_common_words = top_n_list("en", MOST_COMMON_WORDS_REMOVED)
    common_words = set(top_10000) - set(super_common_words)  # pretty common words, but not stuff like 'very' and 'when'
    return common_words
