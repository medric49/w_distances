from distances import *
if __name__ == '__main__':
    distance = JaccardDistance(nb_char=2)

    print(distance('wave', 'issu'))
