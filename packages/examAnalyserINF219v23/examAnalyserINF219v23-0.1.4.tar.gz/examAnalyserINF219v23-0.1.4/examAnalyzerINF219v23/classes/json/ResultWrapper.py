from examAnalyserINF219v23.classes.json.Result import Result


class ResultWrapper:
    def __init__(self, result):
        self.result = Result(**result)
