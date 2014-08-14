from setenumtree import SetEnumTree
from setenumtree_refless import SetEnumTreeRefless
from collections import Counter, defaultdict
import re
import sys
import json

MIN_FREQ = float(sys.argv[2])

#lol, do this for now
try: #twitter
   statuses = json.load(open(sys.argv[1]))['statuses']
except: #instagram
   statuses = [x['caption'] for x in json.load(open(sys.argv[1])) if x['caption']]

def prep_statuses (statuses):
   #strip out non alphanumeric characters and/or spaces
   #TODO: may want to preserve hashtags and mentions...
   pattern = re.compile('([^\s\w]|_)+')
   return [tuple(pattern.sub('', x['text'].encode('utf-8')).split()) for x in statuses if x]

def get_counter (token_set_list, support):
   c = Counter()
   for token_set in token_set_list:
      c.update(token_set)
   #filter out things under a certain support -> this step may not even be necessary
   return Counter(dict((x, c[x]) for x in c if c[x] >= support))
tweets = prep_statuses(statuses)
#tokenize and filter out the retweets

tweets_as_tokens = filter(lambda z: 'rt' not in z, [set([y.lower() for y in x]) for x in tweets])

MIN_SUPP = int(MIN_FREQ * len(tweets_as_tokens))
cnt = get_counter (tweets_as_tokens, MIN_SUPP)

tweets_as_tokens = [set(x for x in t if x in cnt) for t in tweets_as_tokens]

rankings_dict = dict((v, i) for i,(v,_) in enumerate(cnt.most_common()))
# lt = LexicoTree(tweets_as_tokens, rankings_dict)

et = SetEnumTreeRefless(rankings_dict, rankings_dict.keys())
#lets assume we know the one world common tokens for now
et.grow()

ln = defaultdict(list)
while et.leafs:
   for x in list(et.leafs):
      freq = sum(1 for t in tweets_as_tokens if frozenset(x.head).issubset(t))
      if (freq >= MIN_SUPP):
         ln[len(x.head)].append((x.head, freq))
         # ln.append((x.head, freq))
         # print "%s - f{%s}" % (x.head, freq)
      else:
         #pseudo-prune
         et.leafs.remove(x)
   et.grow()

for k in ln:
   print '\nitemsets of length %s' % k
   sorted_l = sorted(ln[k], key=lambda tup: tup[1])
   for i, f in sorted_l:
      print str(i) + '   f{%s}  =>  %.3f%%'% (f, float(f)*100/len(tweets_as_tokens))

print len(tweets_as_tokens)