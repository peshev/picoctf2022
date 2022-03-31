from urllib.request import urlretrieve
from urllib.parse import urlparse
import os.path
import hashlib

BUFSIZE = 16 * 1024


def file_hash(filename, hash_algorithm=hashlib.sha256, buffer_size=BUFSIZE):
    hasher = hash_algorithm()
    with open(filename, "rb") as fp:
        while True:
            read = fp.read(buffer_size)
            hasher.update(read)
            if len(read) < buffer_size:
                break
    return hasher.hexdigest()


def download_artifacts():
    files_to_skip = set()
    checksums = {}
    if os.path.isfile("SHA256SUMS"):
        with open("SHA256SUMS") as fp:
            checksums = {
                file: checksum
                for checksum, file in
                [
                    line.strip().split(maxsplit=1)
                    for line in
                    fp.readlines()
                ]
            }
        for filename, checksum in checksums.items():
            if os.path.isfile(filename):
                if file_hash(filename) == checksum:
                    files_to_skip.add(filename)

    new_checksums = {}
    with open("FILES") as fp:
        for url in filter(None, map(str.strip, fp.readlines())):
            filename = urlparse(url).path.split("/")[-1]
            if filename not in files_to_skip:
                urlretrieve(url, filename)
                checksum = file_hash(filename)
                if filename in checksums:
                    assert checksum == checksums[filename]
                else:
                    new_checksums[filename] = checksum

    if new_checksums:
        with open("SHA256SUMS", "a") as fp:
            for filename, checksum in new_checksums.items():
                fp.write(f"{checksum} {filename}\n")
