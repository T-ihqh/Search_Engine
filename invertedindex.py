# Team Member: Mingchen Huang, Qihang Huang, Junlong Lu
# UCI ID: 11211979,32514470,22111353
import json
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from collections import Counter
import os
import psutil
import math
from urllib.parse import urldefrag

document_dict = {}
document_link = ""
InvertedIndexlist = {}
storefileid = 1
mergedfileid = 1
indexofindex = {}
filenamelist = []
mergedfilelist = []
documentcounter = 0
test_counter = 0
url_dict = {}

class Posting:
    def __init__(self, id, count):
        self.docID = id
        self.frequency = count


def run_all_files(filepath):
    global document_dict, document_link, InvertedIndexlist, counter, documentcounter, test_counter

    inverted_index_file_number = 0
    json_file_number = 0

    for root, ds, fs in os.walk(filepath):
        for f in fs:
            if ".json" in f:
                json_file_number += 1
                fullname = os.path.join(root, f)
                read_a_file(fullname, documentcounter)

                #if psutil.virtual_memory().percent > 45:
                if test_counter > 20000:
                    test_counter = 0
                    print(psutil.virtual_memory().percent)
                    print("saved: ",storefileid)
                    storeIndexlist()




def read_a_file(path, pageidcount):
    global document_link, InvertedIndexlist, documentcounter, url_dict, document_dict, test_counter
    tokenizer = RegexpTokenizer(r'[0-9a-zA-Z]+')

    fp = open(path, "r")
    data = json.load(fp)
    document_link = data['url']
    url = urldefrag(document_link)[0]
    if url in url_dict.keys():
        pass
    else:
        url_dict[url] = 1
        document_dict[documentcounter] = url
        print(documentcounter)
        soup = BeautifulSoup(data['content'], 'lxml')
        content = soup.getText()
        tokenlist = tokenizer.tokenize(content)




        ps = PorterStemmer()
        for i in range(len(tokenlist)):
            # tokenlist[i] = tokenlist[i].lower()
            tokenlist[i] = ps.stem(tokenlist[i])

        counts = Counter(tokenlist)

        important_text = ["b", "strong", "h1", "h2", "h3"]
        for element in important_text:
            for i in soup.find_all(element):
                important_text_tokenlist = tokenizer.tokenize(i.get_text())
                for j in range(len(important_text_tokenlist)):
                    important_text_tokenlist[j] = ps.stem(important_text_tokenlist[j])
                important_text_counts = Counter(important_text_tokenlist)
                for key in important_text_counts.keys():
                    counts[key] += important_text_counts[key]*10




        # print(counts)
        for i in counts.keys():
            if i not in InvertedIndexlist:
                InvertedIndexlist[i] = {}
                # InvertedIndexlist[i].append(Posting(pageidcount, counts[i]))
                InvertedIndexlist[i][pageidcount] = round(1 + math.log10(counts[i]), 4)
            else:
                # InvertedIndexlist[i].append(Posting(pageidcount, counts[i]))
                InvertedIndexlist[i][pageidcount] = round(1 + math.log10(counts[i]), 4)
        fp.close()
        documentcounter += 1
        test_counter += 1


# write inverted index into a jason file
def output_content_file():
    global InvertedIndexlist, document_dict
    with open("document_index.json", 'w') as document_index_file:
        json.dump(document_dict, document_index_file)

    storeIndexlist()


def storeIndexlist():
    global InvertedIndexlist, storefileid, filenamelist
    filename = "inverted_index" + str(storefileid) + ".txt"
    with open(filename, 'w') as outfile:
        for i in sorted(InvertedIndexlist.keys()):
            newdict = {}
            newdict[i] = InvertedIndexlist[i]
            json.dump(newdict, outfile)
            outfile.write("\n")

    filenamelist.append(filename)

    InvertedIndexlist = {}
    storefileid += 1


