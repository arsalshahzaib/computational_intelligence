import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define fuzzy variables and membership functions
midterm_exam = ctrl.Antecedent(np.arange(0, 101, 1), 'Midterm Exam')
assignments_quizzes = ctrl.Antecedent(np.arange(0, 101, 1), 'Assignments and Quizzes')
final_exam = ctrl.Antecedent(np.arange(0, 101, 1), 'Final Exam')
final_grade = ctrl.Consequent(np.arange(0, 101, 1), 'Final Grade')

# Define membership functions for each fuzzy variable
midterm_exam['Low'] = fuzz.trimf(midterm_exam.universe, [0, 0, 50])
midterm_exam['Medium'] = fuzz.trimf(midterm_exam.universe, [0, 50, 100])
midterm_exam['High'] = fuzz.trimf(midterm_exam.universe, [50, 100, 100])

assignments_quizzes['Low'] = fuzz.trimf(assignments_quizzes.universe, [0, 0, 50])
assignments_quizzes['Medium'] = fuzz.trimf(assignments_quizzes.universe, [0, 50, 100])
assignments_quizzes['High'] = fuzz.trimf(assignments_quizzes.universe, [50, 100, 100])

final_exam['Low'] = fuzz.trimf(final_exam.universe, [0, 0, 50])
final_exam['Medium'] = fuzz.trimf(final_exam.universe, [0, 50, 100])
final_exam['High'] = fuzz.trimf(final_exam.universe, [50, 100, 100])

final_grade['Fail'] = fuzz.trimf(final_grade.universe, [0, 0, 50])
final_grade['Pass'] = fuzz.trimf(final_grade.universe, [0, 50, 100])
final_grade['Merit'] = fuzz.trimf(final_grade.universe, [50, 100, 100])
final_grade['Distinction'] = fuzz.trimf(final_grade.universe, [50, 100, 100])

# fuzzy rules
rule1 = ctrl.Rule(midterm_exam['Low'] & assignments_quizzes['Low'] & final_exam['Low'], final_grade['Fail'])
rule2 = ctrl.Rule(midterm_exam['Medium'] & assignments_quizzes['Medium'] & final_exam['Medium'], final_grade['Pass'])
rule3 = ctrl.Rule(midterm_exam['High'] & assignments_quizzes['High'] & final_exam['High'], final_grade['Distinction'])
rule4 = ctrl.Rule(midterm_exam['Low'] & assignments_quizzes['High'] & final_exam['High'], final_grade['Pass'])
rule5 = ctrl.Rule(midterm_exam['Low'] & assignments_quizzes['Medium'] & final_exam['High'], final_grade['Pass'])

# control system
grading_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

# control system simulation
grading_sim = ctrl.ControlSystemSimulation(grading_ctrl)

# input values
grading_sim.input['Midterm Exam'] = 70
grading_sim.input['Assignments and Quizzes'] = 80
grading_sim.input['Final Exam'] = 90

# Evaluation
grading_sim.compute()

# crisp output value
final_grade_value = grading_sim.output['Final Grade']

# Mapping of the final grade to CGPA
grading_scale = {
    'Fail': 0.0,
    'Pass': 1.3,
    'Merit': 3.0,
    'Distinction': 4.0
}

gpa = grading_scale.get(final_grade_value, 0.0)

# Print the Final Grade and GPA
print("Final Grade:", final_grade_value)
print("GPA:", gpa)
