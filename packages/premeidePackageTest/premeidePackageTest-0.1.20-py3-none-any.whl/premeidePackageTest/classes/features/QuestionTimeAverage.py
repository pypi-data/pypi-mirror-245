from premeidePackageTest.classes.features.Box import Box
from premeidePackageTest.classes.json.Exam import Exam
from premeidePackageTest.classes.features.TaskDuration import TaskDuration
import matplotlib.pyplot as plt


class QuestionTimeAverage:
    """
    """

    def __init__(self, question, correctPortion):
        self.question = question
        self.correctPortion = correctPortion

    @classmethod
    def extractFromExam(cls, exam: Exam):
        taskduration = TaskDuration.extractFromExam(exam)

        average_time = []
        question_nr = []
        question_ids = []

        for taskDuration in taskduration:
            question_id = taskDuration.questionID
            duration = taskDuration.candidate_time

            average_duration = int(sum(duration) / len(duration))
            average_time.append(average_duration)
            question_nr.append(exam.getQuestionNr(question_id))
            question_ids.append(question_id)

        for i in reversed(exam.checkMultipleChoice()):
            if i == False:
                del average_time[-1]
                del question_nr[-1]
                del question_ids[-1]

        sorted_pairs = sorted(zip(average_time, question_nr, question_ids))

        # Extract the sorted values into separate lists
        sorted_average_time, sorted_question_nr, question_ids = zip(
            *sorted_pairs)

        return sorted_average_time, sorted_question_nr, question_ids

    @classmethod
    def getFigure(cls, exam: Exam):
        sorted_average_time, sorted_question_nr, question_ids = cls.extractFromExam(
            exam)

        colors = []
        # Calculate colors for each question based on correct portion
        for question_id in question_ids:
            correct_portion = (exam.getCorrectPortion(question_id)) / 100
            color = Box.get_color(correct_portion)
            colors.append(color)

        # Line plot - Average Time vs Question Number
        fig1 = plt.figure(figsize=(8, 6))
        plt.plot(sorted_question_nr, sorted_average_time,
                 marker='o', linestyle='-', color='blue')
        plt.xlabel('Question Number')
        plt.ylabel('Average Time')
        plt.title('Line Plot: Average Time vs Question Number')
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Bar plot - Average Time vs Question Number with color coding
        fig2 = plt.figure(figsize=(8, 6))
        plt.bar(sorted_question_nr, sorted_average_time,
                color=colors, edgecolor='black')
        plt.xlabel('Question Number')
        plt.ylabel('Average Time')
        plt.title('Bar Plot: Average Time vs Question Number')
        plt.xticks(rotation=90)

        # Adding legend outside the plot
        labels = ["Very Difficult (0-20%)", "Difficult (21-60%)",
                  "Moderately difficult (61-90%)", "Easy (91-100%)"]
        handles = [plt.Rectangle((0, 0), 1, 1, color=Box.get_color(
            port / 100)) for port in [20, 60, 90, 100]]
        plt.legend(handles, labels, title="Difficulty Level",
                   loc='upper left', bbox_to_anchor=(1, 1))

        plt.tight_layout()
        return fig1, fig2
