import csv
from functools import partial
from glob import glob
import statistics
from sys import argv
from tabulate import tabulate
from lingpy import Wordlist, Alignments
from lingreg.reg import regularity
from lingreg.trim import trim_by_gap, trim_by_core, get_skeleton, apply_trim, trim_random
from lingrex.copar import CoPaR


if len(argv) > 1:
    data = argv[1:]
else:
    data = [f for f in sorted(glob("datasets/*.tsv")) if "-" not in f]

# settings and major table
table = []
word_threshold = 0.75
pattern_threshold = 3
iterations = 100


def get_copar(filename, min_refs=3, ref="cogid", structure="structure"):
    """
    Utility function carrying out the clustering directly.
    """
    cop = CoPaR(filename, transcription="form", ref=ref, structure=structure,
                min_refs=min_refs)
    cop.get_sites()
    cop.cluster_sites()
    cop.sites_to_pattern()
    return cop


def trim_alignments(
        wordlist,
        trim_fun,
        pattern_threshold=3,
        word_threshold=0.75,
        ref="cogid",
        gap_threshold=0.5,
        skeletons=("CV", "VC")
        ):
    """
    Function takes a wordlist and then applies the trimming procedure.
    """
    new_alms = {}
    for cogid, msa in wordlist.msa[ref].items():
        trimmed = apply_trim(
                msa["alignment"],
                trim_fun(
                    msa["alignment"],
                    threshold=gap_threshold,
                    skeletons=skeletons
                    )
                )
        for idx, row in zip(msa["ID"], trimmed):
            new_alms[idx] = row
    wordlist.add_entries("original_alignment", "alignment", lambda x: x)
    wordlist.add_entries("original_tokens", "tokens", lambda x: x)
    wordlist.add_entries("original_structure", "structure", lambda x: x)
    wordlist.add_entries("alignment", new_alms, lambda x: x, override=True)
    wordlist.add_entries(
            "tokens",
            new_alms, lambda x: [c for c in x if c != "-"],
            override=True)
    wordlist.add_entries(
            "structure",
            new_alms, lambda x: get_skeleton([[c for c in x if c != "-"]]),
            override=True)


random_test = []
frequencies = [["Language", "Trimming", "ID", "Count"]]

for f in data:
    #########################################
    # Prepare data
    name = f.split("/")[1][:-4]
    cop = get_copar(f, ref="cogid", structure="structure", min_refs=3)
    count = 0

    #########################################
    # Get summary stats for each dataset:
    # - langs, concepts, cognate sets, words
    # wl = Wordlist(f)
    # etd = wl.get_etymdict(ref="cogid")
    # print(f"Created {name} with {wl.width} languages, {wl.height} concepts"
    # f",and {len(etd)} cognatesets, and {len(wl)} entries"
    # )

    #########################################
    # Print coverage of correspondence patterns to file
    method = "none"
    for c, vals in cop.clusters.items():
        count += 1
        frequencies.append([name, method, "ID_"+str(count), len(vals)])

    #########################################
    # Regularity stats
    table += [
            [name] + list(
                regularity(
                    cop,
                    word_threshold=word_threshold,
                    threshold=pattern_threshold
                    ))]

    #########################################
    # Run Trimming
    for method, trim_fun, gap_threshold in [
            ("gap", trim_by_gap, 0.5),
            ("core", trim_by_core, 0.5)]:
        alms = Alignments(f, ref="cogid", transcription="form")
        trim_alignments(
                alms,
                pattern_threshold=pattern_threshold,
                word_threshold=word_threshold,
                gap_threshold=gap_threshold,
                trim_fun=trim_fun
                )
        new_f = f.replace(".tsv", "-" + method)
        alms.output("tsv", filename=new_f,  prettify=False)

        cop = get_copar(new_f+".tsv", ref="cogid", structure="structure",
                        min_refs=3)

        # Print gap-results of correspondence patterns to file
        if method == "gap":
            count = 0
            for c, vals in cop.clusters.items():
                count += 1
                frequencies.append([name, method, "ID_"+str(count), len(vals)])

        table += [
            [name+'/'+method] + list(
                regularity(
                    cop,
                    word_threshold=word_threshold,
                    threshold=pattern_threshold
                    ))]

        non_random_eval = list(
                regularity(
                    cop,
                    word_threshold=word_threshold,
                    threshold=pattern_threshold
                    ))[7]

        #########################################
        # Run Random model
        regs = []
        compare_random = []
        for i in range(iterations):
            f_rand = f.replace("datasets", "randomize").replace(".tsv", "-") + method + "-{0}".format(i+1)
            alms = Alignments(f, ref="cogid", transcription="form")
            trim_alignments(
                    alms,
                    pattern_threshold=pattern_threshold,
                    word_threshold=word_threshold,
                    gap_threshold=gap_threshold,
                    trim_fun=partial(trim_random, func=trim_fun)
                    )
            alms.output("tsv", filename=f_rand, prettify=False)
            cop = get_copar(f_rand+".tsv", ref="cogid", structure="structure",
                            min_refs=3)
            regs += [list(regularity(cop, word_threshold=word_threshold,
                                     threshold=pattern_threshold))]
            reg_words = list(regularity(cop, word_threshold=word_threshold,
                                        threshold=pattern_threshold))[7]

            if reg_words > non_random_eval:
                compare_random.append(1)
            else:
                compare_random.append(0)

        sig = compare_random.count(1)
        table += [
                [name+"/"+method+"/r"]+[
                    round(statistics.mean([row[0] for row in regs]), 0),
                    round(statistics.mean([row[1] for row in regs]), 0),
                    round(statistics.mean([row[2] for row in regs]), 0),
                    round(statistics.mean([row[3] for row in regs]), 2),
                    round(statistics.mean([row[4] for row in regs]), 0),
                    round(statistics.mean([row[5] for row in regs]), 0),
                    round(statistics.mean([row[6] for row in regs]), 0),
                    round(statistics.mean([row[7] for row in regs]), 2),
                    ]]

        random_test.append([name+"/"+method, sig])

print(tabulate(
    table,
    tablefmt='latex',
    headers=[
        "Analysis",
        "Frequ. Pat.",
        "Rare Pat.",
        "All Pat.",
        "Frequ. Pat. Prop.",
        "Reg. Words",
        "Irr. Words",
        "All Words",
        "Reg. Word Prop."
        ]
        ))
print(tabulate(random_test, headers=["Language", "Random better than Target"]))

#########################################
# Print Correspondence Pattern-Coverage to file
with open("plot/pattern_distribution.tsv", "w", encoding="utf8") as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerows(frequencies)
