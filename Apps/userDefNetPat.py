from Pattrens.negative_patterns2 import get_negative_patterns
from Utilities.APTA import APTA
from Utilities.APTA_labeledBYRefDFA import LabeledAPTA
from Utilities.Learner import Learner
from Utilities.ReferenceAutomata import get_reference_DFA
from Pattrens.SatPatterns_RandFSM import discover_patterns_fromTraces
from Evaluation.evaluation import Evaluation
from FilesReader.input_reader import *
from FilesReader.matrix_reader import *
import csv

if __name__ == '__main__':
    clean_folder()
    input_folder = "Evaluation/input-10states"
    counter = 1

    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)

        reference_DFA = get_reference_DFA(input_file_path, counter)
        User_defined_negative_patterns = get_negative_patterns(reference_DFA)
        traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp  = GetTrainingEvaluationData(input_file_path)

        # building the tree
        apta = APTA()
        apta.build_APTA(traningPosExmp, trainingNegExmp)

        learned_DFA = Learner(apta)
        learned_DFA.run_EDSM_usrDefNegPat_learner(User_defined_negative_patterns)
        # learned_DFA.draw2(f'automata{counter}')

        eval = Evaluation(learned_DFA, evalPosExmp, evalNegExamp)
        true_positive, true_negative, false_positive, false_negative, precision, recall, F_measure, Accuracy = eval.evaluate()

        data = [
            [file_name, len(traningPosExmp), len(trainingNegExmp), len(evalPosExmp), len(evalNegExamp), true_positive,
             true_negative,
             false_positive, false_negative, precision, recall, F_measure, Accuracy]]
        file_path = 'NegPat10StatesData2.csv'
        # Write data to CSV file
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print(f'Automata{counter}')
        counter += 1
