# coding: utf-8
"""
This module holds various MT evaluation metrics.
"""

import sacrebleu
import editdistance


def wer(hypotheses, references): 
    """
    Normalized edit distance from editdistance (word level)

    :param hypotheses: list of hypotheses (strings)
    :param references: list of references (strings)
    :return:
    """
    wer = []
    for hyp, ref in zip(hypotheses, references):
        wer.append(editdistance.eval(hyp.split(), ref.split())/len(ref.split()))
        print("H:", hyp, "SPLIT:", hyp.split(), "LEN:", len(hyp.split()))
        print("R:", ref, "SPLIT:", ref.split(), "LEN:", len(ref.split()))
        print(editdistance.eval(hyp.split(), ref.split())/len(ref.split()))
    print("wer:", sum(wer), "devided by", len(wer))
    return sum(wer)/len(wer)


def cer(hypotheses, references):
    """
    Normalized edit distance from editdistance (character level)

    :param hypotheses: list of hypotheses (strings)
    :param references: list of references (strings)
    :return:
    """
    cer = []
    for hyp, ref in zip(hypotheses, references):
        cer.append(editdistance.eval(' '.join(hyp.split()), ref)/len(ref))
        print("H:", hyp, "SPLIT:", ' '.join(hyp.split()), "LEN:", len(hyp), " & ", len(' '.join(hyp.split())))
        print("R:", ref, "LEN:", len(ref))
        print(editdistance.eval(' '.join(hyp.split()), ref)/len(ref))
    print("cer:", sum(cer), "devided by", len(cer))
    return sum(cer)/len(cer)    


def chrf(hypotheses, references):
    """
    Character F-score from sacrebleu

    :param hypotheses: list of hypotheses (strings)
    :param references: list of references (strings)
    :return:
    """
    return sacrebleu.corpus_chrf(hypotheses=hypotheses, references=references)


def bleu(hypotheses, references):
    """
    Raw corpus BLEU from sacrebleu (without tokenization)

    :param hypotheses: list of hypotheses (strings)
    :param references: list of references (strings)
    :return:
    """
    return sacrebleu.raw_corpus_bleu(sys_stream=hypotheses,
                                     ref_streams=[references]).score


def token_accuracy(hypotheses, references, level="word"):
    """
    Compute the accuracy of hypothesis tokens: correct tokens / all tokens
    Tokens are correct if they appear in the same position in the reference.

    :param hypotheses: list of hypotheses (strings)
    :param references: list of references (strings)
    :param level: segmentation level, either "word", "bpe", or "char"
    :return:
    """
    correct_tokens = 0
    all_tokens = 0
    split_char = " " if level in ["word", "bpe"] else ""
    assert len(hypotheses) == len(references)
    for hyp, ref in zip(hypotheses, references):
        all_tokens += len(hyp)
        for h_i, r_i in zip(hyp.split(split_char), ref.split(split_char)):
            # min(len(h), len(r)) tokens considered
            if h_i == r_i:
                correct_tokens += 1
    return (correct_tokens / all_tokens)*100 if all_tokens > 0 else 0.0


def sequence_accuracy(hypotheses, references):
    """
    Compute the accuracy of hypothesis tokens: correct tokens / all tokens
    Tokens are correct if they appear in the same position in the reference.

    :param hypotheses: list of hypotheses (strings)
    :param references: list of references (strings)
    :return:
    """
    assert len(hypotheses) == len(references)
    correct_sequences = sum([1 for (hyp, ref) in zip(hypotheses, references)
                             if hyp == ref])
    return (correct_sequences / len(hypotheses))*100 if hypotheses else 0.0
