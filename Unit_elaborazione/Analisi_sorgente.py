from Unit_elaborazione import Cloc_Analize
from Unit_elaborazione import Request_Code


class Analyzer:
    def __init__(self, group: str, link:str):
        self.link = link
        self.group = group

    def cloc_file(self, req, cloc, link):
        tmp = self.link.split('.')
        suffix = tmp[len(tmp)-1]
        return cloc.count_file(req.get_content(), suffix)

    def cloc_files(self) -> list:
        req = Request_Code.extract_code(self.link)
        cloc = Cloc_Analize.C_Analysis(self.group)

        self.cloc_file(req, cloc, self.link)

        # return [self.summary.total_code_count, self.summary.total_documentation_count, self.summary.total_empty_count]
        return cloc.get_summary()
