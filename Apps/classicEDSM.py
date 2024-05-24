import random
from Utilities.APTA import APTA
from Utilities.Learner import Learner
from Evaluation.evaluation import Evaluation
from FilesReader.input_reader import *
import csv
import os, shutil

def start_learning(traningPosExmp, trainingNegExmp):
    apta = APTA()
    apta.build_APTA(traningPosExmp, trainingNegExmp)
    edsm_DFA = Learner(apta)
    edsm_DFA.run_EDSM_learner()

    return edsm_DFA
if __name__ == '__main__':

    clean_folder()
    input_folder = 'Evaluation/input-5states'
    counter = 1
    # inputfile = "input/PosNegExamples.txt"

    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)
        traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp = GetTrainingEvaluationData(input_file_path)

        # building the tree
        apta = APTA()
        apta.build_APTA(traningPosExmp, trainingNegExmp)

        learned_DFA = Learner(apta)
        learned_DFA.run_EDSM_learner()
        # learned_DFA.draw2(f'automata{counter}')

        eval = Evaluation(learned_DFA, evalPosExmp, evalNegExamp)
        true_positive, true_negative, false_positive, false_negative, precision, recall, F_measure, Accuracy = eval.evaluate()
        # print(f'the root: {edsm_DFA.apta.root}')

        data = [
            [len(traningPosExmp), len(trainingNegExmp), len(evalPosExmp), len(evalNegExamp), true_positive, true_negative,
             false_positive, false_negative, precision, recall, F_measure, Accuracy]]
        file_path = 'Evaluation/CSV-files/EDSM5StatesData.csv'
        # Write data to CSV file
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print(f'Automata{counter}')
        counter+=1
