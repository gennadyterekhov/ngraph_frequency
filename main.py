import json
import csv


def csv_to_dict(filepath, delimiter='\t', quotechar='"'):
    """
    Reads data from a CSV file and returns it as a list of dictionaries.

    Args:
        filepath: The path to the CSV file.
        delimiter: The delimiter used in the CSV file (default: ',').
        quotechar: The quote character used in the CSV file (default: '"').

    Returns:
        A list of dictionaries, where each dictionary represents a row in the CSV file.
    """

    data = []
    with open(filepath, 'r', newline='') as csvfile:
        reader = csv.DictReader(
            csvfile, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            data.append(row)
    return data


def getDictionaryAsDict() -> dict:
    filename = 'freqrnc2011.csv'
    return csv_to_dict(filename)


def fillEntriesMap(dct: dict):
    for wordData in dct:
        processWord(wordData['Lemma'], float(wordData['Freq(ipm)']))


def processWord(word: str, freq: float):
    digs = getDigraphsFromWord(word)
    for d in digs:
        addToMap(d, freq)


def getDigraphsFromWord(word: str) -> list:
    l = len(word)
    i = 0
    dig = ''
    digs = []
    while (i < l-1):
        dig = word[i] + word[i+1]
        digs.append(dig.lower())
        i += 1
    return digs


def addToMap(key: str, newVal: float):
    global digraphToEntriesMap

    if key not in digraphToEntriesMap:
        digraphToEntriesMap[key] = 0
    digraphToEntriesMap[key] += newVal


def turnIntoList():
    for key, value in digraphToEntriesMap.items():
        freqList.append(
            {"digraph": key, "freq": value}
        )


def sort():
    freqList.sort(key=sortKey, reverse=True)


def sortKey(ob):
    return ob['freq']


def output():
    handle = open('res.json', 'w')
    handle.write(json.dumps(freqList, ensure_ascii=False))
    handle.close()


digraphToEntriesMap = {}
freqList = []


def main():
    dct = getDictionaryAsDict()
    fillEntriesMap(dct)
    turnIntoList()
    sort()
    output()


if __name__ == '__main__':
    main()
