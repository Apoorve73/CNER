import pandas as pd


def query_db_train_formatter(path: str):
    sentence_list = []
    with open(path) as f:
        lines = f.readlines()
        sentence = ""

        for string in lines:

            if string != "\n":
                word_list = string.rstrip('\n').split('\t')
                sentence = sentence + " " + word_list[1]

            else:
                if sentence:
                    sentence_list.append(sentence.strip())
                sentence = ""

    return sentence_list


def write_to_csv(array: list, filename: str):
    if len(array) > 0 and type(array[0]) == str:
        array_n = list()
        for string in array:
            array_n.append([string])
        print(array_n)

    columns = ['query']
    dataframe = pd.DataFrame(array_n, columns=columns)
    dataframe.to_csv(filename)


sentences_array = query_db_train_formatter('train/query_db.txt')
write_to_csv(sentences_array, "train/query_db.csv")
