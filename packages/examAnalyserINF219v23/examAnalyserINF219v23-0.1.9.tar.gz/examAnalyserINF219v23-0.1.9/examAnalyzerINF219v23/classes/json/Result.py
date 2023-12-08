from .Question import Question


class Result:
    def __init__(self, **kwargs):
        self.questions = [Question(**question_data)
                          for question_data in kwargs.get('ext_inspera_questions', [])]
        self.autoScore = kwargs.get('ext_inspera_autoScore')
        self.maxScore = self.calculate_max_score()
        self.candidateId = kwargs.get('ext_inspera_candidateId')
        self.sourcedId = kwargs.get('sourcedId')
        self.userAssessmentSetupId = kwargs.get(
            'ext_inspera_userAssessmentSetupId')
        self.userAssessmentId = kwargs.get('ext_inspera_userAssessmentId')
        self.dateLastModified = kwargs.get('dateLastModified')
        self.startTime = kwargs.get('ext_inspera_startTime')
        self.endTime = kwargs.get('ext_inspera_endTime')
        self.extraTimeMins = kwargs.get('ext_inspera_extraTimeMins')
        self.incidentTimeMins = kwargs.get('ext_inspera_incidentTimeMins')
        self.attendance = kwargs.get('ext_inspera_attendance')
        self.lineItem = kwargs.get('lineItem')
        self.student = kwargs.get('student')
        self.finalGradeDate = kwargs.get('ext_inspera_finalGradeDate')
        self.finalGrade = kwargs.get('ext_inspera_finalGrade')
        self.totalScore = kwargs.get('ext_inspera_totalScore')
        self.score = kwargs.get('score')

    def calculate_max_score(self):
        return sum(question.maxQuestionScore for question in self.questions)

    def to_dict(self):
        return {
            "ext_inspera_autoScore": self.autoScore,
            "ext_inspera_candidateId": self.candidateId,
            "ext_inspera_questions": [question.to_dict() for question in self.questions],
            "sourcedId": self.sourcedId,
            "ext_inspera_userAssessmentSetupId": self.userAssessmentSetupId,
            "ext_inspera_userAssessmentId": self.userAssessmentId,
            "dateLastModified": self.dateLastModified,
            "ext_inspera_startTime": self.startTime,
            "ext_inspera_endTime": self.endTime,
            "ext_inspera_extraTimeMins": self.extraTimeMins,
            "ext_inspera_incidentTimeMins": self.incidentTimeMins,
            "ext_inspera_attendance": self.attendance,
            "lineItem": self.lineItem,
            "student": self.student,
            "ext_inspera_finalGradeDate": self.finalGradeDate,
            "ext_inspera_finalGrade": self.finalGrade,
            "ext_inspera_totalScore": self.totalScore,
            "score": self.score
        }
