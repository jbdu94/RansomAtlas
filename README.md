# RansomAtlas


## Purpose
Map ransomwares, malwares, and find interesting relationships between them.
The idea is not only to get the TTPs but also try to obtain as much information as possible, about targeted domains, targeted countries, commands, api calls, libraries used....

## Disclaimer
I spent hours building this database, using online resources, so please give credit to this work before you reuse it. 
This database, and codes, are not linked anyhow with my employer.
It may contain some errors, or duplicates, although I do my best to regularly clean the file for duplicates.
Also you have conflicting sources, some source says this, while other sources say that. In this case, I see which is the most reliable.
When multiple reliable sources say different things, I merge them


## How to use

### Use the web version to search keywords
If you want to find which ransomware, malware, threat actor is using a special technique (eg T1105) or a tool (eg Citrix) or a vulnerability (eg CVE-2025-xxxx) the web version can provide this, and it has the advantage to not mess up with the dataset


### Use the code if you want to use Machine Learning on latest dataset
Obtain the latest Excel available
Install and run the codes: 
<br><br>
python3 Apriori.py<br>
python3 MonteCarlo.py<br><br>




