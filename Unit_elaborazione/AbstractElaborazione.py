from abc import ABC


class AbstractElaborazione(ABC):

    def __init__(self, ElabName):
        if ElabName is not None:
            self.name = ElabName
        else:
            raise "ELabName None"

    def GetName(self) -> str:
        return self.name

    def DoElaborazione(self, RepoList: list) -> list:
        pass
