import subprocess

lsaKey = input("Enter the LSAKey value: ").strip()
lsaKey = lsaKey.replace(" ", "")

currVal = input("Enter the currVal of DPAPI_SYSTEM: ")
currVal = currVal.replace(" ", "")

groupByByte = []
for i in range(0, len(currVal), 2): 
    groupByByte.append(currVal[i:i+2])
    
version = "".join(groupByByte[0:4])
encKeyId = "".join(groupByByte[4:20])
encAlgorithm = "".join(groupByByte[20:24])
flags = "".join(groupByByte[24:28])
salt = "".join(groupByByte[28:60])
encryptedPayload = "".join(groupByByte[60:])

salt = salt * 1000

derivedKey = subprocess.run(
    ["openssl", "dgst", "-sha256", "-binary"],
    input=bytes.fromhex(lsaKey) + bytes.fromhex(salt),
    capture_output=True,
).stdout

derivedKeyHex = derivedKey.hex()

decryptedPayload = subprocess.run(
    ["openssl", "enc", "-aes-256-ecb", "-d", "-K", derivedKeyHex, "-nopad"],
    input=bytes.fromhex(encryptedPayload),
    capture_output=True,
).stdout

groupByByte = []
decryptedPayloadHex = decryptedPayload.hex()

for i in range(0, len(decryptedPayloadHex), 2): 
    groupByByte.append(decryptedPayloadHex[i:i+2])
    

secretLength = groupByByte[0:4]
secretLength = bytes.fromhex("".join(secretLength))
secretLength = int.from_bytes(secretLength, byteorder="little")
reserved = groupByByte[4:16]

secretData = groupByByte[16:16 + secretLength]
#dpapiSystem = "".join(secretData)

#the source didn't specify how to parse the dpapi keys so i had to figure it out myself by comparing output to secretsdump

#each key is 20 bytes each. The first 4 bytes (Index 0-3) of the secretData is a garbage value of 00 00 00 01. Index 4 - 23 (20 bytes) is the machine dpapi key. Index 24-43 (20 bytes) is the user dpapi key
dpapiMachineKey = "".join(secretData[4:24])
dpapiUserKey = "".join(secretData[24:44])

print(f"\ndpapi_machinekey: {dpapiMachineKey}") 
print(f"\ndpapi_userkey: {dpapiUserKey}")
