import subprocess

#keep in mind that you need to open registry editor as system to inspect the security hive, psexec can hel you do this: .\PsExec.exe -accepteula -s -i regedit.exe

bootKey = input("Enter the bootkey value: ").strip()
bootKey = bootKey.replace(" ", "")

polekList = input("Enter the PolekList Data Value: ").strip()
polekList = polekList.replace(" ", "")

groupByByte = []
for i in range(0, len(polekList), 2): 
    groupByByte.append(polekList[i:i+2])
    

version = "".join(groupByByte[0:4])
encKeyId = "".join(groupByByte[4:20])
encAlgorithm = "".join(groupByByte[20:24])
flags = "".join(groupByByte[24:28])
salt = "".join(groupByByte[28:60])
encryptedPayload = "".join(groupByByte[60:])

salt = salt * 1000

derivedKey = subprocess.run(
    ["openssl", "dgst", "-sha256", "-binary"],
    input=bytes.fromhex(bootKey) + bytes.fromhex(salt),  
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
    



clearSecretSize = groupByByte[0:4]
clearUnk0 = groupByByte[4:8]
clearUnk1 = groupByByte[8:12] 
clearUnk2 = groupByByte[12:16] 

clearSecretSize = bytes.fromhex("".join(clearSecretSize))
clearSecretSize = int.from_bytes(clearSecretSize, byteorder="little") 


keys = groupByByte[16:16 + clearSecretSize] #all bytes that aren't within this range are discarded



keysUnkType0 = keys[0:4] 
keysCurrentKeyId = keys[4:20] 
keysUnkType1 = keys[20:24] 
keysNbKeys = keys[24:28]


keysNbKeys = bytes.fromhex("".join(keysNbKeys))
keysNbKeys = int.from_bytes(keysNbKeys, byteorder="little")



keyId = keys[28:44] 
keyType = keys[44:48] 
keySize = keys[48:52] 

keySize = bytes.fromhex("".join(keySize))
keySize = int.from_bytes(keySize, byteorder="little")

#LSA Encrption key
lsaKey = "".join(keys[52:52+keySize])
print(f"LSA Key: {lsaKey}")


