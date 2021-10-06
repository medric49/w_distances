from distances import *
if __name__ == '__main__':
    distance = LevenshteinDistance(None, None, 0)

    print(distance.distance('wave', 'issu'))
