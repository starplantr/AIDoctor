#Make the Knowledge DB into oneline
import os
file_names_txt = os.listdir("Knowledge DB")
file_names = []

for i in range(len(file_names_txt)):
    file_names.append(file_names_txt[i][:-4])

# def createFolder(directory):
#     try:
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#     except OSError:
#         print('Error : creating directory. ' + directory)

for file_name in file_names:
    #각각의 질병에 대하여 Data DB 폴더 속에 해당 질병의 폴더를 만들고 그 안에 15개의 파일을 만들어줄 것이다.

    diseasePath = "Knowledge DB" + "\\"+ file_name + ".txt"
    diseaseKnowledge = " "
    with open(diseasePath, encoding='UTF-8') as file:
        knowledge_list = file.readlines()
        diseaseKnowledge = ' '.join(knowledge_list).replace("\n", "").strip()
        file.close()

    path = 'Context_v2 DB' + '\\' + file_name + '.txt'
    with open(path, 'w', encoding='UTF-8') as f:
        f.write(diseaseKnowledge)
        f.close()
#%%
