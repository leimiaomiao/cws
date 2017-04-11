import glob
import json
import xml.etree.ElementTree as ET
import os
from config.constant import CORPUS_JSON_PATH


def extract_full_text(doc):
    try:
        root = ET.fromstring(doc)
        info = root.find(".//QW[@nameCN='全文']")
        if info is not None:
            main_info = info.get("value")
            return main_info
        else:
            return ""
    except ET.ParseError:
        return ""


def load_ms_files(path="../Postgraduate/msyspjs/*.xml"):
    json_file = CORPUS_JSON_PATH
    if not os.path.exists(json_file):
        docs = []
        file_list = glob.glob(path)
        for file in file_list:
            with open(file, "rb") as f:
                try:
                    doc = f.read().decode("utf-8")
                except UnicodeDecodeError:
                    doc = f.read().decode("latin-1")

                full_text = extract_full_text(doc).lstrip()
                if full_text != "":
                    docs.append(full_text)

        json.dump(docs, open(json_file, "w"))
    else:
        docs = load_object(json_file)
    return docs


def load_object(json_file):
    if os.path.exists(json_file):
        return json.load(open(json_file, "r"))
    else:
        return None


def dump_object(obj, json_file):
    json.dump(obj, open(json_file, "w"))


def cut_sentence(words):
    start = 0
    i = 0
    sentence_list = []
    punt_list = str(',.!?:;~，。！？：；～ ')
    for word in words:
        if word in punt_list and token not in punt_list:  # 检查标点符号下一个字符是否还是标点
            sentence_list.append(words[start:i + 1])
            start = i + 1
            i += 1
        else:
            i += 1
            token = list(words[start:i + 2]).pop()  # 取下一个字符
    if start < len(words):
        sentence_list.append(words[start:])
    return sentence_list
