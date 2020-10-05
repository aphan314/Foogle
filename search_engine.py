import nltk
import json
from bs4 import BeautifulSoup
from collections import defaultdict
import pymongo
import create_tokens
import math
import re
import os
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def set_pos(penntag):
    morphy_tag = {'NN':'n', 'JJ':'a',
                  'VB':'v', 'RB':'r'}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return 'n'

def tokenize(data):
    tokens = nltk.word_tokenize(data)
    tokens = create_tokens.tokenizer(tokens)
    return tokens


def read_files(json_dict):
    main_dict = defaultdict(dict)
    wl = WordNetLemmatizer()
    stopwords_set = set(stopwords.words('english'))

    path = os.environ.get('WEBPAGES_RAW')

    for i in json_dict.keys():
        file = path + i
        try:
            html_doc = open(file, encoding="utf8").read()
        except:
            print(file)
        soup = BeautifulSoup(html_doc, 'lxml')
        for script in soup(["script", "style"]):
            script.decompose()
        t_data = tokenize(soup.get_text())
        for num, word in enumerate(t_data):
            if word not in stopwords_set:
                lem_word = wl.lemmatize(word.lower(), pos=set_pos(pos_tag([word])[0][1]))
                if i not in main_dict[lem_word]:
                    d = {"index": [num], "count": 1, "tfidf": 0}
                    main_dict[lem_word][i] = d
                else:
                    main_dict[lem_word][i]["count"] += 1
    return main_dict


def get_tfidf(main_dict, json_dict):
    N = len(json_dict.keys())

    for token, d in main_dict.items():
        df = len(d.keys())
        for f, f_data in d.items():
            f_data["tfidf"] = (1 + math.log10(f_data["count"])) * (math.log10(N/df))
    return main_dict


def put_database(stat_dict):
    client = pymongo.MongoClient('127.0.0.1', port=27017)
    db = client["test-database"]
    my_collection = db["test-collection-1"]

    return my_collection

def get_database():
    client = pymongo.MongoClient('127.0.0.1', port=27017)
    db = client["test-database"]
    my_collection = db["test-collection-1"]

    return my_collection


def search(json_dict, db, txt):
    tfidf_dict = defaultdict(list)
    token_dict = defaultdict(set)
    for i in txt:
        for j in db.find({i: {"$exists": True}}):
            for d in j[i]:
                tfidf_dict[d].append(j[i][d]['tfidf'])
                token_dict[d].add(i)

    avg_dict = defaultdict(int)
    for f in tfidf_dict.keys():
        avg_dict[f] = sum(tfidf_dict[f]) / len(tfidf_dict[f])

    sorted_path = sorted(avg_dict.items(), key=lambda kv: -kv[1])

    urls_list = []
    if len(sorted_path) > 20:
        for i in range(0, 20):
            path = sorted_path[i][0]
            token_set = token_dict[path]
            sentences = set()
            for j in token_set:
                sentences.add(description(path, j))
            urls_list.append((json_dict[path], sentences))
    else:
        for i in sorted_path:
            path = sorted_path[i][0]
            token_set = token_dict[path]
            sentences = set()
            for j in token_set:
                sentences.add(description(path, j))
            urls_list.append((json_dict[path], sentences))
    return urls_list


def description(doc, token):
    path = os.environ.get('WEBPAGES_RAW')

    file = path + doc
    html_doc = open(file).read()
    soup = BeautifulSoup(html_doc, 'lxml')
    for script in soup(["script", "style"]):
        script.decompose()
    data = soup.get_text()
    pattern = r"([\w\s]*?" + re.escape(token) + r"[\w\s]*)"
    match = re.search(pattern, data, re.IGNORECASE)
    sentence = match.group(0)
    return sentence


def lem_words(words):
    wl = WordNetLemmatizer()
    result = []
    for word in words:
        result.append(wl.lemmatize(word.lower(), pos=set_pos(pos_tag([word])[0][1])))
    return result


def main(query):
    bookkeeping = os.environ.get('BOOK_KEEPING')
    json_file = open(bookkeeping)

    json_dict = json.load(json_file)

    db_collection = get_database()

    s = lem_words(query)
    urls = search(json_dict, db_collection, s)

    return urls
