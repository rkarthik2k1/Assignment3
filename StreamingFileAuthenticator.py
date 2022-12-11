import sys
import hashlib

debug = True
fileName = "Somefile"   # This is the initial file stream
fileNameWithHash = "SomefileAfterHashing" # This is the file after hashing is done

BLOCK_SIZE = 1024
blocks = []
hash0 = bytes(32)

# Reads a file in binary into list of blocks specified by
# blockSize
def ReadFileIntoBlocks(fileName, blockSize):
    # Open file in binary mode
    file = open(fileName, "rb")
    numBlocks = 0
    global blocks
    blocks = []
    # Read block by block into blocks
    while True:
        block = file.read(blockSize)
        if not block:
            break
        else:
            blocks.append(block)
            numBlocks += 1     
    DebugPrint(f'Total Number of Blocks = {numBlocks}')
    file.close()
    return numBlocks

# Compute SHA256 of data
def Sha256(data):
    m = hashlib.sha256()
    m.update(data)
    return m.digest()

# Find hash for whole file
def ComputeFileHash():

    DebugPrint("***** ComputeFileHash ***** ")    
    global hash0
    global blocks
    numBlocks = ReadFileIntoBlocks(fileName, BLOCK_SIZE)
    DebugPrint(numBlocks)
    dataForHash = []
    fileDataAfterHash = []
    
    # Find hash of each block starting with the last block.
    # Append hash of previous block to the next one.
    # So, fileDataiWithHash will actually contain data starting
    # with last block and end with first block
    # So while writing to file one needs to reverse it
    # One can also use a stack!!!
    for i in range(numBlocks):
        if i == 0:
            dataForHash = blocks[numBlocks-i-1]
        else:
            dataForHash = blocks[numBlocks-i-1]
            dataForHash = dataForHash + prevBlkHash

        DebugPrint(f'Block {numBlocks-i-1}: {dataForHash}')
        fileDataAfterHash.append(dataForHash)
        prevBlkHash = Sha256(dataForHash)
        hash0 = prevBlkHash.hex()
        DebugPrint(f'Hash for block {numBlocks-i-1}: {prevBlkHash.hex()}')

    DebugPrint(f'Final Hash0 : {hash0}')

    # Write data with hash but with reverse order so that block 0
    # with hash is first then block 1 with hash and so on till the
    # last block without any hash
    f = open(fileNameWithHash, "wb")
    for j in range(numBlocks):
        #f.write(fileDataAfterHash[numBlocks-j-1])
        f.write(fileDataAfterHash.pop())  
    f.close()
    DebugPrint("*************** ")    

# Validate hash for the file stream
def ValidateFileHash():

    DebugPrint("***** ValidateFileHash ***** ")    
    global hash0
    global blocks
    blocks = []
    numBlocks = ReadFileIntoBlocks(fileNameWithHash, BLOCK_SIZE + 32)
    DebugPrint(f"HASH is {hash0}")
    bRet = True
    if hash0 is None:
        DebugPrint("Invalid hash0")
        bRet = False
    else:
        hashToVerify = hash0
        # Compute hash for each block starting with the first block
        # Verify hash for each block till the last block
        for i in range(numBlocks):
            # Compute hash for the block
            hashBlock = (Sha256(blocks[i])).hex()
            DebugPrint(f"hash for block {i}: {hashBlock}")
            DebugPrint(f"hash to Verify: {hashToVerify}")
            # Compare this hash with hashToVerify
            if hashToVerify != hashBlock:
                bRet = False
                break

            # hash so far is good, store hash at end of this block into hashToVerify.
            # Hash is the last 32 bytes of the current block
            blockLen = len(blocks[i])
            hashToVerify = ((blocks[i])[blockLen-32:blockLen]).hex()
            DebugPrint(f'Block {i}: {blocks[i]}')
    ClearData()
    DebugPrint("*************** ")    
    return bRet

def ClearData():
    blocks = []
    hash0 = bytes(32)
    
def DebugPrint(s):
    if (debug == True):
        print(s)

def main():
    ComputeFileHash()
    if (ValidateFileHash()):
        print("File hash is valid")
    
