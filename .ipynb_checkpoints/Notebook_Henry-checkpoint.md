# Notebook

### 2023-01-31
Commit: search_process.py   
https://github.com/henryluo-lyh/534Project_FootballAPI/commit/5a84bfd1e4ea338ab17aae0963888f6c212f96e6   
Finished data wrangling and search functions in the search_process module.   
This Module reads the csv produced by the extract module, wrangle it and allow user to search two players by name   
from the dataset. The search result is returned as a data frame, which is then pivoted longer, making it visualization ready.    

Deleted the draft "visualizer.ipynb" which contains all the functions of "search_process.py" and simple plot function to check if the data frame is visualization ready.   

Commit: code_of_conduct.txt   
https://github.com/henryluo-lyh/534Project_FootballAPI/commit/740ce5a9195500c64a81b252fa9fc7ed65b5ea77   
Added code_of_conduct document   

### 2023-02-01   
Commit: search_process.py   
https://github.com/henryluo-lyh/534Project_FootballAPI/commit/96f01b5d38cf6b1394a41d75cc0fb5b52eb423cc   
Added comments to the functions   

### 2023-02-08
Commit: search_process.py   
https://github.com/henryluo-lyh/534Project_FootballAPI/commit/e43ba8570de260f86d4b3209c1ea5ae5734e9cc6   
Deleted all columns containing url links from the data frame.   
The url links for the same player is sometimes different from different request for the same data, creating strange duplicates of player stats. Deleted the columns with url to prevent this problem from occuring, since all the urls are for pictures such as player photo, league logo, etc, which are not important for the purpose of this project.