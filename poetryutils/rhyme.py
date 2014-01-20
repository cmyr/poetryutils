# coding=utf-8

from __future__ import print_function
from __future__ import unicode_literals
import cPickle as pickle
import sys
import os
import re
import requests
import string
import multiprocessing
import time

import poetryutils

# RHYME_DB_PATH = 'rhymes.db'
PHONEME_INDEX_PICKLE_PATH = "data/phonemes.p"

try:
    phoneme_index = pickle.load(open(PHONEME_INDEX_PICKLE_PATH, 'r'))
except IOError:
    phoneme_index = dict()


# rhyme_index = {}
wordlist = set()

ipa_vowels = ['a','e','i','o','u','y','ɑ','ɛ','ɪ','ɩ','ɔ','ɚ','ɷ','ʊ','ʌ','œ','ø','ə','æ','ʒ','ö']

def get_phonemes(word):
    global modified_phonemes
    phonemes = phoneme_index.get(word)
    if not phonemes:
        word = word.lower().strip()
        if not word or any(ch in string.punctuation for ch in word):
            return ""
        espeak_output = os.popen3("speak -v english-us -q --ipa %s"%word, 'r')[1].read()
        phonemes = espeak_output.strip().decode('utf8')
    
        # we don't want to add words to our index when bulk-adding
        # because we're using multiprocessing
        phoneme_index[word] = phonemes
        phonemes = adjust_phonemes(phoneme_index[word])
        modified_phonemes.add((word, phonemes))
        return phonemes

    return adjust_phonemes(phonemes)

def _mp_get_phonemes(word):
    espeak_output = os.popen3("speak -v english-us -q --ipa %s"%word, 'r')[1].read()
    phonemes = espeak_output.strip().decode('utf8')
    return word, phonemes

def convert_phoneme_index():
    """some changes to IPA for our own purposes"""
    modp = set()
    for w,p in phoneme_index.items():
        # modp[adjust_phonemes(p)] = w
        modp.add((w, adjust_phonemes(p)))

    return modp


def adjust_phonemes(phonemes):
    
    if not isinstance(phonemes, basestring):
        print('bad phoneme data:', type(phonemes))
        return
    phonemes = re.sub(r'[ˈˌ]', '', phonemes, flags=re.UNICODE)
    phonemes = re.sub(r'(oː|ɔː)', 'ö', phonemes, flags=re.UNICODE)

    return phonemes

modified_phonemes = convert_phoneme_index()


def get_rhyme_words(word):
    word = word.lower().strip()
    
    phonemes = get_phonemes(word)
    ending = end_sound(phonemes)
    rhymes = [x for x,y in modified_phonemes if end_sound(y) == ending]
    rhymes = [x for x in rhymes if not words_are_homonymy(x, word)]
    return rhymes


def end_sound(phonemes):
    # end sound is the last syllable - initial consonants, if any
    pattern = ur'[aeiouyɑɛɪɩɔɚɷʊʌœøöəæʒˈˌː]+[^ˈˌaeiouyɑɛɪöɩɔɚɷʊʌœöøəæʒː]*$'
    endsound = re.findall(pattern, phonemes, re.UNICODE)
    
    if len(endsound) == 0:
        print("NO END SOUND?", phonemes)
        return
    try:
        return endsound[0]
    except IndexError:
        print("INDEX ERROR?", phonemes, endsound)
        raise


def words_are_homonymy(word1, word2, debug=False):

    phoneme1 = get_phonemes(word1)
    phoneme2 = get_phonemes(word2)

    if debug:
        print(type(phoneme1), type(phoneme2))
        print(phoneme1, phoneme2)

    phoneme1 = re.sub(ur'[ˈˌ]', '', phoneme1, re.UNICODE)
    phoneme2 = re.sub(ur'[ˈˌ]', '', phoneme2, re.UNICODE)

    if debug:
        print(phoneme1, phoneme2)

    if phoneme1 == phoneme2:
        return True

    shorter = phoneme1 if (len(phoneme1) < len(phoneme2)) else phoneme2
    longer = phoneme1 if shorter == phoneme2 else phoneme2

    # if the shorter word begins with a consonant we return True
    # if the longer word contains all the shorter's phonemes
    if re.search(ur'^[^ˈˌaeiouyɑɛɪöɩɔɚɷʊʌœöøəæʒː]', shorter):
        if longer[-len(shorter):] == shorter:
            return True

    return False


