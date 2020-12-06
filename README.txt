# Team Member: Mingchen Huang, Qihang Huang, Junlong Lu
# UCI ID: 11211979,32514470,22111353

1. This search engine has four .py files, two html files, one static folder, one templates folder and one venv folder inside the code folder.
2. You only need to run invertedindex.py, PageRankMaker.py, GUI.py in order.
3. You need to change the directory path to a folder that contains all the json files for each url at the 255 line in invertedindex.py, the 135 line in PageRankMaker.py.
4. Open your terminal and reach to the code folder, use "pip install <package name>" to install all the package needed to run. The packages you need to install are: json, bs4, nlkt, collection, os, psutil, math, urllib3, re, flask.
5. Make sure that your python version is equal or above 3.6.
6. Use command lines "python invertedindex.py" on terminal, it will create multiple files and do not change them.
7. When the last one is finished running. Use command lines "python PageRankMaker.py" on terminal.
8. When the last one is finished running. Use command lines "python GUI.py" on terminal.
9. After running the GUI.py, multiple information are displayed, find the phrase "Running on " and copy the web address after the phrase, then paste the address on your browser url input field, next press enter. You will see a search engine shows up.
10. You can enter your query in the blank input field, and press search button. The webpage will direct to a new page, and the new page shows response time for this query and the top 10 ranked url. If you want to search again, press the back button, the page will go back to the searching interface.
