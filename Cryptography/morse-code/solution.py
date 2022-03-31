#!/usr/bin/env python3

from typing import List, Dict, Union
import wave

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()

character = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
code = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.',
        '--.-', '.-.', '...',
        '-', '..-', '...-', '.--', '-..-', '-.--', '--..', '-----', '.----', '..---', '...--', '....-', '.....',
        '-....', '--...', '---..', '----.']
encode_dict = dict(zip(character, code))
decode_dict = dict(zip(code, character))


def morse_codec(lst: Union[str, List[str]], d: Dict[str, str]):
    return [d[i] for i in lst]


def morse_encode(s: str) -> List[str]:
    return morse_codec(s, encode_dict)


def morse_decode(lst: List[str]) -> List[str]:
    return morse_codec(lst, decode_dict)


zero_frame = b'\x00\x00'
short_pulse_lower_threshold = 0.05
short_pulse_upper_threshold = 0.17
long_pulse_lower_threshold = 0.25
long_pulse_upper_threshold = 0.35
short_space_lower_threshold = 0.05
short_space_upper_threshold = 0.17
long_space_lower_threshold = 0.35
long_space_upper_threshold = 0.45
pause_lower_threshold = 0.7


def iterframes(fp):
    yield from (fp.readframes(1) for _ in range(fp.getnframes()))


def get_signal_periods(filename):
    with wave.open(filename, "rb") as fp:
        frame_rate = fp.getparams().framerate
        count = 0
        last = None
        for f in iterframes(fp):
            if last is not None:
                if (last == zero_frame) ^ (f == zero_frame):
                    yield last != zero_frame, count / frame_rate
                    count = 0
            last = f
            count += 1
        if last is not None:
            yield last != zero_frame, count / frame_rate


def filter_short_transitions(periods):
    last_pulse = None
    last_length = 0
    last_yielded = False
    for p, l in periods:
        if not (p and l < short_pulse_lower_threshold or (not p and l < short_space_lower_threshold)):
            if last_pulse is not None:
                if last_pulse and last_pulse == p:
                    last_length += l
                    last_yielded = False
                    continue
                else:
                    last_yielded = True
                    yield last_pulse, last_length
            last_pulse = p
            last_length = l
    if not last_yielded:
        yield last_pulse, last_length


def translate_periods_to_morse_symbols(periods):
    symbols = [""]
    for pulse, length in periods:
        if pulse:
            if length < short_pulse_upper_threshold:
                symbols[-1] += "."
            elif long_pulse_lower_threshold < length < long_pulse_upper_threshold:
                symbols[-1] += "-"
            else:
                print(f"Ignored pulse with length {length}")
        else:
            if long_space_lower_threshold < length < long_space_upper_threshold:
                symbols.append("")
            elif length > pause_lower_threshold:
                if not symbols[-1]:
                    symbols = symbols[:-1]
                if symbols:
                    yield symbols
                symbols = [""]
            elif length > short_space_upper_threshold:
                print(f"Ignored space with length {length}")
    if not symbols[-1]:
        symbols = symbols[:-1]
    if symbols:
        yield symbols


flag = "_".join(
    "".join(map(str.lower, morse_decode(c)))
    for c in
    translate_periods_to_morse_symbols(
        filter_short_transitions(
            get_signal_periods("morse_chal.wav")))
)

print(f"picoCTF{{{flag}}}")
