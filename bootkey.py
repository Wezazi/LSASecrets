
#The classes of these keys can be extracted by exporting them in the registry editor and opening the exported text file in the notepad
#The keys can be foound under HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa or HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Lsa
jd = input("enter the class name for the JD subkey: ").strip()
skew1 = input("enter the class name for the skew1 subkey: ").strip()
gbg = input("enter the class name for the GBG subkey: ").strip()
data = input("enter the class name for the Data subkey: ").strip()


joined = jd + skew1 + gbg + data

list = []
for i in range(0, len(joined), 2):
    list.append(joined[i:i+2])


permutationBox = [8, 5, 4, 2, 11, 9, 13, 3, 0, 6, 1, 12, 14, 10, 15, 7]
keyList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for index, value in enumerate(permutationBox):
    keyList[index] = list[value]
    
hexBootKey = "".join(keyList)

print(f"The boot key: {hexBootKey}")




