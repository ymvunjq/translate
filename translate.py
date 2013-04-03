#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from itertools import imap
import urllib2,urllib
import json

def _get_url(url):
    ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0"
    req = urllib2.Request(url)
    req.add_header("User-Agent",ua)

    try:
        r = urllib2.urlopen(req).read()
    except urllib2.URLError as e:
        print "URLError on url : %s => %s" % (e.url,e.reason,)
        sys.exit(0)

    return r


def cmp_score(x,y):
    """ Compare score of translation """
    s1 = x.get("score",0)
    s2 = y.get("score",0)
    return cmp(s1,s2)


def translate(text,lin="fr",lout="en"):
    url = "http://translate.google.fr/translate_a/t?client=a&text=%s&hl=%s&sl=%s&tl=%s&ie=UTF-8&oe=UTF-8&multires=1&ssel=0&tsel=0&sc=1" % (urllib.quote(text),lin,lin,lout,)

    r = json.loads(_get_url(url))
    out = {}
    if "sentences" in r and "trans" in r["sentences"][0]:
        out["trans"] = r["sentences"][0]["trans"]
    if "dict" in r and "entry" in r["dict"][0]:
        out["other"] = []
        for o in sorted(r["dict"][0]["entry"],lambda x,y: cmp_score(y,x)):
            out["other"].append((o['word'],o['reverse_translation']))
    return out


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Translate text using google services")
    parser.add_argument("text",metavar="TEXT",help="Text to translate",nargs="*")
    parser.add_argument("-i","--input",metavar="LANGUAGE",default="fr",help="Input Language (default fr)")
    parser.add_argument("-o","--output",metavar="LANGUAGE",default="en",help="Output Language (default en)")
    args = parser.parse_args()

    t = translate(" ".join(args.text),args.input,args.output)
    if "trans" in t:
        print t["trans"]
    else:
        print "no translation"
    if "other" in t:
        smax = len(max(imap(lambda x:x[0],t['other']),key=len))
        for o in t["other"]:
            print "%s => %s" % (o[0].ljust(smax," "),",".join(o[1]),)
