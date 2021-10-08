from distances import *
if __name__ == '__main__':
    distance = JaroDistance(winkler=True)

    print(distance('wave', 'wa'))
