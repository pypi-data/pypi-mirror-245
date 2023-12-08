from classes.json.Exam import Exam
import matplotlib.pyplot as plt


class QuestionTable:
    """
    Table that tells what the questions actually was
    """

    def __init__(self, question):
        self.question = question

    @classmethod
    def extractFromExam(cls, exam):
        questionLabel = {}
        question_ids = exam.getQuestionIds()
        for i in range(len(question_ids)):
            question_id = question_ids[i]
            question_title = exam.getQuestionTitle(question_id)
            questionLabel[question_id] = f'Question {i + 1}: {question_title}'

        #exam.getQuestionIds()
        return questionLabel

    @classmethod
    def getFigure(cls, exam):
        data = QuestionTable.extractFromExam(exam)

        question_numbers = []
        question_titles = []
        for question_id, title in data.items():
            question_numbers.append(title.split(":")[0].strip())
            question_titles.append(title.split(":")[1].strip())

        fig, ax = plt.subplots()

        # Hide axes
        ax.axis('off')

        table_data = [['Question Number', 'Question Title']]
        for i in range(len(question_numbers)):
            table_data.append([question_numbers[i], question_titles[i]])

        table = ax.table(cellText=table_data, loc='center', cellLoc='center')

        # Setting alternating row colors
        for i, (key, cell) in enumerate(table.get_celld().items()):
            row, col = key
            if row == 0:
                cell.set_facecolor('#ADD8E6')  # Light blue for the header row
            elif row % 2 == 0:
                cell.set_facecolor('#E0E0E0')  # Light gray for even rows
            else:
                cell.set_facecolor('white')  # White for odd rows

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)

        return fig
        