import pickle

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
            if w in eval_data:
                eval_data[w].append(p)
            else:
                eval_data[w] = [p]
    return eval_data


def save_obj(file, obj):
    with open(file, 'wb') as obj_file:
        pickle.dump(obj, obj_file)


def load_obj(file):
    with open(file, 'rb') as obj_file:
        obj = pickle.load(obj_file)
    return obj
