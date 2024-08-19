import pickle


def load_object(filename):
    with open(filename, 'rb') as file:
        obj = pickle.load(file)
    return obj


def save_object(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file=file)
