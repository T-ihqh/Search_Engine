# Team Member: Mingchen Huang, Qihang Huang, Junlong Lu
# UCI ID: 11211979,32514470,22111353
import json
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse
from urllib.parse import urldefrag

pagedict = {}
pagepointout = {}
pagepointin = {}
firstversionpagerank = {}
pagerankfilename = ['pagerank1.json']
docdict = {}
documentcounter = 0

def Invert_document_index():
    global pagedict, pagepointout, pagepointin
    with open("document_index.json" ,'r') as fp:
        documenttable = json.load(fp)
        for i in documenttable.keys():
            pagedict[documenttable[i]] = i
            pagepointin[i] = []



def run_all_files(filepath):
    global document_dict, documentcounter



    for root, ds, fs in os.walk(filepath):
        for f in fs:
            if ".json" in f:

                fullname = os.path.join(root, f)
                read_a_file(fullname)
                print(documentcounter)





def read_a_file(path):
    global pagedict, pagepointout, pagepointin, firstversionpagerank, docdict, documentcounter

    fp = open(path, "r")
    data = json.load(fp)
    document_link = data['url']
    url = urldefrag(document_link)[0]

    if url not in docdict.keys():
        soup = BeautifulSoup(data['content'], 'lxml')
        pagepointout[pagedict[url]] = 0
        firstversionpagerank[pagedict[url]] = 1
        for i in soup.findAll('a', href=True):
            rawurl = i['href']
            if is_valid(rawurl):
                link = urldefrag(rawurl)[0]
                if link in pagedict.keys():
                    pagepointout[pagedict[url]] += 1
                    pagepointin[pagedict[link]].append(pagedict[url])
        docdict[url] = 1
        documentcounter += 1
    else:
        pass



def savedata():
    global pagepointin, pagepointout, firstversionpagerank
    with open("pagepointout.json", 'w') as fp1:
        json.dump(pagepointout, fp1)
    print("pagepointout saved")

    with open("pagepointin.json", "w") as fp2:
        json.dump(pagepointin, fp2)
    print("pagepointin saved")

    with open("pagerank1.json","w") as fp3:
        json.dump(firstversionpagerank, fp3)
    print("pagerank1 saved")

    firstversionpagerank = {}


def iteration(filename):
    global pagepointin, pagepointout, pagerankfilename, pagedict
    fp = open(pagerankfilename[len(pagerankfilename)-1], 'r')
    previous = json.load(fp)

    newpagerank = {}

    for i in pagedict.keys():
        sum = 0
        for j in pagepointin[pagedict[i]]:
            sum += previous[j]/pagepointout[j]
        result = 0.85 * sum + 0.15
        newpagerank[pagedict[i]] = result

    fp.close()
    with open(filename, 'w') as fp2:
        json.dump(newpagerank, fp2)
    pagerankfilename.append(filename)
    print(filename, " saved")


def is_valid(url):
    try:
        parsed = urlparse(str(url))
        if parsed.scheme not in set(["http", "https"]):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|january|february|march|april|may|june|july"
            + r"|august|september|october|november|december"
            + r"|jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise


if __name__ == "__main__":
    Invert_document_index()
    run_all_files("/Users/Mr.Concise/Desktop/CS 121 Assignment3/DEV")
    savedata()
    for i in range(2,6):
        if i != 5:
            pagerankname = "pagerank"+str(i)+".json"
        else:
            pagerankname = "finalpagerank.jason"

        iteration(pagerankname)
