"""
Calculate regularity metrics on dataset.
"""

from lingrex.copar import CoPaR
from lingpy.sequence.sound_classes import token2class
import statistics


def regularity(wordlist, threshold=3, ref="cogid", min_refs=3, missing="Ø",
               gap="-", word_threshold=0.75):
    """
    Check regularity in three flavors.

    - regularity based on the number of correspondence patterns that have more
      or the same number of sites as threshold
    - the proportion of correspondence patterns identified as regular via
      threshold counting all alignment sites
    - the proportion of words that we judge regular, judging words to be
      regular when more than the proportion word_threshold of sites are judged
      to be regular since they can be assigned to patterns that are covered by
      more than threshol sites
    """
    if not hasattr(wordlist, "clusters"):
        raise ValueError("need a CoPaR object with clusters")
    patterns = {
            p: len(vals) for p, vals in wordlist.clusters.items()
            }
    regular_patterns = len([p for p, vals in wordlist.clusters.items() if
                            len(vals) >= threshold])
    regular_proportion = sum([len(vals) for vals in wordlist.clusters.values()
                              if len(vals) >= threshold])
    full_proportion = sum([len(vals) for vals in wordlist.clusters.values()])

    # get the proportion of words
    regular_words, irregular_words = 0, 0
    for cogid, msa in filter(
            lambda x: len(set(x[1]["taxa"])) >= min_refs, 
            wordlist.msa[ref].items()):
        scores = []
        for idx in range(len(msa["alignment"][0])):
            if (cogid, idx) not in wordlist.patterns:
                print("warning, duplicate cognate in {0} / {1}".format(
                    cogid, idx))
            else:
                if max([
                        len(wordlist.clusters[b, c]) for a, b, c in
                        wordlist.patterns[cogid, idx]]) >= threshold:
                    scores += [1]
                else:
                    scores += [0]
        if statistics.mean(scores) >= word_threshold:
            regular_words += len(set(msa["taxa"]))
        else:
            irregular_words += len(set(msa["taxa"]))

    return (
            regular_proportion, 
            full_proportion - regular_proportion,
            full_proportion,
            round((regular_proportion / full_proportion),2),
            regular_words,
            irregular_words,
            regular_words + irregular_words,
            round((regular_words / (regular_words + irregular_words)),2)
            )
