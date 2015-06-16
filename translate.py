#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from itertools import imap
import urllib2,urllib
import json
import pprint

def get_url(url):
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"
    req = urllib2.Request(url)
    req.add_header("User-Agent",ua)

    try:
        r = urllib2.urlopen(req).read()

    except urllib2.URLError as e:
        print "URLError on url : %s => %s" % (e.url,e.reason,)
        sys.exit(0)

    return r

def sanitize_json(data):
    while ",," in data:
        data = data.replace(",,",",\"\",")
    while "[," in data:
        data = data.replace("[,","[\"\",")
    while ",]" in data:
        data = data.replace(",]",",\"\"]")
    return data


def cmp_score(x,y):
    """ Compare score of translation """
    s1 = x.get("score",0)
    s2 = y.get("score",0)
    return cmp(s1,s2)

def main_translation(data):
    print "%s => %s" % (data[0][1],data[0][0])
    print ""

def other_translation(data):
    if type(data) is not list:
        return
    for typ in data:
        print "[%s]" % (typ[0])
        # typ[1] = liste des traductions, reprises plus précisément par la suite
        for i in xrange(2,len(typ)-2):
            for trans in typ[i]:
                print "%s => %s" % (trans[0],", ".join(trans[1]))
    print ""

def synonym(data):
    if type(data) is not list:
        return
    print "SYNONYMES"
    for typ in data:
        print "[%s]" % (typ[0])
        # typ[1] = liste des traductions, reprises plus précisément par la suite
        for trans in typ[1]:
            print "\t %s" % (", ".join(trans[0]))
    print ""

def translate(text,lin="fr",lout="en",debug=False):
    url = "https://translate.google.fr/translate_a/single?client=t&sl=%s&tl=%s&hl=%s&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=0&otf=1&kc=7&tk=520264|395118&q=%s" % (lin,lout,lout,urllib.quote(text))

    google_response = get_url(url)
    json_data = sanitize_json(google_response)
    r = json.loads(json_data)
    if debug: pprint.pprint(r)

    main_translation(r[0])
    other_translation(r[1])
    if len(r) > 11: synonym(r[11])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Translate text using google services")
    parser.add_argument("text",metavar="TEXT",help="Text to translate",nargs="*")
    parser.add_argument("-i","--input",metavar="LANGUAGE",default="fr",help="Input Language (default fr)")
    parser.add_argument("-o","--output",metavar="LANGUAGE",default="en",help="Output Language (default en)")
    parser.add_argument("-d","--debug",action="store_true",help="Output google json response")
    args = parser.parse_args()

    t = translate(" ".join(args.text),args.input,args.output,args.debug)
