'''
Lempel-Ziv Welch decompressor (StarLeaf intern challenge)
by Myles Rankin ~ 2017
'''
import codecs, re

def fileHandler(file):
    ''' handles file, outputs data '''
    file = open(file, "rb")
    data = file.read()
    file.close()
    return data

def generateAsciiDict(dictSize):
    ''' creates dictionary of ascii values '''
    dictionary = {}
    for i in range(dictSize):
        dictionary[i] = chr(i)
    return dictionary

def bitConverter(bitstring):
    ''' converts raw file contents to 12-bit tokens with 16-bit padding for odd code strings '''
    raw = []
    for i in bitstring:
        b = bin(i).replace("0b","")
        raw.append("0"*(8-len(b))+b)
    if len(raw) %2 != 0:
        raw[-1] = "0"*(16-len(raw[-1]))+raw[-1]
    converted = []
    for i in range(1,len(raw)-1,3):
        if len(raw[i]) != 16:
            b1 = raw[i-1]+raw[i][:4]
            b2 = raw[i][4:]+raw[i+1]
            converted.append(int(b1,2))
            converted.append(int(b2,2))
    return converted

def lzwDecompress(compressed):
    dictionary = generateAsciiDict(256)
    k = compressed.pop(0)
    w = dictionary[k]
    result = w
    while(len(compressed)>0):
        k = compressed.pop(0)
        if k in dictionary:
            temp = w
            w = dictionary[k]
            dictionary[len(dictionary)] = temp+w[0]
        else:
            dictionary[len(dictionary)] = w + w[0]
            w = dictionary[k]
        result += w
        if len(dictionary) == 4096:
            dictionary = generateAsciiDict(256)
    print(result)
    return result
    

b = bitConverter(fileHandler("compressedfile4.z"))
lzwDecompress(b)



''' other things
binary = re.finditer('.{%s}'%chunksize, raw)

old:

def bitConverter(bitString):
    binary = bin(int(codecs.encode(bitString,"hex_codec"),16))
    binary = binary.replace("b","")
    if len(binary)%12 != 0:
        binary = split(binary,12)
        binary[-1] = "0"*(16-len(binary[-1]))+binary[-1]
    else:
        print("No padding needed")
        binary = split(binary,12)
    print(binary)
    return binary

def split(string,n):
    result = []
    counter = 0
    while string != "":
        if counter == n:
            result.append(string[:n])
            string = string[n:]
            counter = 0
        else:
            counter += 1
    return result

    for i in range(0,len(compressed)-1):
        char = chr(int(compressed[i],2))
        w = char + chr(int(compressed[i-1],2))
        print(char)
        if char in _ascii.values():
            result += char
            prev = char
        elif compressed[i] != 0 and w not in _ascii.values():
            print(w)
            n = max(_ascii, key=_ascii.get)+1
            _ascii[n] = w

            
'''

#print(len(b)%12)
