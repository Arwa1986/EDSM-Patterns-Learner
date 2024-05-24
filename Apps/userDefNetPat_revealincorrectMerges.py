from Utilities.APTA import APTA
from Utilities.APTA_labeledBYRefDFA import LabeledAPTA
from Utilities.FSM import FSM
from Utilities.ReferenceAutomata import get_reference_DFA
from Evaluation.evaluation import Evaluation
from FilesReader.input_reader import *
from FilesReader.matrix_reader import *



if __name__ == '__main__':
    clean_folder()
    input_file_path='input-10states/automata20.txt'
    reference_DFA = get_reference_DFA(input_file_path, 1)
    traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp = GetTrainingEvaluationData(input_file_path)
    LabeledAPTA = LabeledAPTA(reference_DFA)
    LabeledAPTA.build_APTA(traningPosExmp, trainingNegExmp)
    LabeledAPTA.draw_multiDigraph()

    apta = APTA()
    apta.G = LabeledAPTA.G
    apta.root = 0
    apta.alphabet = LabeledAPTA.alphabet

    fsm = FSM(apta, [], 0, reference_DFA)
    fsm.run_EDSM_learner()
    fsm.draw()
    eval = Evaluation(fsm, evalPosExmp, evalNegExamp)
    true_positive, true_negative, false_positive, false_negative, precision, recall, F_measure, Accuracy = eval.evaluate()
    print(f'F_measure= {F_measure}')
