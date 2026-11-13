I created this repo to make it easier to understand how dumping LSA secret works and to rely less on tools like impacket and mimikatz.  

I split the process in to smaller pieces of code so that you can focus on learning one thing at a time. When using tools like secretsdump, it becomes hard to understand what goes on behind the scenes because everything is automated. When i was reading through the source code of secretsdump i wasn't able to understand it even though python is my main language. The main reason i struggled to read the source code of secretsdump was because not only did i have to learn the process of manually dumping LSA secrets, i also had to figure out what each part of the code did and whether it was relevant to the dumping process.  

I take a different approach from traditional tools and try to automate as little as possible in my code, so that you can actually learn and understand what it's doing but also create your own tools and scripts from it. It's just as easy for me to automate everything such as the extraction of the 4 class names required for the bootkey but that would just make it harder for someone trying to learn.  

The only prerequisite to run these scripts is downloading and adding openSSL to your path. I have only run these scripts in Windows but they should work on Linux. If anyone doesn't know how to setup openssl or have any other questions please open a Issue, i don't mind creating a full step by step. If you have created your own versions of these scripts in other programming languages or have other scripts, feel free to make a pull request so we can centralize them. 

This article saved me alot of time and most of the scripts that i made are based on it:  
https://hideandsec.sh/books/windows-sNL/page/from-boot-key-to-plaintext-how-windows-lsa-secrets-are-deciphered-from-the-registry/
