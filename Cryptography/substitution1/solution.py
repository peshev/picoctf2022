#!/usr/bin/env python3

from collections import Counter
import wordfreq
import re

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()


class Alphabet(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.score = 1


def normalize_word(w):
    return "".join(filter(str.isalpha, w)).lower()


def group_word_frequencies_by_length(word_frequencies):
    by_length = {}
    for w, f in word_frequencies.items():
        by_length.setdefault(len(w), {})[w] = f

    return {
        k: sorted(v.items(), key=lambda x: x[1], reverse=True)
        for k, v in
        by_length.items()
    }


def group_words_by_length(words):
    by_length = {}
    for w in words:
        by_length.setdefault(len(w), []).append(w)
    return by_length


def find_alphabet(ciphertext, plaintext, frequency, primer, length):
    assert len(ciphertext) == len(plaintext)
    zipped = list(zip(ciphertext, plaintext))
    cipher_to_plain = {}
    plain_to_cipher = {}
    for c, p in zipped:
        if primer.get(c, p) != p:
            return
        if c in cipher_to_plain:
            if cipher_to_plain[c] != p:
                return
            else:
                cipher_to_plain[c] = p
        if p in plain_to_cipher:
            if plain_to_cipher[p] != c:
                return
            else:
                plain_to_cipher[p] = c

    found = False
    for a in alphabets:
        if all(a.get(c, p) == p for c, p in zipped):
            found = True
            for c, p in zipped:
                a[c] = p
            if len(a) >= length:
                return a
            a.score += len(ciphertext) * frequency

    if not found:
        alphabets.append(Alphabet({**primer, **dict(zipped)}))


def decrypt(ciphertext, alphabet):
    result = []
    for c in ciphertext:
        if c.lower() in alphabet:
            p = alphabet.get(c.lower())
            if c.isupper():
                p = p.upper()
        else:
            p = c
        result.append(p)
    return "".join(result)


message_filename = "message.txt"
with open(message_filename, "r") as fp:
    message = fp.read()

primer = dict(list(zip(normalize_word(re.search(r"([a-z]{4}[A-Z]{3}){", message).group(1)), normalize_word("picoCTF"))))
primer = {
    # 'p': 'k',
    'n': 'q',
    **primer
}

message_words = message.split()[:-1]  # Exclude the flag
message_words = [normalize_word(w) for w in message_words]  # Remove anything that's not a letter from words

word_frequencies = wordfreq.get_frequency_dict("en")
word_frequencies_by_length = group_word_frequencies_by_length(word_frequencies)
message_words_by_length = group_word_frequencies_by_length(
    {k: (v / len(message_words)) for k, v in Counter(message_words).items()})

all_ciphertext_letters = set(map(str.lower, filter(str.isalpha, message)))
alphabets = []
plaintext = None
for l, words in message_words_by_length.items():
    for w, f in words:
        for ww, ff in word_frequencies_by_length[l][:400]:
            a = find_alphabet(w, ww, ff, primer, len(all_ciphertext_letters))
            if a:
                plaintext = decrypt(message, a)
                break
        if plaintext:
            break
    if plaintext:
        break

if not plaintext:
    print("Could not find plaintext. Closest 5 attempts were:")
    for a in sorted(alphabets, key=lambda a: (len(a), a.score), reverse=True)[:5]:
        print(decrypt(message, a))
else:
    flag = re.search(r"picoCTF\{.+}", plaintext).group(0)
    print(flag)
