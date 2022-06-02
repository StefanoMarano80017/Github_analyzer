import Cloc_Analize
import Request_Code


class analyzer:
    def __init__(self, group: str, links: list, suffixs: list):
        self.links = links
        self.suffixs = suffixs
        self.group = group

    def analyser_files(self):
        req = Request_Code.extract_code()
        cloc = Cloc_Analize.C_Analysis(self.group)

        for (link, suffix) in zip(self.links, self.suffixs):
            try:
                cloc.count_file(req.get_content(link), suffix)
            except Exception as e:
                print(e)