def set_word_list(words):
    global wordlist
    wordlist = set(words)
    new_words = set()
    for word in wordlist:
        if word not in phoneme_index:
            new_words.add(word)

    print('set wordlist with %d words, %d new' % (len(wordlist), len(new_words)))
    if not len(new_words):
        # build_rhyme_index()
        return

    add_new_words(new_words)


def add_new_words(words):
    print('extracting phonemes for %d new words' % len(words))
    print('this might take a while.')
    start = time.time()
    pool = multiprocessing.Pool(4)
    result = pool.map(_mp_get_phonemes, words)
    for w,p in result:
        phoneme_index[w] = p
        modified_phonemes.add((w, adjust_phonemes(p)))
    print('finished in %0.2f' % (time.time() - start))
    print('saving updated phoneme list')
    pickle.dump(phoneme_index, open(PHONEME_INDEX_PICKLE_PATH, 'w'))

    

def rhyme_check(word1, word2, debug=False):
    p1 = get_phonemes(word1)
    p2 = get_phonemes(word2)

    if (end_sound(p1) == end_sound(p2)
        and not words_are_homonymy(word1, word2)):
        return True

    return False



def debug_end_sounds(word, modified=False):
    phonemes = get_phonemes(word)
    # if modified:
    #     phonemes = adjust_phonemes(phonemes)
    print("%s/%s"% (word, phonemes))
    print(end_sound(phonemes))


def main():
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument('arg1', type=str, help="required argument")
    # parser.add_argument('arg2', '--argument-2', help='optional boolean argument', action="store_true")
    # args = parser.parse_args()
    setup_tests()
    # test_simple_rhymes()
    # interactive_debug()
    # test_homonymity()
    # test_rhymes()
    test_import_spead()




def setup_tests():
    # import nltk
    # words = nltk.corpus.words.words()

    words = phoneme_index.keys()
    set_word_list(words)

def test_simple_rhymes():
    tests = ['construe', 'true', 'retina']
    for t in tests:
        ws = get_rhyme_words(t)
        for w in ws:
            debug_rhyme(t, w[0])
        # print(t, get_rhyme_words(t))


def interactive_debug():
    while True:
        inp = raw_input('enter a debug word, "q" to quit:')
        if inp == 'q':
            return
        if len(inp.split()) > 1:
            print('please only enter one word')
            continue
        
        ws = get_rhyme_words(inp)
        for w in ws:
            debug_rhyme(inp, w[0])

        tosort = sorted([(y,x) for x,y in ws], reverse=True)
        ws = [(x,y) for y,x in tosort]
        print(ws)


def debug_rhyme(word1, word2):
    p1 = get_phonemes(word1)
    p2 = get_phonemes(word2)
    width = max(len(p1), len(p2))
    print('%s/%s\n' % (word1, word2), p1.rjust(width), p2.rjust(width), sep='\n')

def test_homonymity():
    print(words_are_homonymy('high', 'hi'))
    # print(words_are_homonymy('tie', 'untie'))
    # print(words_are_homonymy('untie', 'tie'))
    print(words_are_homonymy('friend', 'bestfriend', True))
    print(words_are_homonymy('friend', 'girlfriend', True))
    print(words_are_homonymy('hi', 'i', True))
    

def fetch_rhyme_words(word):
    url = 'http://rhymebrain.com/talk?function=getRhymes&word=%s' % word
    words = requests.get(url).json()
    return [w['word'] for w in words]


def test_rhymes():
    while True:
        inp = raw_input('enter a debug word, "q" to quit:')
        if inp == 'q':
            return
        if len(inp.split()) > 1:
            print('please only enter one word')
            continue
        
        rhymes = fetch_rhyme_words(inp)
        for w in rhymes:
            isrhyme = rhyme_check(inp, w)
            print(inp, w, isrhyme)
            if not isrhyme:
                debug_rhyme(inp, w)


def test_import_spead():
    words = set()
    with open('corpii/smallsample.txt') as f:
        sample = f.read().split()
        sample = [w.lower() for w in sample if w.isalpha()]
        words = set(sample)

    # add_new_words_slowly(words)
    add_new_words_quickly(words)
        # tosort = sorted([(y,x) for x,y in ws], reverse=True)
        # ws = [(x,y) for y,x in tosort]
        # print(ws)
# okay, so: we have some sort of basic rhyming thing working.
# but we want our rhymer to find the *good* rhymes, not just *any* rhymes.
# what makes a rhyme good?

# syllable count: the closer they are, the better
# the closeness of the sound, generally;
# not actually just containing the entire sound, or being homonyms

if __name__ == "__main__":
    main()


