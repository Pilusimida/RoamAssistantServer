import pandas as pd


def readCSV(filename: str):
    d = pd.read_csv(r'EA/resources/' + filename, sep=',',header='infer')
    arr = d.values[0::, 1::]
    return arr


if __name__ == "__main__":
    h, array = readCSV('bus-cost.csv')
    print(h)
    print(array)
    print(type(array))
    print(len(array[0]))
