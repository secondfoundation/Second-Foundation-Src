import wikipedia as wi
import wiki2plain as w2
import sys


#def query_wiki(ss):
lang = 'simple'
wiki = wi.Wikipedia(lang)

if len(sys.argv) < 2:
    print 'Exception: no query provided'
    sys.exit(1)

ss = str(sys.argv[1])
for i in xrange(len(sys.argv)-2):
    ss += " "+str(sys.argv[i+2])

print ss 

try:
    raw = wiki.article(ss)
    wiki2plain = w2.Wiki2Plain(raw)
    content = wiki2plain.text
    print content.split("\n")[0]
except:
        # not precise match, lets guess
        raw = wiki.search(ss)
        if not raw: 
            # list is empty
            print 'I do not know what', ss, 'is.'
            raw = None
        else:
            print 'I am not certain I know what', ss, 'is. I will guess.'
            print raw[0]['snippet']
            #wiki2plain = w2.Wiki2Plain(raw[0][0])

#if raw:
#    print raw

#
# nick
# 10/17/13
#
