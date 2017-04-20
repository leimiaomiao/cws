from util.candidate_util import CandidateUtil
from util.file_util import load_ms_files
from dao.candidate import Candidate
from util.unicode_util import is_chinese
import math


class ChineseWordSegment(object):
    def __init__(self, text):
        self.candidate_list = CandidateUtil.rtrv_candidate_list(text)

    def rtrv_candidate_by(self, word):
        candidate = Candidate.rtrv_one(word=word)
        inner_solid = self.calc_inner_solid_degree(candidate)
        outer_free_degree = self.calc_outer_free_degree(candidate)

        candidate.inner_solid_degree = inner_solid
        candidate.outer_free_degree = outer_free_degree
        return candidate

    @staticmethod
    def calc_inner_solid_degree(candidate):
        if candidate is None:
            return 0
        if len(candidate.word) == 1:
            return 1
        inner_solid = 1
        for i in range(len(candidate.word) - 1):
            j = i + 1
            pre_word = Candidate.rtrv_one(word=candidate.word[:j])
            post_word = Candidate.rtrv_one(word=candidate.word[j:])
            if pre_word is not None and post_word is not None:
                value = candidate.count / (pre_word.count * post_word.count)
                inner_solid = min(value, inner_solid)
        return inner_solid

    def calc_outer_free_degree(self, candidate):
        if candidate is None:
            return 0
        left_set = candidate.left_set
        right_set = candidate.right_set

        left_set_entropy = self.calc_info_entropy(left_set)
        right_set_entropy = self.calc_info_entropy(right_set)
        return min(left_set_entropy, right_set_entropy)

    def calc_info_entropy(self, neighbor_set):
        count = self.calc_count(neighbor_set)
        entropy = 0
        for key, value in neighbor_set.items():
            if is_chinese(key) and key != ' ':
                entropy += -(int(value) / count) * math.log(2, (int(value) / count))
        print(entropy)
        return entropy

    @staticmethod
    def calc_count(neighbor_set):
        count = 0
        for key, value in neighbor_set.items():
            if is_chinese(key) and key != ' ':
                count += int(value)
        return count


if __name__ == "__main__":
    corpus_list = load_ms_files()
    corpus = corpus_list[0]
    cws = ChineseWordSegment(corpus)
    candidate = cws.rtrv_candidate_by("化肥")
    print(candidate.right_set)
    print(candidate.count, candidate.inner_solid_degree, candidate.outer_free_degree)

