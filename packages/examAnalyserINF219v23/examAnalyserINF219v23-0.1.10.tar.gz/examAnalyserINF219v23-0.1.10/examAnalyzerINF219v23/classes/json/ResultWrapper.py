from .Result import Result


class ResultWrapper:
    def __init__(self, result):
        self.result = Result(**result)
