from __future__ import print_function
import re
import nltk
from nltk.corpus import wordnet
import cPickle as pickle
import os
import string

import syllables

def rhyme_word(line):
    """finds the last word of a sentance,
     but in special cases will modify
    it to help our pronounciation engine. """
    word = get_last_word(line)
    if not word:
        return None

    word = re.sub(r'^thx$', 'thanks', word)
    word = re.sub(r'uhh+$', 'uh', word)
    word = re.sub(r'(n|s|y|h)oo+$', lambda m: '%so' % m.group(1), word)

    return word.lower()


def get_last_word(sentance):
    
    sentance = sentance.split()
    while len(sentance):
        word = sentance.pop()
        word = ''.join([w for w in word if w.isalpha()])
        if word:
            if is_camel(word):
                return de_camel(word).split().pop()
            return word


def real_word_ratio(sentance):
    if not hasattr(real_word_ratio, "words"):
        real_word_ratio.words = set(w.lower() for w in nltk.corpus.words.words())
    sentance = format_input(sentance)
    sentance_words = [w.lower() for w in sentance.split() if w.isalpha()]
    if not len(sentance_words):
        return 0
        
    return (float(len([w for w in sentance_words if w in real_word_ratio.words]))
    / len([w for w in sentance_words]))

def synonyms(word):
    syns = set([word])
    synsets = wordnet.synsets(word)
    for sn in synsets:
        syns.update(set(sn.lemma_names))

    return syns



def count_syllables(sentance, debug=False):
    # first lets strip out punctuation and emotive marks
    count = 0
    if debug:
        print('received sentance: %s' % sentance)

    sentance = format_input(sentance)

    if debug:
        print('formatted sentance: %s' % sentance)


    words = [w for w in sentance.split() if w.isalpha()]

    if debug:
        print('extracted words: %s' % repr(words))
        nonwords = [w for w in sentance.split() if not w.isalpha()]
        if nonwords:
            print('found nonwords: %s' % repr(words))


    for w in words:
        if w[0] == '#':
            w = w[1:]
            sylls = count_syllables(de_camel(w))
        else:
            sylls = syllables.count(w)


        count += sylls

        if debug:
            print('%s\t\t\t%d' %(w, sylls))

    if debug:
        print('total\t\t\t%d' % count)
    return count

def format_input(sentance):
    return stripped_string(sentance)

def de_camel(word):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', word)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower()


def is_camel(word):
    if de_camel(word) == word.lower():
        return False
    else:
        return True


def stripped_string(text, spaces=False):
    """
    returns string with all non alpha chars removed
    """
    text = re.sub(r'&', ' and ', text) #  handle ampersands
    text = re.sub(r'http://[a-zA-Z0-9\./]*\w', '(link)', text) # remove links
    return re.sub(r'[^a-zA-Z ]', '', text)


def contains_url(text):
    if re.search(r'http://[a-zA-Z0-9\./]*\w', text):
        return True
    else:
        return False




def main():
    print(synonyms('cheer'))
    print(synonyms('space'))
    print(synonyms('assgrabhat'))
    print(synonyms('rage'))
    pass


if __name__ == "__main__":
    main()