import matplotlib.pyplot as plt

from classes.Constants import Constants


class Box:
    """
    Represents a box containing a question and its correct portion.

    Attributes:
        question (str): The question title.
        correctPortion (float): The correct portion for the question,
                               represented as a float between 0 and 100.
    """

    def __init__(self, question, correctPortion):
        self.question = question
        self.correctPortion = correctPortion

    @staticmethod
    def extractFromExam(exam):
        """
        Extracts and converts question-related data from an exam object into a list of Box objects.

        This method iterates through each question in the provided exam object. 
        For each question, it retrieves the question number and the correct portion of answers. 
        The correct portion is then converted into a percentage. 
        Each of these elements is used to create a Box object, which is appended to a list. 
        The list of Box objects is then returned in reverse order.

        Parameters:
        exam (ExamType): An instance of an Exam class. 
        This object should have methods getQuestionIds, getQuestionNr, and getCorrectPortion for accessing exam data.

        Returns:
        list[Box]: A list of Box objects, each representing a question's number and the percentage of correct answers. 
        The list is returned in reverse order of the questions in the exam.

        Raises:
        TypeError: If the types of the returned values from exam methods are not as expected.
        ZeroDivisionError: If there is a division by zero when calculating the correct percentage.
        
        Note:
        - The method is a static method and should be called on the class rather than an instance of the class.
    """
        boxes = []
        for questionId in exam.getQuestionIds():
            questionNr = exam.getQuestionNr(questionId)
            correctPortion = exam.getCorrectPortion(questionId=questionId)
            # Convert correctPortion to percentage
            correctPercentage = correctPortion / 100

            boxes.append(Box(questionNr, correctPercentage))
        return boxes[::-1]

    @staticmethod
    def getFigure(exam, title):
        """
        Generates a horizontal bar chart visualization for an exam object.

        This method first retrieves a list of Box objects from the provided exam object using the extractFromExam method. 
        Each Box object represents a question's number and the percentage of correct answers. 
        A horizontal bar chart is then generated using this data. 
        The chart displays each question's correct portion as a percentage, with bars colored according to difficulty level, as determined by Box.get_color.

        Parameters:
        exam (ExamType): An instance of an Exam class from which data is extracted. 
            The class should be compatible with Box.extractFromExam method.
        title (str): The title of the generated figure.

        Returns:
        matplotlib.figure.Figure: A matplotlib figure object containing the generated bar chart.

        Raises:
        TypeError: If the types of the provided arguments are not as expected.

        Note:
        - The method uses matplotlib for plotting, and it assumes matplotlib.pyplot is imported as plt.
        - The bar chart includes a legend indicating difficulty levels based on correct portion percentages.
        - This method is a static method and should be called on the class rather than an instance of the class.
    """
        # Retrieve boxes using extractFromExam method
        boxes = Box.extractFromExam(exam)

        # Visualization
        fig, ax = plt.subplots(figsize=(8, 10))
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        plt.title(title)

        y_positions = range(len(boxes))
        questions = [box.question for box in boxes]
        correctPortions = [box.correctPortion * 100 for box in boxes]
        colors = [Box.get_color(box.correctPortion) for box in boxes]

        bars = ax.barh(y_positions, correctPortions,
                       align='center', color=colors, alpha=0.7)
        ax.set_yticks(y_positions)
        ax.set_yticklabels(questions)
        ax.set_xlabel('Correct Portion (%)')
        ax.set_xlim(0, 100)

        labels = ["Very Difficult (0-20%)", "Difficult (21-60%)",
                  "Moderately difficult (61-90%)", "Easy (91-100%)"]
        handles = [plt.Rectangle((0, 0), 1, 1, color=Box.get_color(port))
                   for port in [0.1, 0.4, 0.75, 0.95]]
        ax.legend(handles, labels, title="Difficulty Level", loc='center right', bbox_to_anchor=(1.9, 0.5))

        return fig

    @staticmethod
    def get_color(value):
        """
        Determine the color based on the value of correctPortion.
    """
        if value <= 0.2:
            return "red"
        elif value <= 0.6:
            return "orange"
        elif value <= 0.9:
            return "yellow"
        else:
            return "green"
