#txt file input find index of target word
import os
import pandas as pd
file_names = os.listdir("One line DB ver1") #46개의 질병들 list

def find_word_start_indices(sentence, target_words):
    indices = []
    sentence =  sentence.lower()
    
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
        target_words = ['food intolerance','lactose intolerance']

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
            indices.append((index))
            start_index = index + 1
    return indices

answer_indices = []
asdfas = []
for file_name in file_names: #각 질병에 대하여
    #createFolder('One line DB ver1\\' + file_name)
    #print(file_name)
    OnelineDBPath = os.listdir(os.path.join('One line DB ver1',file_name))
    for i, problemFile in enumerate(OnelineDBPath,1):
        #i_th_case = One line DB/질병명/질병명 case[i].txt
        i_th_case = "One line DB ver1" + "\\" + file_name + "\\" + file_name + " case" + str(i) + ".txt"

        with open(i_th_case, 'r', encoding= 'UTF-8') as file:
            temp = file.read()
            indice = find_word_start_indices(temp, file_name)
            try:
                asdfas.append(indice[1])
            except:
                asdfas.append(file_name)
            answer_indices.append(indice)


print(asdfas)       

#print(len(answer_indices))
df = pd.DataFrame(
    {
        "Context": [],
        "Question":[],
        "Answer": [],
        "Answer start index": []
    }
)
context_list = []

for file_name in file_names:
    OnelineDBPath = os.listdir(os.path.join('One line DB ver1',file_name))
    for i, problemFile in enumerate(OnelineDBPath,1):
        #i_th_case = One line DB/질병명/질병명 case[i].txt
        i_th_case = "One line DB ver1" + "\\" + file_name + "\\" + file_name + " case" + str(i) + ".txt"

        with open(i_th_case, 'r', encoding= 'UTF-8') as file:
            temp = file.read()
            context_list.append(temp)

df["Context"] = context_list
df["Question"] = ["What is the most likely diagnosis of the patient?" for _ in range(len(context_list))]

# Answer_list = []
# for file_name in file_names:
#     for _ in range(15):
#         Answer_list.append(file_name)
# df["Answer"] = Answer_list
# df_ = pd.DataFrame(answer_indices)
# df['Answer start index'] = df_[df_.columns[0:]].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
# df['Answer start index'] = df['Answer start index'].replace('\.0',',',regex=True).astype(int)
# print(df)

#df.to_csv('C:\\Users\\VIP\\Desktop\\makingmacro\\data.csv',sep=',',encoding='UTF-8')