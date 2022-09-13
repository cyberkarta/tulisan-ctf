#!/usr/bin/env python3
file = "enc"
flag = ""


with open(file, "r") as f:
    strings = f.read()
    for i in range(len(strings)):
        ordinal = ord(strings[i]) >> 8 # finding ordinal of these characters
        ordinal2 = bin(ord(strings[i]))[9:]
        print(ordinal2)
        ordinal2 = int(ordinal2, 2)
        flag += chr(ordinal) + chr(ordinal2)

print(flag)
