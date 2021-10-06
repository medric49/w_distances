def read_glossary(glossary_file):
    glossary = {}
    with open(glossary_file, 'r') as glossary_file:
        lines = glossary_file.read().split('\n')
        lines.remove('')
        for line in lines:
            f, w = line.strip().split(' ')
            glossary[w] = int(f)
    return glossary


def read_eval_file(eval_file):
    eval_data = {}
    with open(eval_file, 'r') as eval_file:
        lines = eval_file.read().split('\n')
        lines.remove('')
        for line in lines:
            w, p = line.split('\t')
            eval_data[w] = p
    return eval_data