from matplotlib import pyplot as plt
from classes.Constants import Constants
from classes.json.Exam import Exam
import math as m


class PBC:

    REVIEW_PBC = 0.2    #Review - Revision likely necessary 
    MARGINAL_PBC = 0.3  #Marginal - Revision may be necessary 
    BETTER_PBC = 0.4    #Better - Some revision may be necessary
    # 0.4 >             #Best - No revision necessary

    """
    Point-biserial correlation (PBC) class

    Parameters:
    - title (str): Question title
    - value (float): coefficient, value between -1 and 1
    """

    def __init__(self, title, value):
        self.title = title
        self.value = value

    @classmethod
    def extractFromExam(cls, exam):
        return cls.retrieve_PBCs(exam)

    @classmethod
    def getFigure(cls, exam):
        PBCs = PBC.extractFromExam(exam)
        PBCs = list(reversed(PBCs))

        fig1, ax = plt.subplots(figsize=(8, 10))
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        plt.title("PBC visualization")

        y_positions = range(len(PBCs))
        titles = [pbc.title for pbc in PBCs]
        pbc_values = [pbc.value for pbc in PBCs]

        colors = [cls.get_color(pbc.value) for pbc in PBCs]

        bars = ax.barh(y_positions, pbc_values,align='center', color=colors, alpha=0.7)
        ax.set_yticks(y_positions)
        ax.set_yticklabels(titles)
        ax.set_xlabel('PBC value')
        ax.set_xlim(min(pbc.value for pbc in PBCs)-0.2, 1)

        labels = [f"Review (PBC <= {PBC.REVIEW_PBC})", f"Marginal ({PBC.REVIEW_PBC} < PBC <= {PBC.MARGINAL_PBC})",
                  f"Better ({PBC.MARGINAL_PBC} < PBC <= {PBC.BETTER_PBC})", f"Best (PBC > {PBC.BETTER_PBC})"]
        handles = [plt.Rectangle((0, 0), 1, 1, color=PBC.get_color(port))
                   for port in [PBC.REVIEW_PBC, PBC.MARGINAL_PBC, PBC.BETTER_PBC, 0.400001]]
        ax.legend(handles, labels, title="PBC level", loc='upper right')

        plt.tight_layout()

        # -- Bar chart --

        fig2, ax2 = plt.subplots(figsize=(8, 3))

        Review_count = sum(1 for pbc in PBCs if pbc.value <= PBC.REVIEW_PBC)
        Marginal_count = sum(1 for pbc in PBCs if PBC.REVIEW_PBC < pbc.value <= PBC.MARGINAL_PBC)
        Better_count = sum(1 for pbc in PBCs if PBC.MARGINAL_PBC < pbc.value <= PBC.BETTER_PBC)
        Best_count = sum(1 for pbc in PBCs if pbc.value > PBC.BETTER_PBC)

        counts = [Review_count, Marginal_count, Better_count, Best_count]

        ax2.bar(["Review", "Marginal", "Better", "Best"], counts, color=[
                'red', 'orange', 'yellow', 'green'], alpha=0.7)
        ax2.set_ylabel('Count')
        ax2.yaxis.grid(True, linestyle='--', alpha=0.5)
        ax2.set_title('PBC Category Counts')

    

        return [fig1, fig2]

    @classmethod
    def retrieve_PBCs(cls, exam: Exam):
        '''
        Calculate the point-biserial-correlation for each question from an exam
        return list of correlations.
        '''

        # Retrieve candidate scores:
        candidate_scores = exam.getCandidateScores()

        # list of lists, where as each list is a question, and each 1 or 0 corresponds to
        # student and if he/she answered the question correct or not
        questions_1_0 = [[] for _ in range(len(exam.getQuestionIds()))]

        for can in exam.candidates:
            for i, question in enumerate(can.questions):
                # Calculate total score (autoScore + manualScore if available)
                total_score = question.autoScore
                if question.manualScores is not None:
                    total_score += question.manualScores

                if total_score == question.maxQuestionScore:
                    questions_1_0[i].append(1)
                else:
                    questions_1_0[i].append(0)

        # Initializing list to hold all PBCs
        PBCs = []

        # Retrieve the std of score
        num_all = len(candidate_scores)
        mean_all = sum(candidate_scores)/len(candidate_scores)

        squared_diff = [(score - mean_all)**2 for score in candidate_scores]
        average_squared_diff = sum(squared_diff) / len(squared_diff)

        std_all = m.sqrt(average_squared_diff)

        # Retrieve the PBC of each question
        for i in range(len(exam.getQuestionIds())):
            data = list(zip(candidate_scores, questions_1_0[i]))

            passed_candidates = [score for score,
                                 correct in data if correct == 1]
            failed_candidates = [score for score,
                                 correct in data if correct == 0]

            num_passed = len(passed_candidates)
            num_failed = len(failed_candidates)

            if num_passed == 0:
                mean_passed = 0
            else:
                mean_passed = sum(passed_candidates)/len(passed_candidates)

            if num_failed == 0:
                mean_failed = 0
            else:
                mean_failed = sum(failed_candidates)/len(failed_candidates)

            correlation = ((mean_passed-mean_failed)/std_all) * \
                m.sqrt((num_passed*num_failed)/(num_all)**2)

            curr_pbc = PBC(exam.getQuestionNr(
                exam.getQuestionIds()[i]), correlation)

            PBCs.append(curr_pbc)

        return PBCs

    @staticmethod
    def get_color(value):
        """Determine the color based on the value of correctPortion."""
        if value <= PBC.REVIEW_PBC:
            return "red"
        elif value <= PBC.MARGINAL_PBC:
            return "orange"
        elif value <= PBC.BETTER_PBC:
            return "yellow"
        else:
            return "green"
