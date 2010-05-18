
# bulkdownload.py
#
# Downloads all Dutch etexts from Project Gutenberg's website.
# Todo: Implement other languages as well.
#
# Software by Michiel Overtoom, motoom@xs4all.nl, july 2009.

import urllib2
import re
import os

# To isolate etext book numbers from the index.
# Index sourec looks like: <li class="pgdbetext"><a href="/etext/17077">Over literatuur</li>
hrefpat = re.compile("href=\"\/etext\/([0-9]{5})\"")

# Fetch id's of texts.  No need to parse the HTML source, since we only need to grab numbers.
ids = set()
f = urllib2.urlopen("http://www.gutenberg.org/browse/languages/nl") # all dutch etexts (approx. 400)
for line in f:
    m = hrefpat.search(line)
    if m:
        ids.add(m.group(1)) # 17077
f.close()

# Fetch etexts from locations like http://www.gutenberg.org/files/25257/25257-8.txt
for id in ids:
    ofn = "%s-8.txt" % id
    if os.path.isfile(ofn):
        print "Already exists:", ofn
        continue
    url = "http://www.gutenberg.org/files/%s/%s-8.txt" % (id,id)
    print url
    try:
        f = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print "Warning: Can't fetch:", url
        continue
    of = open("%s-8.txt" % id,"wb")
    of.write(f.read())
    of.close()
    f.close()
