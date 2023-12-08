import json
import pypandoc
from premeidePackageTest.classes.features.Box import Box
from premeidePackageTest.classes.features.GradeDistribution import GradeDistribution
from premeidePackageTest.classes.features.PBC import PBC
from premeidePackageTest.classes.features.QuestionTable import QuestionTable
from premeidePackageTest.classes.features.QuestionTimeAverage import QuestionTimeAverage
from premeidePackageTest.classes.features.TaskDuration import TaskDuration
from premeidePackageTest.classes.json.Exam import Exam


class File_gen:
    '''
    The File_gen class provides functions for generating PDF reports from exam data.

    Functions:
    - calculate_pdf(json_path, pdf_path, md_path, options): Calculate PDF function, for calculating the PDF
      corresponding to the current JSON exam and options chosen by the user.
    - generate_viz(exam, options): Generate visualization function, for generating each and every visualization
      corresponding to options chosen from the current exam.
    - generate_md_string(img_paths, options): Generate Markdown string function, for creating the Markdown content
      with links to visualizations based on the chosen options.
    '''

    def calculate_pdf(json_path, pdf_path, md_path, options):
        """
        Calculate PDF function, for calculating the pdf
        corresponding to the current json_exam and options
        chosen by user.

        Parameters:
        - json_path (str): path to json_file containing exam
        - options (List[str]): List of options chosen

        Returns:
        - pdf_file_path(str): path to pdf file
        """
        # Open json file and Generate matplotlib vizualizations:
        with open(json_path) as f:
            exam_json_data = json.load(f)
        exam = Exam(**exam_json_data)

        img_file_paths = File_gen.generate_viz(exam, options)

        # Generate markdown string with curr options:
        md_string = File_gen.generate_md_string(img_file_paths, options)

        # Define the file paths
        md_file_path = md_path
        pdf_file_path = pdf_path

        # Save the md_string as .md
        with open(md_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_string)

        # Use pypandoc to convert .md --> PDF
        try:
            pypandoc.convert_file(md_file_path, 'pdf',
                                  format='markdown', outputfile=pdf_file_path)
        except Exception as e:
            print(f"Error converting Markdown to PDF: {e}")
            return None

        # Return the path to the generated PDF file
        return pdf_file_path

    def generate_viz(exam, options):
        """
        Generate visualization function, for generating each
        and every viz corresponding to options chosen from the
        current exam

        Parameters:
        - exam (Exam): Exam object for curr exam
        - options(List[str]): List of options

        Returns:
        - fig_paths(List[str]): List of figure paths
        """
        include_question_table = "Question Table" in options,
        include_grade_distribution = "Grade Distribution" in options,
        include_correct_portion = "Correct Portion" in options,
        include_PBC = "PBC" in options,
        include_task_duration = "Task Duration" in options,
        include_question_time_average = "Question Time Average" in options

        fig_paths = []

        if include_question_table:
            question_table_fig = QuestionTable.getFigure(exam)
            question_table_fig.set_size_inches(5, 6)
            question_table_fig_path = "static/question_table.png"

            question_table_fig.savefig(
                question_table_fig_path, bbox_inches='tight')
            fig_paths.append(question_table_fig_path)

        if include_correct_portion:
            box_fig = Box.getFigure(exam, "Correct Portion Visualization")
            box_fig.set_size_inches(5, 8)
            box_fig_path = "static/box_fig.png"

            box_fig.savefig(box_fig_path, bbox_inches='tight')
            fig_paths.append(box_fig_path)

        if include_grade_distribution:
            grade_distribution_fig = GradeDistribution.getFigure(exam)
            grade_distribution_fig_path = "static/grade_distribution_fig.png"

            grade_distribution_fig.savefig(
                grade_distribution_fig_path, bbox_inches='tight')
            fig_paths.append(grade_distribution_fig_path)

        if include_PBC:
            pbc_figs = PBC.getFigure(exam)

            for i, fig in enumerate(pbc_figs):
                curr_pbc_fig_path = f"static/pbc_fig_{i}.png"
                fig.savefig(curr_pbc_fig_path, bbox_inches='tight')
                fig_paths.append(curr_pbc_fig_path)

        if include_task_duration:
            task_duration_fig = TaskDuration.getFigure(
                exam, "Task Duration Visualization")
            task_duration_fig_path = "static/task_duration_fig.png"

            task_duration_fig.savefig(
                task_duration_fig_path, bbox_inches='tight')
            fig_paths.append(task_duration_fig_path)

        if include_question_time_average:
            q_time_average_fig = QuestionTimeAverage.getFigure(exam)

            for i, fig in enumerate(q_time_average_fig):
                curr_q_time_fig_path = f"static/q_time_fig_{i}.png"
                fig.savefig(curr_q_time_fig_path, bbox_inches='tight')
                fig_paths.append(curr_q_time_fig_path)

        return fig_paths

    def generate_md_string(img_paths, options):
        # Generation of md string
        ### FRONT PAGE W/ FOOTER ###
        md_string = '# Exam analyzer (Version 1.0)\n\n&nbsp;\n\n'
        md_string += '## Features chosen:'
        for i, option in enumerate(options, start=1):
            anchor_link = option.lower().replace(" ", "-")
            md_string += f'\n\n**Feature {i}:** *[{option}](#{anchor_link})*'
        md_string += '\n\n&nbsp;\n\n*Click the feature for redirection to feature page*'

        footer = 'Generated using Exam Analyzer (Version 1.0)'
        for i in range(26-len(options)-2):
            md_string += f'\n\n&nbsp;'
        md_string += "\n\n" + int(134/2-len(footer)) * "&nbsp;" + f'{footer}'
        md_string += '\n\n\\newpage'  # Page break

        ### VIS PAGES ###
        for i, path in enumerate(img_paths):
            ### QUESTION TABLE ###
            if 'question_table' in path:
                md_string += '# Question Table:\n\n'
                md_string += """The following is a question table generated from your uploaded exam
                showing all questions numerated from 1 to n, where n is the number of questions.             
                """
                md_string += f'\n![Question table]({path}) \n\n\\newpage'

            ### CORRECT PORTION ###
            if 'box' in path:
                md_string += '# Correct Portion:\n\n'
                md_string += '''The following is a visualization showing the portion (%) of students
                which got the following question correct. This was generated using the current uploaded
                exam.\n\n'''

                md_string += '## Difficulty levels:\n\n'
                md_string += '''**Easy ( (90, 100]% )** Questions in this range is considered easy where as almost all 
                or all students got it correct.\n\n'''
                md_string += '''**Moderately difficult ( (60 90]% )** Questions in this range is considered moderatly difficult
                where as more than half of the students get it correct, but not all.\n\n'''
                md_string += '''**Difficult ( (20, 60]% )** Questions in this range is considered hard as quite few get these
                questions correct.\n\n'''
                md_string += '''**Very difficult ( [0, 20]% )** Questions in this range is considered very difficult as a
                very low proportion or none of the students get these questions correct.\n\n'''

                md_string += f'![Correct portions]({path}) \n\n\\newpage'

            if 'grade_distribution' in path:
                md_string += '# Grade Distribution:\n\n'
                md_string += '''The following is a visualization showing the grade distribution among the
                students. The grades are retrieved from the standard grading system
                used at The University of Bergen.\n\n'''

                md_string += '''**Grades:**\n\n1. *A - Excellent*\n2. *B - Very good*\n3. *C - Good*
                \n4. *D - Satisfactory*\n5. *E - Sufficient*\n6. *F - Fail*\n\n&nbsp;\n\n'''

                md_string += f'![Grade distribution]({path}) \n\n\\newpage'

            if 'pbc_fig_0' in path:
                md_string += '# PBC (Point Biserial Correlation):\n\n'
                md_string += '''The PBC (Point Biserial Correlation) is a correlation factor generated from the exams
                showing how well a test item discriminates students. Discriminating in regards to which of the students
                who actually know the content, from those who dont.\n\n&nbsp;\n\n'''

                md_string += '*Calculation of PBC:*\n\n'
                md_string += '1. *M~0~ / M~1~* - Mean of group 0 and 1\n'
                md_string += '3. *n~0~ / n~1~* - Number of people in group 0 and 1\n'
                md_string += '2. *S~n~* - Standard deviation\n\n&nbsp;\n\n'

                md_string += "![PBC Calculation](static/CALC_PBC.png) \n\n![PBC (Standard Deviation)](static/CALC_PBC_STD.png)\n\n"
                md_string += "*See next page for results*"

            # TODO: FIKS resterende features (PBC, task dur, question time average.)

        # reutrn md_string:
        return md_string
