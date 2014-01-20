from __future__ import print_function
import corpustor
import nltk
import special_syllables_en as special_syllables


    
# test_file = 'corpii/chunk1.txt'
test_file = 'corpii/hundaKtst.txt'
# test_file = 'corpii/smallsample.txt'


# set up tests

tests = []
with open(test_file) as f:
    for line in f:
        tests.append(line)

def test_last_word_extraction():
    for t in tests:
        w = corpustor.get_last_word(t)
        print(t.rstrip(), w, sep=' ')



def test_fabric_of_reality():
    words = set([w.lower() for w in nltk.corpus.words.words()])
    cmuwords = set([w.lower() for w,x in nltk.corpus.cmudict.entries()])
    net_words = [x for x,y in [z.split() for z in special_syllables.internet_syllables]]
    print(net_words)
    print('extraced %d words from nltk, %d from cmudict' % (len(words), len(cmuwords)))


    words = cmuwords

    words = words.union(set(net_words))

    ts = [t for t in tests if not corpustor.contains_url(t)]
    print('testing %d tweets' % len(tests))
    fails = []

    for t in ts:
        w = corpustor.get_last_word(t)
        if w and w.lower() not in words:
            fails.append(w)

    print(fails, '\n', '%d total fails' % len(fails))
    
    # for f in fails:
    #     if corpustor.is_camel(f):
    #         print(f)

    
    return fails

def test_end_sounds():
    
    for t in tests:
        w = corpustor.get_last_word(t)
        s = corpustor.end_sound(t)
        print( w, s, sep=' ')

def test_finding_rhymes():
    print('testing rhyme finding?')
    rhyme_style = []
    # generate our line-by-line data:
    for t in tests:
        metadata = {
        'syllables': corpustor.count_syllables(t),
        'end_word': corpustor.end_sount(t)
        'end_sound': corpustor.end_sound(t)[1:],
        'real_word_ratio': corpustor.real_word_ratio(t),
        'text': corpustor.get_last_word(t)
        }
        
        if metadata['end_sound']:
            rhyme_style.append(metadata)

    print('extracted metadata from %d rhymes' % len(rhyme_style))
    # actually look for rhymes:
    set_of_rhymes = set(repr(w['end_sound']) for w in rhyme_style)

    set_of_rhymes = [eval(w) for w in set_of_rhymes]
    print('found %d unique sounds in %d total' % (len(set_of_rhymes), len(rhyme_style)))
    
    rhymes = list()
    for r in set_of_rhymes:
        rw = ''.join(r)
        rr = [w['text'] for w in rhyme_style if w['end_sound'] == r]
        if len(rr) > 1:
            rhymes.append(rr)


    for r in rhymes:
        print(r,'\n\n')


if __name__ == "__main__":
    # test_last_word_extraction()
    # test_fabric_of_reality()
    # test_end_sounds()
    test_finding_rhymes()