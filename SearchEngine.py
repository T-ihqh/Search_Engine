# Team Member: Mingchen Huang, Qihang Huang, Junlong Lu
# UCI ID: 11211979,32514470,22111353

import json
import time
from nltk.stem import PorterStemmer
import math

global data_fp
pagerank = {}
indextable = {}
query_token_info = {}
result = []
response_time = 0.0


def parse_query(query):
    query_list = query.split(" ")
    ps = PorterStemmer()
    for i in range(len(query_list)):
        query_list[i] = ps.stem(query_list[i])
    return query_list


def get_term_posting(term):
    global data_fp, indextable
    data_fp.seek(indextable[term]['position'])
    content = data_fp.readline()
    posting = json.loads(content)
    for i in posting.keys():
        key = i
    return posting[key]


def get_docID_from_inverted_index(query_list):
    global data_fp, query_token_info, indextable

    highidf_list = []

    querylength = 0
    bottomline = 0.8

    old_query_list = query_list.copy()
    query_list.clear()
    query_list = []

    keys = indextable.keys()
    print("query list: ", old_query_list)
    for term in old_query_list:
        if term in keys:
            query_list.append(term)

    numofterm = len(query_list)
    if numofterm == 0:
        return []

    # when the whole query only contain one word
    if numofterm == 1:
        term_posting = get_term_posting(query_list[0])
        return sorted(term_posting.items(), key=lambda x: x[1], reverse=True)

    # only count high idf terms
    while len(highidf_list) / len(query_list) < 0.6:
        highidf_list = []
        querylength = 0
        for i in query_list:
            if indextable[i]["idf"] > bottomline:
                querylength += math.pow(indextable[i]["idf"], 2)
                highidf_list.append(i)
        # print("query: ", highidf_list)
        bottomline -= 0.1

    querylength = math.sqrt(querylength)

    querydict = {}

    for i in highidf_list:
        querydict[i] = round(indextable[i]["idf"] / querylength, 4)

    docdict = {}

    for i in highidf_list:
        term_posting = get_term_posting(i)
        for j in term_posting.keys():
            if j not in docdict:
                docdict[j] = {}
                docdict[j][i] = term_posting[j]
                docdict[j][0] = math.pow(term_posting[j], 2)
            else:
                docdict[j][i] = term_posting[j]
                docdict[j][0] += math.pow(term_posting[j], 2)

    for i in docdict.keys():
        for j in docdict[i].keys():
            if type(j) == str:
                docdict[i][j] = round(docdict[i][j] / math.sqrt(docdict[i][0]), 4)

    finaldict = {}

    for i in docdict.keys():
        finaldict[i] = 0
        for j in docdict[i].keys():
            if type(j) == str:
                finaldict[i] += docdict[i][j] * querydict[j]

    for i in finaldict.keys():
        finaldict[i] += pagerank[i]

    return sorted(finaldict.items(), key=lambda x: x[1], reverse=True)



#def interface():
def interface(query):
    global indextable, data_fp, pagerank, result, response_time
    data_fp = open("FinalIndex.txt", "r")

    pagerank_fp = open("finalpagerank.jason", 'r')
    pagerank = json.load(pagerank_fp)

    document_fp = open("document_index.json", "r")
    document_id = json.load(document_fp)

    indextable_fp = open("IndexofIndex.json", "r")
    indextable = json.load(indextable_fp)

    start = time.time()

    query_list = parse_query(query)
    # print("after stemming: ", query_list)

    final_result = get_docID_from_inverted_index(query_list)

    end = time.time()
    response_time = (end - start)*1000
    print("it take ", response_time)

    count = 0
    result.clear()
    for i in final_result:
        print(document_id[i[0]], ": ", i[1])
        count += 1
        result.append(document_id[i[0]])
        if count == 10:
            break

    print("result: ", result)


    data_fp.close()
    document_fp.close()

    if len(result) == 0:
        result.append("No result due to invalid query term. Check your query.")

    return [response_time, result]

    '''
    while True:
        query = input("\n\n>>>>>>: ")
        if query == "exit":
            break

        start = time.time()

        query_list = parse_query(query)
        # print("after stemming: ", query_list)

        final_result = get_docID_from_inverted_index(query_list)

        end = time.time()
        responsetime = end - start
        print("it take ", responsetime)

        count = 0
        for i in final_result:
            print(document_id[i[0]], ": ", i[1])
            count += 1
            result.append(document_id[i[0]])
            if count == 10:
                break

        print("result: ", result)

    data_fp.close()
    document_fp.close()
    # final_result = calculate_combined_frequency(query_list, intersect_doc_id)
    # print("final result keys: \n", final_result)
'''

'''
        if len(final_result) < 5:
            number_print_url = len(final_result)
        else:
            number_print_url = 5





        for i in range(0, number_print_url):
            print("-->> ", str(document_id[str(final_result[i])]))
'''

if __name__ == "__main__":
    interface("machine learning")

'''
    #start = time.time()
    fp = open("inverted_index.json", "r")
    data = json.load(fp)
    start = time.time()
    temp = data["class"]
    time.sleep(1)
    end = time.time()
    print(f"Runtime of the program is {end - start}")
    print()
    print("class posting size: ", data["class"][str(0)])
'''
