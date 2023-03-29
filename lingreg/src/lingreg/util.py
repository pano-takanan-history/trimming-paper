"""
Utility functions to check the regularity of corresponcence patterns and cognates.
"""
from lingreg.trim import subsequence_of, get_skeleton

def prep_wordlist(wordlist, min_refs=3, exclude="_+", ref="cogid"):
    """
    Preprocessing will make sure that the data are unified.

    - delete markers of morpheme boundaries (often inconsistently applied), as
      indicated by exclude
    - only consider cognate sets with size > min_refs (unique taxa), as identified by
    - delete duplicate words in the same cognate set
    """
    whitelist = []
    for cogid, idxs in wordlist.get_etymdict(ref="cogid").items():
        visited, all_indices = set(), []
        for idx in map(lambda x: x[0], filter(lambda x: x, idxs)):
            if wordlist[idx, "doculect"] not in visited:
                visited.add(wordlist[idx, "doculect"])
                all_indices += [idx]
        if len(visited) >= min_refs:
            whitelist += all_indices
    for idx, tokens in wordlist.iter_rows("tokens"):
        wordlist[idx, "tokens"] = [t for t in tokens if t not in exclude]

    dct = {0: wordlist.columns}
    for idx in whitelist:
        dct[idx] = wordlist[idx]
    return wordlist.__class__(dct)


def prep_alignments(
        wordlist, 
        skeletons=("CV", "VC")
        ):
    whitelist = []
    for cogid, msa in wordlist.msa["cogid"].items():
        skel = get_skeleton(msa["alignment"])
        if any([subsequence_of(s, skel) for s in skeletons]):
            whitelist += msa["ID"]
    wordlist.add_entries(
            "structure", "tokens", lambda x: " ".join(get_skeleton([x])))
    dct = {0: wordlist.columns}
    for idx in whitelist:
        dct[idx] = wordlist[idx]
    return wordlist.__class__(dct, transcription="form")
