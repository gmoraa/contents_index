#!/usr/bin/python3
import argparse
from collections import Counter
import gzip
import os
import sys
import wget

# Variables
URL='http://ftp.uk.debian.org/debian/dists/stable/main/Contents-'

def initializeParser():
    parser = argparse.ArgumentParser(description = "Usage ./package_statistics.py <architecture>")
    parser.add_argument('architecture', type=str, help='input the architecture name like ./package_statistics.py arm64 or ./package_statistics.py i386')
    args = parser.parse_args()
    return args.architecture

def downloadContents():
    fullURL = URL + initializeParser() + '.gz'
    try:
        wget.download(fullURL, './contents.gz')
    except NameError:
        print("Invalid architecture.")
    except:
        print("The valid options are 'arm64','amd64','armel','armhf','i386','mips','mips64el','mipsel','ppc64el','s390x' and 'source'.")
        sys.exit(1)

def fileManipulation():
    with gzip.open('contents.gz', 'rb') as file:
        f = [x.decode('utf8').strip() for x in file.readlines()]
        f_clean = " ".join(f).split()
        f_counter = Counter(f_clean[1::2])
        f_sorted = sorted(f_counter.items(), key=lambda x: x[1], reverse=True)
    os.remove("contents.gz")
    return f_sorted

def outputResult():
    file = fileManipulation()
    print("")
    for i in file[0:10]:
        print(i[0], i[1])

if __name__ == "__main__":
    initializeParser()
    downloadContents()
    outputResult()