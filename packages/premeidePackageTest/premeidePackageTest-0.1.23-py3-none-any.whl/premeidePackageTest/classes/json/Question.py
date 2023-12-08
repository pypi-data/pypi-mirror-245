
class Question:
    def __init__(self, **kwargs):
        self.maxQuestionScore = kwargs.get('ext_inspera_maxQuestionScore')
        self.questionId = kwargs.get('ext_inspera_questionId')
        self.questionTitle = kwargs.get('ext_inspera_questionTitle')
        self.autoScore = kwargs.get('ext_inspera_autoScore')
        self.durationSeconds = kwargs.get('ext_inspera_durationSeconds')
        self.candidateResponses = kwargs.get('ext_inspera_candidateResponses')
        self.questionContentItemId = kwargs.get('ext_inspera_questionContentItemId')
        self.questionNumber = kwargs.get('ext_inspera_questionNumber')
        self.questionWeight = kwargs.get('ext_inspera_questionWeight')
        self.manualScores = self.extract_manual_scores(kwargs.get('ext_inspera_manualScores', []))

    def to_dict(self):
        return {
            "ext_inspera_maxQuestionScore": self.maxQuestionScore,
            "ext_inspera_questionId": self.questionId,
            "ext_inspera_questionTitle": self.questionTitle,
            "ext_inspera_autoScore": self.autoScore,
            "ext_inspera_durationSeconds": self.durationSeconds,
            "ext_inspera_candidateResponses": self.candidateResponses,
            "ext_inspera_questionContentItemId": self.questionContentItemId,
            "ext_inspera_questionNumber": self.questionNumber,
            "ext_inspera_questionWeight": self.questionWeight
        }
    def extract_manual_scores(self, manual_scores):
        if not manual_scores:
            return None
        # Assuming there's only one manual score per question
        return manual_scores[0].get('ext_inspera_manualScore')
