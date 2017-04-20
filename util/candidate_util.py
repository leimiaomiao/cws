import re
import util.unicode_util as unicode_util
import util.file_util as file_util
from config import constant as constant
from config import expression
import ijson
from dao.candidate import Candidate


class CandidateUtil(object):
    def rtrv_candidate_dict(self):
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

    @staticmethod
    def dump_candidate_dict_to_db():
        with open(constant.CANDIDATE_DICT_JSON_PATH, 'r') as fd:
            parser = ijson.parse(fd)
            candidate = Candidate()
            for prefix, event, value in parser:
                print(prefix, event, value)
                if (prefix, event) == ("", "map_key"):
                    if candidate is not None:
                        candidate.save()
                    candidate = Candidate()
                    candidate.word = value
                    candidate.left_set = {}
                    candidate.right_set = {}
                elif event == "map_key" and prefix.endswith("left_set"):
                    key = value
                    left_temp_dict = {key: None}
                elif event == "number" and prefix.endswith("left_set.%s" % key):
                    left_temp_dict[key] = str(value)
                    candidate.left_set.update(left_temp_dict)
                elif event == "map_key" and prefix.endswith("right_set"):
                    key = value
                    right_temp_dict = {key: None}
                elif event == "number" and prefix.endswith("right_set.%s" % key):
                    right_temp_dict[key] = str(value)
                    candidate.right_set.update(right_temp_dict)
                elif event == "number" and prefix.endswith("count"):
                    candidate.count = value
