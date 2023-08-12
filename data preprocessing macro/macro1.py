import os
file_names_txt = os.listdir("Knowledge DB")
file_names = []

for i in range(len(file_names_txt)):
    file_names.append(file_names_txt[i][:-4])

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error : creating directory. ' + directory)

def split_text(text, keyword = "Case"):
    parts = text.split(keyword)
    # Remove empty strings and strip leading/trailing spaces
    parts = [part.strip() for part in parts if part.strip()]
    return parts

for file_name in file_names:
    #각각의 질병에 대하여 Data DB 폴더 속에 해당 질병의 폴더를 만들고 그 안에 15개의 파일을 만들어줄 것이다.
    createFolder('Context DB\\' + file_name)

    diseasePath = "Knowledge DB" + "\\"+ file_name + ".txt"
    #print("reading file name : " + full_path_file_name)

    with open(diseasePath, encoding='UTF-8') as file:
        knowledge_list = file.readlines()
        diseaseKnowledge = ' '.join(knowledge_list)
        #Disease DB 폴더의 txt 파일을 열고 내용을 text 변수에 담았음
        #if full_path_file_name == 'Disease DB\Achalasia.txt': print(text)
    
    problemPath = 'problem DB'+ "\\" + file_name + '.txt'
    with open(problemPath, encoding= 'UTF-8') as file:
        problem_list = file.readlines()

    problem = ' '.join(problem_list)
    results = split_text(problem)

    for i, part in enumerate(results,1):
        part = part.splitlines()[2]
        i_th_case = "Context DB" + "\\" + file_name + "\\" + file_name + " case" + str(i) + ".txt"
        with open(i_th_case, 'w', encoding= 'UTF-8') as f:
            #temp = diseaseKnowledge.append(part)

            temp = diseaseKnowledge + "\n" * 2  + part
            #print(temp)
            f.write(temp)

        f.close()
