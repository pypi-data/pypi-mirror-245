import matplotlib.pyplot as plt
from ..Constants import Constants
from ..features.Box import Box
from ..json.Exam import Exam


class TaskDuration:
    """
    Represents the duration students use for every task 
    """

    def __init__(self, questionID, candidate_time: {int: float}, correctPortion):
        self.questionID = questionID
        self.candidate_time = candidate_time
        self.correctPortion = correctPortion

    @classmethod
    def extractFromExam(cls, exam: Exam):
        """
        Extracts task durations from the provided Exam object and creates TaskDuration instances for each question.

        Args:
            cls: Class reference.
            exam (Exam): The Exam object containing candidate and question information.

        Returns:
            List[TaskDuration]: A list of TaskDuration instances representing task durations for each question in the exam.

        Explanation:
            This method iterates through the candidates and their questions within the provided Exam object. It collects 
            the durations for each question/task attempted by the candidates and calculates the correct portion for each 
            question. It then creates TaskDuration instances containing question ID, candidate durations, and correct portion.
            The resulting list comprises TaskDuration objects encapsulating the duration data for analysis or visualization.

        Example:
            task_durations = TaskDuration.extractFromExam(my_exam)
        """
        durations = {}
        candidates = exam.candidates
        for can in candidates:
            for question in can.questions:
                question_id = question.questionId
                duration_seconds = question.durationSeconds
                if question_id not in durations:
                    durations[question_id] = []
                durations[question_id].append(duration_seconds)

        taskDurations = []
        for questionId, duration_list in durations.items():
            correctPortion = exam.getCorrectPortion(
                questionId=questionId) / 100
            taskDurations.append(
                cls(questionId, duration_list, correctPortion))
        return taskDurations

    @staticmethod
    def _calculateCandidateTime(exam, questionId):
        """
        Calculates the candidate times for a specific question ID within an exam.
        """
        durations = {}
        candidates = exam.candidates
        for can in candidates:
            for question in can.questions:
                if question.questionId == questionId:
                    duration_seconds = question.durationSeconds
                    if questionId not in durations:
                        durations[questionId] = []
                    durations[questionId].append(duration_seconds)

        return durations.get(questionId, [])

    @classmethod
    def getFigure(cls, exam: Exam, title, threshold=0.5, max_rows=3, num_bins=20):
        """
        Get figure creates the figure for TaskDurations and returns it as a figure
        """
        taskDurations = cls.extractFromExam(exam)
        task_groups_list = cls._create_TG(taskDurations, num_bins=num_bins)

        fig, axes = plt.subplots(
            len(task_groups_list), 1, figsize=(8, 6 * len(task_groups_list)))
        if len(task_groups_list) == 1:
            axes = [axes]  # Ensure axes is always iterable

        for i, taskDuration in enumerate(taskDurations):
            question_id = taskDuration.questionID
            correctPortion = taskDuration.correctPortion
            color = Box.get_color(correctPortion)
            time_intervals = next(iter(task_groups_list[i].values()))
            intervals = [interval['duration']
                         for interval in time_intervals.values()]
            candidate_counts = [interval['candidates']
                                for interval in time_intervals.values()]
            bar_width = (max(intervals) - min(intervals)) / \
                len(intervals) if intervals else 1
            ax = axes[i]
            ax.bar(intervals, candidate_counts, width=bar_width,
                   align='center', color=color, edgecolor='black')
            ax.margins(x=0.05)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Number of Candidates')
            ax.set_title(f'{exam.getQuestionNr(question_id)}')

        plt.tight_layout()
        return fig

    @classmethod
    def _create_TG(cls, taskDurations, num_bins):
        """
        This method categorizes the durations into intervals and counts the number of candidates falling into each interval 
        for each task/question. The resulting list contains dictionaries representing groups of task durations for visualization.

        Args:
            cls: Class reference.
            taskDurations: List of TaskDuration instances.
            num_bins (int): Number of bins for grouping task durations.

        Returns:
            A list containing dictionaries representing task duration groups.

        """
        task_groups_list = []
        for taskDuration in taskDurations:
            question_id = taskDuration.questionID
            durations = taskDuration.candidate_time
            max_duration = max(durations) if durations else 0
            bin_size = max_duration / num_bins if max_duration else 1
            task_duration_group = {question_id: {
                i: {'duration': i * bin_size, 'candidates': 0} for i in range(num_bins)}}

            for duration in durations:
                group = min(int(duration / bin_size), num_bins - 1)
                task_duration_group[question_id][group]['candidates'] += 1
            task_groups_list.append(task_duration_group)
        return task_groups_list
