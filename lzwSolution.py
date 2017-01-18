'''
Lempel-Ziv Welch decompressor (StarLeaf intern challenge)
by Myles Rankin ~ 2017
'''
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
    ''' converts 8-bit raw file contents to 12-bit tokens with 16-bit padding for odd code strings '''
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
    ''' applies LZW Decompression algorithm to compressed data (in integer format), then returns result'''
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
            dictionary[len(dictionary)] = w+w[0]
            w = dictionary[k]
        result += w
        if len(dictionary) == 4096:
            dictionary = generateAsciiDict(256)
    return result

if __name__ == "__main__":
    data = fileHandler("compressedfile3.z")
    compressed = bitConverter(data)
    decompressed = lzwDecompress(compressed)
    print(decompressed)
