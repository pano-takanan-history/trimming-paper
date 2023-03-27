from lingreg.util import prep_wordlist, prep_alignments
from lingpy import *

def run(wordlist):
    taxa = wordlist.taxa[:20]
    dct = {0: wordlist.columns}
    for idx, doc in wordlist.iter_rows("doculect"):
        if doc in taxa:
            dct[idx] = wordlist[idx]
    wordlist = prep_wordlist(wordlist.__class__(dct))
    alms = Alignments(wordlist, ref="cogid", transcription="form")
    alms = prep_alignments(alms)
    alms.align()
    return alms
