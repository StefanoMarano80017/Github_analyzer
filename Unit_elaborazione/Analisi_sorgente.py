from Unit_elaborazione import Cloc_Analize
from Unit_elaborazione import Request_Code


class Analyzer:
    def __init__(self, group: str):
        self.group = group
        self.cloc = Cloc_Analize.C_Analysis(group)

    def cloc_files(self, links: list)->list:
        for link in links:
            self.cloc_file(link)
        # return [self.summary.total_code_count, self.summary.total_documentation_count, self.summary.total_empty_count]
        return self.cloc.get_summary()

    def cloc_file(self, link: str):
        try:
            req = Request_Code.extract_code(link)
            tmp = link.split('.')
            suffix = tmp[len(tmp) - 1]
            return self.cloc.count_file(req.get_content(), suffix)
        except Exception as e:
            print(e)
