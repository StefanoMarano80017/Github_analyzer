from Unit_elaborazione import Cloc_Analize
from Unit_elaborazione import Request_Code


class analyzer:
    def __init__(self, group: str, links: list, suffixs: list):
        self.links = links
        self.suffixs = suffixs
        self.group = group
        self.list_counts = []


    def cloc_file(self, req, cloc, link, suffix):
        return cloc.count_file(req.get_content(link), suffix)

    def cloc_files(self):
        req = Request_Code.extract_code()
        cloc = Cloc_Analize.C_Analysis(self.group)

        for (link, suffix) in zip(self.links, self.suffixs):
            self.cloc_file(req, cloc, link, suffix)

        print(cloc.get_summary())