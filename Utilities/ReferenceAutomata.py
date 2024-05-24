from Utilities.APTA import APTA
from FilesReader.matrix_reader import buildGraphFromMatrix,draw


def get_reference_DFA(input_file, counter):
    # output_file = build_adjs_matrix(input_file, counter)
    G, alphabet = buildGraphFromMatrix(input_file)
    draw(G, f"output/RefrencedAuotmata{counter}.png")

    apta_obj = APTA()
    apta_obj.G = G
    apta_obj.root = 'V0'
    apta_obj.alphabet = alphabet
    return apta_obj