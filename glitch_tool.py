import argparse
import copy
import math
from os import path
import platform
import random
import re
import sys

def writeFile(fileByteList, fileNum, iteration, bytesTochange, seed):
    filename, extension = path.splitext(args.infile)
    filename = filename.split("\\")[-1] if platform.system == "Windows" else filename.split("/")[-1]
    outPath = f"{args.outdir}{filename}_m={args.mode}_b={bytesTochange}_s={seed}_n={fileNum}_i={iteration}{extension}"
    if (not args.quiet):
        print("Writing file to " + outPath)
    open(outPath, "wb").write(bytes(fileByteList))

def messWithFile(originalByteList, iterations, bytesToChange, repeatWidth, fileNum):
    newByteList = copy.copy(originalByteList)
    iteration = 1
    seed = args.seed or random.randrange(sys.maxsize)
    random.seed(seed)
    for i in range(iterations):
        iteration = i+1
        if (args.mode == "repeat"):
            newByteList = repeatBytes(newByteList, bytesToChange, repeatWidth)
        else:
            newByteList = transforms[args.mode](newByteList, bytesToChange)
        if (args.output_iterations > 0 and iteration%args.output_iterations == 0):
            writeFile(newByteList, fileNum, iteration, bytesToChange, seed)
    writeFile(newByteList, fileNum, iteration, bytesToChange, seed)
        
# Transforms

def changeBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = [random.randint(0, 255) for i in range(bytesToChange)]
    byteList[pos:pos+bytesToChange] = chunk
    return byteList

def reverseBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = byteList[pos:pos+bytesToChange][::-1]
    byteList[pos:pos+bytesToChange] = chunk
    return byteList

def repeatBytes(byteList, bytesToChange, repeatWidth):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = []
    for i in range(math.ceil(bytesToChange/repeatWidth)):
        chunk.extend(byteList[pos:pos+repeatWidth])
    byteList[pos:pos+bytesToChange] = chunk[:bytesToChange]
    return byteList

def removeBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    byteList[pos:pos+bytesToChange] = []
    return byteList

def zeroBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    byteList[pos:pos+bytesToChange] = [0] * bytesToChange
    return byteList

def insertBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList))
    chunk = [random.randint(0, 255) for i in range(bytesToChange)]
    byteList[pos:pos] = chunk
    return byteList

def replaceBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = byteList[pos:pos+bytesToChange]
    old = random.randint(0, 255)
    new = random.randint(0, 255)
    chunk = [new if b == old else b for b in chunk]
    byteList[pos:pos+bytesToChange] = chunk
    return byteList

def moveBytes(byteList, bytesToChange):
    pos = random.randint(0, len(byteList) - bytesToChange)
    chunk = byteList[pos:pos+bytesToChange]
    byteList[pos:pos+bytesToChange] = []
    newPos = random.randint(0, len(byteList))
    byteList[newPos:newPos] = chunk
    return byteList

def main():
    # Do stuff to arguments
    if (not args.infile):
        print("Error: No input file specified")
        return False
    if (not path.isfile(args.infile)):
        print("Error: Input file not found")
        return False
    if (not args.mode):
        print("Error: No mode specified")
        return False
    if (not (args.mode in transforms)):
        print("Error: Invalid mode")
        return False
    minChanges = 1
    maxChanges = 1
    if (args.changes and re.match(r"[0-9]+-[0-9]+", args.changes)):
        parts = args.changes.split("-")
        minChanges = int(parts[0])
        maxChanges = int(parts[1])
    elif (args.changes):
        minChanges = int(args.changes)
        maxChanges = int(args.changes)
    minBytes = 1
    maxBytes = 1
    if (args.bytes and re.match(r"[0-9]+-[0-9]+", args.bytes)):
        parts = args.bytes.split("-")
        minBytes = int(parts[0])
        maxBytes = int(parts[1])
    elif (args.bytes):
        minBytes = int(args.bytes)
        maxBytes = int(args.bytes)
    minRepeating = 1
    maxRepeating = 1
    if (args.repeat_width and re.match(r"[0-9]+-[0-9]+", args.repeat_width)):
        parts = args.repeat_width.split("-")
        minRepeating = int(parts[0])
        maxRepeating = int(parts[1])
    elif (args.repeat_width):
        minRepeating = int(args.repeat_width)
        maxRepeating = int(args.repeat_width)
    # Let the glitching commense!
    originalByteList = list(open(args.infile, "rb").read())
    for i in range(args.amount):
        iterations = random.randint(minChanges, maxChanges)
        bytesToChange = random.randint(minBytes, maxBytes)
        repeatWidth = random.randint(minRepeating, maxRepeating)
        messWithFile(originalByteList, iterations, bytesToChange, repeatWidth, i+1)
    if (not args.quiet):
        print("Finished writing files")


# Constants
transforms = {
    "change": changeBytes,
    "reverse": reverseBytes,
    "repeat": repeatBytes,
    "remove": removeBytes,
    "zero": zeroBytes,
    "insert": insertBytes,
    "replace": replaceBytes,
    "move": moveBytes
}

# Setup argparser
parser = argparse.ArgumentParser(description="Do terrible things to data.")
# Required arguments
parser.add_argument("-i", "--infile", help="Input file")
parser.add_argument("-m", "--mode", help="File change mode")
# Optional arguments
parser.add_argument("-o", "--outdir", default="./", help="Output folder")
parser.add_argument("-s", "--seed", type=int, help="Seed to use for random")
parser.add_argument("-a", "--amount", type=int, default=1, help="Amount of new files to create")
parser.add_argument("-c", "--changes", help="Amount of random changes. Can be in a range, like '1-10'.")
parser.add_argument("-b", "--bytes", help="Amount of bytes to change each change. Can be in a range, like '1-10'.")
parser.add_argument("-r", "--repeat-width", help="Amount of bytes to repeat. Can be in a range, like '1-10'.")
parser.add_argument("-q", "--quiet", default=False, action="store_true", help="Surpress logging")
parser.add_argument("--output-iterations", type=int, default=0, help="How many iterations between outputs")
args = parser.parse_args()

main()
