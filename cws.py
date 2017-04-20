from util.candidate_util import CandidateUtil
from util.file_util import load_ms_files


class ChineseWordSegment(object):
    def __init__(self, text):
        self.candidate_list = CandidateUtil.rtrv_candidate_list(text)


if __name__ == "__main__":
    corpus_list = load_ms_files()
    corpus = corpus_list[0]
    cws = ChineseWordSegment(corpus)
    print(cws.candidate_list)
