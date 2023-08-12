#txt file input find index of target word
import os
import pandas as pd
file_names = os.listdir("One line DB ver1") #46개의 질병들 list

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error : creating directory. ' + directory)

def find_word_start_indices(sentence, target_words):
    indices = []
    sentence = sentence.lower()

    #1 맨 뒤의 단어가 축약어일때
    isCap = target_words.split()[-1].isupper()

    if(isCap):
        target_words = target_words.lower().split()
        target_words[:-1] = [' '.join(target_words[:-1])]

    #2 Gastroenteritis viral bacterial
    elif(target_words == 'Gastroenteritis viral bacterial'):
        target_words = ['viral', 'bacterial']

    elif(target_words == 'Esophageal Rupture Boerhaave Syndrome'):
        target_words = ['esophageal rupture', 'boerhaave syndrome']

    elif(target_words == 'Liver Cirrhosis'):
        target_words = ['cirrhosis']

    elif(target_words == 'Food Intolerances Lactose Intolerance'):
        target_words = ['food intolerance', 'lactose intolerance']

    #3 일반적인 단어처리
    else:
        target_words = target_words.lower().split()
        target_words[:] = [' '.join(target_words[:])]

    for target_word in target_words:
        start_index = 0
        while start_index < len(sentence):
            index = sentence.find(target_word, start_index)
            if index == -1:
                break
            indices.append(index)
            start_index = index + 1

    return indices

df = pd.DataFrame(
    {
        "Context": [],
        "Question": [],
        "Answer": [],
        "Answer start index": []
    }
)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
context_list = []
for file_name in file_names:
    with open('Context_v2 DB'+'\\'+ file_name +".txt", 'r', encoding='UTF-8') as file:
        temp = file.read()
        for _ in range(15):
            context_list.append(temp)

df["Context"] = context_list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
question_list = []
for file_name in file_names:
    #OnelineProblemDBPath = os.listdir('problem one line')
    for i in range(1,16):
        #i_th_case = problem one line/질병명/질병명 case[i].txt
        i_th_case = "problem one line" + "\\" + file_name + "\\" + file_name + " case" + str(i) + ".txt"

        with open(i_th_case, 'r', encoding= 'UTF-8') as file:
            temp = file.read()
            question_list.append(temp)

df["Question"] = question_list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Answer_list = []
for file_name in file_names:
    for _ in range(15):
        Answer_list.append(file_name)
df["Answer"] = Answer_list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
answer_indices = []
for file_name in file_names: #각 질병에 대하여
    file_name_ext = file_name + '.txt'
    OnelineDBPath = os.path.join('Context_v2 DB', file_name_ext)
    with open(OnelineDBPath, 'r', encoding='UTF-8') as file:
        temp = file.read()
        indice = find_word_start_indices(temp, file_name)
        for _ in range(15):
            answer_indices.append(indice)

df_ = pd.DataFrame(answer_indices)
df['Answer start index'] = df_[df_.columns[0:]].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
#df['Answer start index'] = df['Answer start index'].replace('\.0',',',regex=True).astype(int)
df['Answer start index'] = df['Answer start index'].replace('\.0',',',regex=True)
#print(df)

df.to_csv('C:\\Users\\Lenovo\\OneDrive - 한양대학교\\의료용 챗봇\\makingmacro\\data.csv',sep=',',encoding='UTF-8')

#%%
