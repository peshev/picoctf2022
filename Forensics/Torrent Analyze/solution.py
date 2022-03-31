#!/usr/bin/env python3

import binascii
import libtorrent as lt
import time
import tempfile
import subprocess
import json

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()


def get_bt_info_hash_filename(info_hash, timeout=20):
    print(info_hash, end="", flush=True)
    params = lt.parse_magnet_uri(f"magnet:?xt=urn:btih:{info_hash}")
    params.save_path = tempfile.mkdtemp()
    handle = ses.add_torrent(params)
    handle.pause()
    while not handle.status().has_metadata and timeout:
        time.sleep(1)
        timeout -= 1
    if timeout:
        filename = handle.torrent_file().name()
        print(" " + filename)
        return filename
    else:
        print(" Timed out")


def tshark_get_statistics_payload(tshark_output):
    started = False
    result = []
    lines = tshark_output.split("\n")
    for line in lines:
        if started:
            result.append(line)
            if line.startswith("=" * 20):
                return result
        else:
            if line.startswith("=" * 20):
                started = True
    if result:
        return result


def parse_tshark_bt_dht_output(tshark_output):
    """
    Parsing the output of tshark properly is quite a chore, since it generates JSON with duplicate keys
    Also, the bt_dht dissector outputs the structure in an appalingly poor way
    So, we don't bother actually parsing the JSON
    """
    info_hash = False
    for line in tshark_output.split("\n"):
        if "info_hash" in line:
            info_hash = True
        elif info_hash:
            yield line.split(":")[1].strip().strip('"')
            info_hash = False


def parse_tshark_udp_payload(tshark_output):
    """
    An cleaner alternative to parse_tshark_bt_dht_output()
    This is a much nicer way to parse the DHT structure, since it outputs it the way it's meant to be presented
    """
    yield from (
        binascii.hexlify(lt.bdecode(binascii.unhexlify("".join(
            packet["_source"]["layers"]["udp"]["udp.payload"].split(":"))))[b"a"][b"info_hash"]).decode()
        for packet in
        json.loads(tshark_output)
    )


def call_tshark(args):
    return subprocess.check_output(["tshark", "-r", "torrent.pcap"] + args).decode()


top_udp_port = tshark_get_statistics_payload(call_tshark(["-z", "endpoints,udp"]))[3].split()[1]
tshark_output = call_tshark(
    ["-T", "json", "-d", f"udp.port=={top_udp_port},bt-dht", 'bt-dht.bencoded.string == "info_hash"'])

ses = lt.session()
filename = next(iter(
    filter(lambda x: x and x.endswith(".iso"),
           map(get_bt_info_hash_filename,
               set(parse_tshark_udp_payload(tshark_output))))), None)
if filename:
    print(f"picoCTF{{{filename}}}")
else:
    print("No filename found")
