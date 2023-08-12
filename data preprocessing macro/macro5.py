#Make the Problem DB into oneline
import os
file_names_txt = os.listdir("problem DB")
file_names = []

for i in range(len(file_names_txt)):
    file_names.append(file_names_txt[i][:-4])

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error : creating directory. ' + directory)

def one_sentence(file_name):
    filename = file_name # 텍스트 파일의 경로와 파일명을 지정해주세요.
    full_text = ""
    with open(filename, "r", encoding='UTF-8') as file:
        for line in file:
            sentence = line.strip()  # 문장의 앞뒤 공백을 제거합니다.
            full_text += (" " + sentence)
    return full_text

def split_text(text, keyword = "Case"):
    parts = text.split(keyword)
    # Remove empty strings and strip leading/trailing spaces
    parts = [part.strip() for part in parts if part.strip()]
    return parts

for file_name in file_names:
    #각각의 질병에 대하여 Data DB 폴더 속에 해당 질병의 폴더를 만들고 그 안에 15개의 파일을 만들어줄 것이다.
    createFolder('problem one line\\' + file_name)

    problemPath = 'problem DB'+ "\\" + file_name + '.txt'
    with open(problemPath, encoding= 'UTF-8') as file:
        problem_list = file.readlines()

    problem = ' '.join(problem_list)
    results = split_text(problem)

    for i, part in enumerate(results, 1):
        #print(part)
        part = (part.splitlines()[2] + part.splitlines()[4]).replace('\n',"")
        i_th_case = "problem one line" + "\\" + file_name + "\\" + file_name + " case" + str(i) + ".txt"
        with open(i_th_case, 'w', encoding= 'UTF-8') as f:
            f.write(part)

        f.close()
#%%
