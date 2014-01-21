"""
tools for poetry-focused textual analysis.
"""

from rhyme import get_rhyme_words, set_word_list
from utils import (rhyme_word, get_last_word, real_word_ratio,
    synonyms, count_syllables, de_camel, is_camel, stripped_string,
    contains_url, low_letter_ratio)