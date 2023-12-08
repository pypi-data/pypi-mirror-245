import matplotlib.pyplot as plt
from examAnalyserINF219v23.classes.Constants import Constants
from examAnalyserINF219v23.classes.json.Exam import Exam


class GradeDistribution:
    """
    Class for generating Grade Distribution graph
    """

    def __init__(self, A=0, B=0, C=0, D=0, E=0, F=0):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E
        self.F = F

    @classmethod
    def extractFromExam(cls, exam):
        grade_counts = cls.calculateGrades(exam)
        return cls(**grade_counts)

    @staticmethod
    def getFigure(exam):
        """
        Generates a bar chart visualization representing the grade distribution for an exam.
        This method first extracts the grade distribution from the provided exam object using the GradeDistribution.extractFromExam method. 
        The grade distribution includes the count of each grade (A, B, C, D, E, F). A bar chart is then generated, 
        where each bar represents the number of students who have achieved each grade.

        Parameters:
        exam (ExamType): An instance of an Exam class from which the grade distribution data is extracted. 

        Returns:
        A matplotlib figure object containing the generated bar chart.

        Raises:
        TypeError: If the types of the provided arguments are not as expected.

        Note:
        - The bar chart visualizes the number of students for each grade (A-F).
        - This method is a static method and should be called on the class rather than an instance of the class.
        """
        grade_distribution = GradeDistribution.extractFromExam(exam)

        grades = ['A', 'B', 'C', 'D', 'E', 'F']
        values = [grade_distribution.A, grade_distribution.B, grade_distribution.C,
                  grade_distribution.D, grade_distribution.E, grade_distribution.F]

        fig, ax = plt.subplots()
        ax.bar(grades, values)
        ax.set_xlabel('Grade')
        ax.set_ylabel('Number of Students')
        ax.set_title('Grade Distribution')

        return fig

    @staticmethod
    def calculateGrades(exam):
        """
        Calculates the distribution of grades for an exam based on predefined thresholds.

        This method computes grades for an exam by first determining the maximum possible score for the exam. 
        It then iterates over each candidate's score, converting these scores into percentages of the maximum score. 
        Based on predefined grade thresholds (A, B, C, D, E, F), each candidate's score is classified into a grade category. 
        The method returns a dictionary that counts the number of candidates in each grade category.

        Parameters:
        exam (ExamType): An instance of an Exam class. 

        Returns:
        dict: A dictionary with keys as grade categories ('A', 'B', 'C', 'D', 'E', 'F') and values as the count of candidates in each category.

        Raises:
        ZeroDivisionError: If max_score is zero, leading to a division by zero error.
        TypeError: If the types of the returned values from exam methods are not as expected.

        Note:
        - The grade thresholds are set at fixed percentages: A (>=85%), B (>=70%), C (>=55%), D (>=40%), E (>=30%), and F (<30%).
        - This method is a static method and should be called on the class rather than an instance of the class.
    """
        max_score = exam.getMaxScore()

        grade_thresholds = {
            'A': 0.85,  # 85%
            'B': 0.70,  # 70%
            'C': 0.55,  # 55%
            'D': 0.40,  # 40%
            'E': 0.30,  # 30%
            'F': 0      # Below 30%
        }

        grade_counts = {
            'A': 0,
            'B': 0,
            'C': 0,
            'D': 0,
            'E': 0,
            'F': 0
        }

        candidate_scores = exam.getCandidateScores()

        # Convert candidate scores to percentages
        candidate_percentages = [
            score / max_score for score in candidate_scores]

        for percentage in candidate_percentages:
            for grade, threshold in grade_thresholds.items():
                if percentage >= threshold:
                    grade_counts[grade] += 1
                    break

        return grade_counts
