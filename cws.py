import re

import util.file_util as file_util
import util.unicode_util as unicode_util
from config import constant as constant
from config import expression
from datetime import datetime


class ChineseWordSegment(object):
    def __init__(self):
        self.candidate_dict = self.rtrv_candidate_dict()

    def rtrv_candidate_dict(self):
        print("loading")
        start_time = datetime.now()
        candidate_dict = file_util.load_object(constant.CANDIDATE_DICT_JSON_PATH)
        end_time = datetime.now()
        print("loading finished")
        print("time expense %s" % (end_time - start_time))
        if candidate_dict is None:
            candidate_dict = {}
            corpus = file_util.load_ms_files()
            for doc in corpus:
                doc = self.replace_number(doc)
                candidate_list = self.rtrv_candidate_list(doc)
                for candidate, left, right in candidate_list:
                    if candidate in candidate_dict:
                        candidate_dict[candidate]["count"] += 1

                        left_set = candidate_dict[candidate]["left_set"]
                        if left in left_set:
                            left_set[left] += 1
                        else:
                            left_set[left] = 1
                        candidate_dict[candidate]["left_set"] = left_set

                        right_set = candidate_dict[candidate]["right_set"]
                        if right in right_set:
                            right_set[right] += 1
                        else:
                            right_set[right] = 1
                        candidate_dict[candidate]["right_set"] = right_set
                    else:
                        candidate_dict[candidate] = {"count": 1, "left_set": {left: 1}, "right_set": {right: 1}}

            file_util.dump_object(candidate_dict, constant.CANDIDATE_DICT_JSON_PATH)
        return candidate_dict

    @staticmethod
    def rtrv_candidate_list(text):
        candidate_list = []
        text_len = len(text)
        for i in range(text_len):
            # 当前字符非汉字、数字、字母
            if unicode_util.is_other(text[i]):
                # 加入左邻节点和右邻节点
                if i < 1:
                    candidate_list.append((text[i], '', text[i + 1]))
                elif 1 <= i <= text_len - 2:
                    candidate_list.append((text[i], text[i - 1], text[i + 1]))
                else:
                    candidate_list.append((text[i], text[i - 1], ''))
                continue
            # 当前字符为汉字
            else:
                j = 1
                while j <= constant.WINDOW_LENGTH and i + j < text_len:
                    if i + j < 1:
                        candidate_list.append((text[i:i + j], '', text[i + j + 1]))
                    elif 1 <= i + j <= text_len - 1:
                        candidate_list.append((text[i:i + j], text[i - 1], text[i + j]))
                    else:
                        candidate_list.append((text[i:i + j], text[i - 1], ''))

                    if unicode_util.is_other(text[i + j]):
                        break
                    j += 1
        return candidate_list

    @staticmethod
    def replace_number(text):
        return re.sub(expression.NUMBER_RE, constant.NUMBER_REPLACEMENT, text, flags=re.UNICODE)


if __name__ == "__main__":
    cws = ChineseWordSegment()
    print(cws.candidate_dict["辽"]["right_set"])

