#txt file input one line of string output
import os
file_names = os.listdir("Context DB")
#print(file_names)

def one_sentence(file_name):
    filename = file_name # 텍스트 파일의 경로와 파일명을 지정해주세요.
    full_text = ""
    with open(filename, "r", encoding='UTF-8') as file:
        for line in file:
            sentence = line.strip()  # 문장의 앞뒤 공백을 제거합니다.
            full_text += (" " + sentence)
    return full_text

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error : creating directory. ' + directory)

for file_name in file_names:
    createFolder('One line DB\\' + file_name)
    
    #problemPath = 'Data DB'+ "\\" + file_name + '.txt' 46개의 질병 list
    #problemPath = os.listdir("problem DB")
    dataDBPath = os.listdir(os.path.join('Data DB',file_name))
    for i, problemFile in enumerate(dataDBPath,1):
        #i_th_case = One line DB/질병명/질병명 case[i].txt
        i_th_case = "One line DB" + "\\" + file_name + "\\" + file_name + " case" + str(i) + ".txt"

        #print(problemFile)
        with open(i_th_case, 'w', encoding= 'UTF-8') as file:
            path_ = os.path.join("Context DB",file_name,problemFile)
            temp_text = one_sentence(path_)
            #print(temp_text)
            file.write(temp_text)