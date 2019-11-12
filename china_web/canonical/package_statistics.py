#!/usr/bin/env python3
import operator
import sys
import gzip
import requests

archs = ["amd64", "arm64", "armel", "armhf",
         "i386", "mips", "mips64el", "mipsel",
         "ppc64el", "s390x", "source", "udeb-amd64",
         "udeb-arm64", "udeb-armel", "udeb-armhf",
         "udeb-i386", "udeb-mips", "udeb-mips64el",
         "udeb-mipsel", "udeb-ppc64el", "udeb-s390x"]


def usage():
    print("usage: ./package_statistics.py [architecture]")
    print("acceptable architectures:")
    count = 0
    for arch in archs:
        count = count + 1
        if count % 3 == 0 or count == len(archs):
            print(arch)
        else:
            print(arch, end=" ")


# check if input arg include an architecture name
if len(sys.argv) != 2:
    print("Error, please input a correct architecture")
    usage()
    sys.exit(1)

# check if inputed architecture in archs list
inputArch = sys.argv[1]
if inputArch not in archs:
    print("Error, please input a correct architecture")
    usage()
    sys.exit(1)

# download contents index file
try:
    downFile = "Contents-" + inputArch + ".gz"
    urlStr = "http://ftp.uk.debian.org/debian/dists/stable/main/" + downFile
    r = requests.get(urlStr)
except Exception as e:
    print(e)
    sys.exit(1)

try:
    with open(downFile, 'wb') as output_file:
        output_file.write(r.content)
except Exception as e:
    print(e)
    sys.exit(1)

myDict = dict()
try:
    with gzip.open(downFile, "rt") as file:
        for line in file:
            str = line.rsplit(' ', 1)

            fileName = str[0]
            packageNamesInLine = str[len(str) - 1].strip('\n')

            # if coma exists in package name string, split every pakage name by coma
            packageName = packageNamesInLine.split(",")
            for packageNameTmp in packageName:
                # use dictionary to save pakage name and count occurrence
                if(packageNameTmp not in myDict):
                    myDict[packageNameTmp] = 1
                else:
                    myDict[packageNameTmp] = myDict[packageNameTmp] + 1

except Exception as e:
    print(e)
    sys.exit(1)

i = 0
# sort dictionary by value and print top 10 pakages
for key in sorted(myDict, key=myDict.get, reverse=True)[:10]:
    i = i+1
    print(f'{i}. ' + key, myDict[key])
