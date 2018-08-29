import nltk
from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    same = []

    # Get the list of common lines into same
    for x in a.split('\n'):
        if x in b.split('\n'):
            same.append(x)

    return remove_dup(same)


def sentences(a, b):
    """Return sentences in both a and b"""

    same = []

    # Same procedure like lines?
    # Get the list of common lines into same
    for x in nltk.tokenize.sent_tokenize(a, language='english'):
        if x in nltk.tokenize.sent_tokenize(b, language='english'):
            same.append(x)

    return remove_dup(same)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    same = []

    # Same procedure like lines?
    # Get the list of common lines into same
    for i in range(len(a)):
        if len(a) - i >= n:
            if a[i:i + n] in b:
                same.append(a[i:i + n])
        else:
            break

    return remove_dup(same)


def remove_dup(same):
    """ Remove duplicates found in list "same" """

    for x in same:
        while same.count(x) > 1:
            del same[same.index(x, same.index(x) + 1)]

    return same
