import os, shutil
import random

"""
version: 3.0
"""

def import_input(input_file):
    accepted = []
    rejected = []
    reading_status = ''

    input = [l.strip().lower() for l in open(input_file).readlines()]

    for line in input:

        if not line or line.strip().startswith("#") or line.strip() == '':
            continue

        if line in ['postive sequences', 'positive sequences', 'negative sequences', 'numbre of transitions:']:
            reading_status = line
            continue

        if reading_status in  ['positive sequences', 'postive sequences']:
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').split(',') if l != ""]
            accepted.append(nodes)
        elif reading_status == 'negative sequences':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').split(',') if l != ""]
            rejected.append(nodes)


#    build_adjs_matrix('evaluation/exp.txt')
    return accepted, rejected

def import_input2(input_file, counter=1):
    accepted = []
    rejected = []
    train_positive_traces = []
    train_negative_traces = []
    test_positive_traces = []
    test_negative_traces = []
    reading_status = ''

    input = [l.strip().lower() for l in open(input_file).readlines()]
    for line in input:

        if not line or line.strip().startswith("#") or line.strip() == '':
            continue

        if line in ['postive sequences', 'positive sequences', 'negative sequences']:
            reading_status = line
            continue
        if line == '------------------':
            train_positive_traces, train_negative_traces, test_positive_traces, test_negative_traces = split_dataset(
                accepted, rejected)
            build_adjs_matrix(input_file, f'input/automata{counter}.txt')
            write_to_file(f'input/automata{counter}.txt', train_positive_traces, train_negative_traces,
                          test_positive_traces, test_negative_traces)
            counter += 1
            accepted = []
            rejected = []
        elif reading_status in  ['positive sequences', 'postive sequences']:
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').split(',') if l != ""]
            accepted.append(nodes)
        elif reading_status == 'negative sequences':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').split(',') if l != ""]
            rejected.append(nodes)

    return train_positive_traces, train_negative_traces, test_positive_traces, test_negative_traces

def build_adjs_matrix(input_file, output_file):
    # open original file
    input = [l.strip().lower() for l in open(input_file).readlines()]

    # create file named "matrixOfRefrencedAuotmata.adjlist"
    # W: will overwirte any previous contents
    f = open(output_file, "w")

    for line in input:
        if not line or line.strip().startswith("#") or line.strip() == '':
            continue
        elif line in ['postive sequences', 'positive sequences', 'negative sequences', 'numbre of transitions:']:
            break

        list = [l.strip().upper() for l in line.replace(' - ',',').replace(' -> ',',').split(',') if l != ""]
        row = list[0].split('<', 1)[0] + ' ' +list[2].split('<', 1)[0] + ' ' + list[1] +'\n'
        f.write(row)

    f.close()
# from input_reader2 import *

def split_dataset(accepted_traces, rejected_traces):
    testing_PosSize = round(len(accepted_traces) * 0.3)
    training_PosSize = len(accepted_traces) - testing_PosSize

    train_positive_traces = random.sample(accepted_traces, training_PosSize)

    # test_positive_traces = random.choices(accepted_traces, k=testing_PosSize)
    test_positive_traces = []
    for trace in accepted_traces:
        if trace not in train_positive_traces:
            test_positive_traces.append(trace)

    testing_NegSize = round(len(rejected_traces) * 0.3)
    training_NegSize = len(rejected_traces) - testing_NegSize
    train_negative_traces = random.sample(rejected_traces, training_NegSize)
    # test_negative_traces = random.choices(rejected_traces, k=testing_NegSize)
    test_negative_traces = [trace for trace in rejected_traces if trace not in train_negative_traces]

    return train_positive_traces, train_negative_traces, test_positive_traces, test_negative_traces

def write_to_file(output_file, traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp):
    f = open(output_file, "a")
    f.write(f"training positive:\n")
    for examp in traningPosExmp:
        f.write(f'{examp}\n')

    f.write(f"training negative:\n")
    for examp in trainingNegExmp:
        f.write(f'{examp}\n')

    f.write(f"evaluation positive:\n")
    for examp in evalPosExmp:
        f.write(f'{examp}\n')

    f.write(f"evaluation negative:\n")
    for examp in evalNegExamp:
        f.write(f'{examp}\n')

    f.close()

def prepare_data(inputfile, counter):
    traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp = import_input2(inputfile, counter)
    # traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp = split_dataset(accepted_traces, rejected_traces)

    # build_adjs_matrix(inputfile, outputfile)
    # write_to_file(outputfile, traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp)
    # traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp  = import_input2("input/traces.txt")\
    return traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp

def GetTrainingEvaluationData(input_file):
    trainingPositive = []
    trainingNegative = []
    evaluationPositive = []
    evaluationNegative = []
    reading_status = ''

    input = [l.strip().lower() for l in open(input_file).readlines()]

    for line in input:

        if not line or line.strip().startswith("#") or line.strip() == '':
            continue

        if line in ['training positive:', 'training negative:', 'evaluation positive:', 'evaluation negative:']:
            reading_status = line
            continue

        if reading_status == 'training positive:':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').replace('\'','').split(',') if l != ""]
            trainingPositive.append(nodes)
        elif reading_status == 'training negative:':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').replace('\'','').split(',') if l != ""]
            trainingNegative.append(nodes)
        elif reading_status == 'evaluation positive:':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').replace('\'','').split(',') if l != ""]
            evaluationPositive.append(nodes)
        elif reading_status == 'evaluation negative:':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').replace('\'','').split(',') if l != ""]
            evaluationNegative.append(nodes)

    return trainingPositive, trainingNegative, evaluationPositive, evaluationNegative

def clean_folder(folder = 'output'):
    # folder = 'output'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == '__main__':
    clean_folder()
    input_folder = 'fromEclips'
    counter = 1
    # Process each file in the input folder
    for file_name in os.listdir(input_folder):
        # Construct the input and output file paths
        input_file_path = os.path.join(input_folder, file_name)

        # Process the file
        prepare_data(input_file_path, counter)
        counter+=10
