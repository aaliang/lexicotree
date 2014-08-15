# frequent itemset miner script. may be hard to follow, i'll break it up someday
# pypy compatible

from setenumtree_refless import SetEnumTreeRefless
from collections import Counter, defaultdict, deque
import re
import sys
import json

#after each tail pass, it will prune out unused db transactions

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

STOP_WORDS = frozenset(('a', 'an', 'the', 'of', 'i', 'me', 'rt', 'to', '#tvtag', 'my', 'realhughjackman'))

# tweets_as_tokens = filter(lambda z: 'rt' not in z, [set([y.lower() for y in x if y.lower() not in STOP_WORDS]) for x in tweets])
tweets_as_tokens = filter(lambda z: 'rt' not in z, [set([y.lower() for y in x if y.lower() not in STOP_WORDS]) for x in tweets])

len_tweets = len(tweets_as_tokens)
MIN_SUPP = int(MIN_FREQ * len_tweets)

print 'MIN_SUPP = %s' % MIN_SUPP
cnt = get_counter (tweets_as_tokens, MIN_SUPP)

tweets_as_tokens = list(Counter(frozenset(x for x in t if x in cnt) for t in tweets_as_tokens).iteritems())
# tweets_as_tokens = list[ for x in Counter(frozenset(x for x in t if x in cnt) for t in tweets_as_tokens)]

rankings_dict = dict((v, i) for i,(v,_) in enumerate(cnt.most_common()))
# lt = LexicoTree(tweets_as_tokens, rankings_dict)

# et = SetEnumTreeRefless({1: 0, 2:1, 3:2, 4:3, 5:4}, [1, 2, 3, 4, 5])
et = SetEnumTreeRefless(rankings_dict, rankings_dict.keys())
#lets assume we know the one world common tokens for now
et.grow()

ln = defaultdict(list)
pruned_dict = defaultdict(list)

#func vars to avoid dotting in a tight loop
is_subset = frozenset.issubset
list_append = list.append

pd_iteritems = pruned_dict.iteritems

freq_deque = deque()
freq_deque_clear = freq_deque.clear
freq_deque_extend = freq_deque.extend
#token instances (counted by sum)

freq_set = set()
freq_set_update = freq_set.update
freq_set_clear = freq_set.clear
#misnamed set for checking if transaction is still relevant

print 'len(freq_set) = %s' % len(tweets_as_tokens)

lx = 2
while et.leafs:
   for i, x in enumerate(reversed(et.leafs)):
      xhead = frozenset(x.head)

      freq_deque_extend(t for t in tweets_as_tokens if is_subset(xhead, t[0]))

      freq = sum(f[1] for f in freq_deque)

      if (freq >= MIN_SUPP):
         list_append(ln[lx], (x.head, freq))

         freq_set_update(freq_deque)

         # check the pruned_list yo, and subprune your tail
         if x.tail:
            for pruned_tail_candidate, v in pd_iteritems():
               # if pruned_tail_candidate in reversed(x.tail):
               if pruned_tail_candidate in x.tail_as_set:
                  for t in v:
                     if is_subset(t, xhead):
                        x.tail_as_set.remove(pruned_tail_candidate)
                        x.tail = tuple(x.tail_as_set)
                        break
               if not x.tail:
                  break

         # print "%s - f{%s}" % (x.head, freq)
      else:
         #pseudo-prune
                              #prefix   , suffix
         list_append(pruned_dict[x.head[-1]], frozenset(x.head[:-1]))
         del et.leafs[x]

      freq_deque_clear()

   pruned_dict.clear()

   print 'len(freq_set) = %s' % len(freq_set)
   tweets_as_tokens = list(freq_set)

   freq_set_clear()
   et.grow()

   # print 'len(vset) = %s' %len(vset)
   lx += 1

for k in ln:
   print '\nitemsets of length %s' % k
   sorted_l = sorted(ln[k], key=lambda tup: tup[1])
   for i, f in sorted_l:
      print str(i) + '   f{%s}  =>  %.3f%%'% (f, float(f)*100/len_tweets)

print len_tweets
