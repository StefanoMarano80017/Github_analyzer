from Unit_elaborazione import Cloc_Analize
from Unit_elaborazione import Request_Code



class counts:
    def __init__(self, code_count, doc_count, empty_count):
        self.code_count = code_count
        self.doc_count = doc_count
        self.empty_count = empty_count

class analyzer:
    def __init__(self, group: str, links: list, suffixs: list):
        self.links = links
        self.suffixs = suffixs
        self.group = group
        self.list_counts = []


    def analyser_file(self, req, cloc, link, suffix):
        return cloc.count_file(req.get_content(link), suffix)

    def analyser_files(self):
        req = Request_Code.extract_code()
        cloc = Cloc_Analize.C_Analysis(self.group)

        for (link, suffix) in zip(self.links, self.suffixs):
                print(link)
                print(self.analyser_file(req, cloc, link, suffix))

        return self.list_counts