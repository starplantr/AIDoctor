#txt파일에 저장되어있는 질문리스트(prompt)를 가져온다. 모듈화를 한다.
def readquestion1():
    with open("./question1.txt", "r", encoding='UTF8') as file:
        question = file.read()
    return "\n"+question


def readquestion2():
    with open("./question2.txt", "r", encoding='UTF8') as file:
        question = file.read()
    return question


def readquestion3():
    with open("./question3.txt", "r", encoding='UTF8') as file:
        question = file.read()
    return question