def mergeallIndex():
    global filenamelist, mergedfilelist

    for i in range(len(filenamelist)):
        if i == 0:
            pass
        elif i == 1:
            merge(filenamelist[0], filenamelist[1], False)
        elif i == len(filenamelist) - 1:
            merge(mergedfilelist[len(mergedfilelist) - 1], filenamelist[i], True)
        else:
            merge(mergedfilelist[len(mergedfilelist) - 1], filenamelist[i], False)


def merge(filename1, filename2, finalmerge):
    global mergedfileid, mergedfilelist, indexofindex, document_dict

    if finalmerge is True:
        mergedfilename = "FinalIndex.txt"
    else:
        mergedfilename = "MergedIndex" + str(mergedfileid) + ".txt"

    fp1 = open(filename1, 'r')
    fp2 = open(filename2, 'r')
    fp3 = open(mergedfilename, 'w')

    content1 = fp1.readline()
    content2 = fp2.readline()

    while content1 != "" and content2 != "":
        dict1 = json.loads(content1)
        dict2 = json.loads(content2)

        for i in dict1.keys():
            key1 = i

        for i in dict2.keys():
            key2 = i

        list1 = [key1, key2]
        list2 = sorted(list1)

        if key1 == key2:
            for i in dict2[key2].keys():
                dict1[key1][i] = dict2[key2][i]

            if finalmerge is True:
                indexofindex[key1] = {}
                indexofindex[key1]["position"] = fp3.tell()
                indexofindex[key1]["idf"] = round(math.log10(len(document_dict.keys())/len(dict1[key1].keys())), 4)

            json.dump(dict1, fp3)
            fp3.write("\n")
            content1 = fp1.readline()
            content2 = fp2.readline()

        else:
            if list2[0] == key1:

                if finalmerge is True:
                    indexofindex[key1] = {}
                    indexofindex[key1]["position"] = fp3.tell()
                    indexofindex[key1]["idf"] = round(math.log10(len(document_dict.keys())/len(dict1[key1].keys())), 4)

                json.dump(dict1, fp3)
                fp3.write("\n")
                content1 = fp1.readline()

            else:

                if finalmerge is True:
                    indexofindex[key2] = {}
                    indexofindex[key2]["position"] = fp3.tell()
                    indexofindex[key2]["idf"] = round(math.log10(len(document_dict.keys())/len(dict2[key2].keys())), 4)

                json.dump(dict2, fp3)
                fp3.write("\n")
                content2 = fp2.readline()

    if content1 == "" and content2 != "":
        while content2 != "":
            dict2 = json.loads(content2)
            for i in dict2.keys(): #can put in the if statement for finalmerge below
                key2 = i

            if finalmerge is True:
                indexofindex[key2] = {}
                indexofindex[key2]["position"] = fp3.tell()
                indexofindex[key2]["idf"] = round(math.log10(len(document_dict.keys())/len(dict2[key2].keys())), 4)

            json.dump(dict2, fp3)
            fp3.write("\n")
            content2 = fp2.readline()

    elif content2 == "" and content1 != "":
        while content1 != "":
            dict1 = json.loads(content1)

            for i in dict1.keys():
                key1 = i

            if finalmerge is True:
                indexofindex[key1] = {}
                indexofindex[key1]["position"] = fp3.tell()
                indexofindex[key1]["idf"] = round(math.log10(len(document_dict.keys())/len(dict1[key1].keys())), 4)

            json.dump(dict1, fp3)
            fp3.write("\n")
            content1 = fp1.readline()

    mergedfilelist.append(mergedfilename)
    mergedfileid += 1

    if finalmerge is True:
        with open("IndexofIndex.json", 'w') as fp4:
            json.dump(indexofindex, fp4)

    fp1.close()
    fp2.close()
    fp3.close()


if __name__ == "__main__":
    run_all_files("/Users/Mr.Concise/Desktop/CS 121 Assignment3/DEV")
    print("\nafter run all files \nbefore output content file \n")
    output_content_file()
    print("\nafter output content file \nbefore merge all index \n")
    mergeallIndex()


