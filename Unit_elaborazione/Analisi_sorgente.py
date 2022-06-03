from Unit_elaborazione import Cloc_Analize
from Unit_elaborazione import Request_Code


class Analyzer:
    def __init__(self, group: str, links: list, suffixs: list):
        self.links = links
        self.suffixs = suffixs
        self.group = group

    @staticmethod
    def cloc_file(req, cloc, link, suffix):
        return cloc.count_file(req.get_content(link), suffix)

    def cloc_files(self) -> list:
        req = Request_Code.extract_code()
        cloc = Cloc_Analize.C_Analysis(self.group)

        for (link, suffix) in zip(self.links, self.suffixs):
            self.cloc_file(req, cloc, link, suffix)

        # return [self.summary.total_code_count, self.summary.total_documentation_count, self.summary.total_empty_count]
        return cloc.get_summary()
