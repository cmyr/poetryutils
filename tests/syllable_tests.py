# coding: utf-8
import poetryutils

test_data = """ pow 1
#pow 1
*pow* 1
ughh 1
ughhhhh 1
lol 3
qb 2
could 1
couldnt 2
boo 1
hair 1
your 1
smell 1
me 1
let 1
be 1
gee 1
de 1
he 1
she 1
question 2
of 1
a 1
the 1
day 1
re 1
fie 1
sue 1
eme 1
wye 1
gee 1
see 1
ase 1
rue 1
pee 1
sie 1
gue 1
hoe 1
uke 1
ife 1
aye 1
mae 1
ore 1
eye 1
poe 1
ale 1
age 1
ode 1
yoe 1
lie 1
due 1
tye 1
bae 1
ule 1
dye 1
hie 1
ose 1
wee 1
ame 1
yee 1
cue 1
roe 1
sye 1
coe 1
woe 1
nee 1
ope 1
dee 1
ike 1
are 1
tee 1
fee 1
ate 1
doe 1
rie 1
ire 1
ere 1
she 1
gie 1
joe 1
ace 1
zee 1
rhe 1
bee 1
ree 1
ice 1
hue 1
ave 1
soe 1
obe 1
ume 1
vie 1
ure 1
nae 1
awe 1
die 1
lye 1
pie 1
tie 1
fae 1
owe 1
one 1
voe 1
cee 1
ute 1
che 1
ape 1
foe 1
vee 1
ake 1
the 1
eke 1
lue 1
tue 1
abe 1
use 1
toe 1
eve 1
wae 1
ade 1
lee 1
axe 1
ide 1
nye 1
rye 1
ewe 1
dae 1
tae 1
bye 1
my 1
sister 2
just 1
screamed 2
in 1
my 1
fucking 2
ear 1
it's 1
its 1
a 1
fuckin 2
frog 1
shut 1
up 1
manu 2
e 1
ee 1
eee 1
aa 1
aaa 1
ah 1
aah 1
aahh 1
ahh 1
practice 2
*day 1
PracticeDay 3
practice* 2
sexiest 3
pancakes 2
am 1
to 1
going 2
boob 1
stroked 2
holly 2
just 1
my 1
praying 2
bryant 2
earlier 3
it's 1
like 1
that 1
bad 1
wouldn't 2
ppl 2
wishes 2
beyond 2
FaceTime 2
after 2
game 1 
._. 0
the 1
bs 2
n 1
ergh 1
hate 1
being 2
something 2
dont 1
give 1
shit 1
fucked 1
creating 3
project 2
struggle 2
hmm 1
hm 1
love 1
when 1
dont 1
text 1
back 1
ppl 2
back😊 1
lmaoo 4
gawd 1
doing 2
like 1
frank 1
gore 1
i 1
last 1
can't 1
RT 2
nuclear 3
explosion 3
ew 1
omg 3
bye 1
otp 3
athiest 3
athiesm 3
those 1
make 1
thing 1
happen 2
people 2
fuckem 2
that'll 2
b 1
c 1
e 1
u 1
hmm 1
hmmm 1
hmmmm 1
idk 3
idek 4
game 1
hate 1
snuggle 2
mayer 2
chaos 2
simple 2
crying 2
watching 2
midwives 2
saying 2
playing 2
love 1
baseball 2
grind 1
ruins 2
"""


def test_syllables():
    tests = test_data.splitlines()
    tests = [tuple(t.strip().split()) for t in tests if len(t)]
    tests = [(a, int(b)) for a,b in tests]
    for t in tests:
        print('testing %s, expect %d' % (t[0], t[1]))
        # result = sum(syllables.count(w) for w in t[0].split())
        result = poetryutils.count_syllables(t[0])
        print('returned %d' % result)
        assert(result == t[1])







if __name__ == "__main__":
    test_syllables()
