from flask import Flask,request, render_template,session,redirect,url_for
from flask_wtf.csrf import CSRFProtect
import os
import openai
from pymongo.mongo_client import MongoClient
import pymongo
import certifi
import question as q
from datetime import timedelta,datetime
import re

#openai.api_key = os.getenv("OPENAI_API_KEY")

API_KEY = "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" #gpt api이용키
openai.api_key = API_KEY #gpt api이용키
app = Flask(__name__, template_folder="templates") #플라스크실행
#uri = "mongodb+srv://kastor:1234@gptservice.hxiwlfg.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://jinsig98:yjs13622!@aidoctor.hkihclo.mongodb.net/?retryWrites=true&w=majority" #몽고디비서버
ca = certifi.where()

# Create a new client and connect to the server
client = MongoClient(uri,tlsCAFile=ca)#DB에 연결한다.

# Send a ping to confirm a successful connection
try: #DB에 연결되어있는지 확인한다.
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route("/") #환영합니다를 띄워주고 login페이지로 이동한다
def Index():
    nextURL = f'<script>alert("환영합니다!");document.location.href=\"/welcome\"</script>'
    return nextURL

def makequestions(s,username):
    questiondb = client.question
    questions = s.split("\n")
    cnt = session['count']
    hour = session['hour']
   
    for i, q in enumerate(questions):
        if q == '':
            del questions[i]
    
    for i, q in enumerate(questions): #세부 질문을 만든다.
        if q != '':
            detailsJSON = {"id": i+1, "question" : q, "answer": "","username":username,"cnt":cnt, "questionhour":hour}
            questiondb.details.insert_one(detailsJSON)

def session_setting(): #세션을 셋팅한다.
    session['count'] = 0
    session['chat_history'] =''

@app.route('/welcome')
def welcome():
    return render_template('index.html')

@app.route("/gpt/details") 
def GPTmiddle():
    if 'username' not in session: #로그인 되어있는지 확인
        nextURL = f'<script>alert("login please");document.location.href=\"/login\"</script>'
        return nextURL
    username = session['username']
    now_hour = session['hour']
    session['nowhour'] = session['hour']
    questionDB = client.question
    cnt = session['count']
    questionhour = session['hour']
    detailscnt = questionDB.details.count_documents({"cnt": cnt,"username" : username}) #전체 데이터 갯수를 센다. 이유는  url gpt/details1/1 1/2 1/3 ... 1/10 이후 2/1로 넘어가기 위해
    msg = ""
    for i in range(1,detailscnt+1):#detailscnt + 1
        onesentence = questionDB.details.find_one(
            {"id": i, "cnt": cnt, "questionhour": questionhour})  # 데이터 한 개 불러오기
        msg += onesentence["question"].replace("\n", "") + onesentence["answer"].replace("\n", "")+"\n" #2번째 질문 다듬기
    reform_message = setting_message(user_message=msg) #질문을 넣는다
    gptResponse = gpt_35_kor(reform_message) #인공지능을 학습한다.
    print("gptResponse : ", gptResponse)
    makequestions(gptResponse,username)
    cnt2 = session['count']
    print("cnt2 : ",cnt2)
    now = datetime.now()
    now_text = now.strftime("%Y%m%d")  # 언제 했는지 저장

    if cnt2 == 3:
###########################################여기부터 해야함 지금 final 답변을 db에 저장하도록 구현해야함 2023.05.22/1:39PM
        question = {'username': username, "gptresponse": gptResponse,
                    "datetime": now_text, "questionhour": now_hour}
        questionDB.finalanswer.insert_one(question)
        nextURL = f'<script>document.location.href=\"/gpt\"</script>'

    else:
        nextURL = f'<script>document.location.href=\"/gpt/details/{cnt2}/1\"</script>'

    return nextURL 

@app.route('/gpt/details/<int:cnt>/<int:detail_id>',methods=["GET","POST"]) #detail에서 입력받은 값을 토대로 반복할 함수
def GPTdetail(cnt,detail_id):  #cnt와 detail_id를 가져온다.
    if 'username' not in session: #로그인 되어있는지 확인한다.
        nextURL = f'<script>alert("login please");document.location.href=\"/login\"</script>'
        return nextURL
    username = session['username']
    now_hour = session['hour']
    print(username)
    questionDB = client.question
    detailscnt = questionDB.details.count_documents({"cnt":cnt,"username":username,"questionhour" : now_hour})
    if request.method =="GET": #해당 cnt와 detail_id로 한 문장 단위로 끊어져있는 질문 목록을 가져온다.
        result = questionDB.details.find_one(
            {'id': detail_id, 'cnt': cnt, "questionhour": now_hour})
        if result:
            return render_template('gptdetails.html', username=username, result=result['question'])
        else:
            return render_template('gptdetails.html',username=username)
    elif request.method =="POST": 
        answer = request.form['user_message']
        query = {"id":detail_id,"answer":"","username":username} 
        newvalues = {"$set": {"id": detail_id,  
                              "answer": answer, "username": username}} #기존에 answer=""로 해놨는데 user가 답변을 함으로써 해당 질문 한 개의 답을 user가 입력한 답으로 json형식을 만든다.
        result = questionDB.details.update_one(query,newvalues) #DB를 update한다.
        print("detail_id : ", detail_id)
        print("detailcnt : ",detailscnt)
        if detail_id != detailscnt:
            nextURL = f'<script>document.location.href=\"/gpt/details/{cnt}/{detail_id+1}\"</script>' #다음 페이지로 이동한다.
        else:
            nextURL = f'<script>document.location.href=\"/gpt/details\"</script>'
        return nextURL


@app.route("/logout",methods=['GET','POST'])
def Logout(): #session에서 pop을 함으로써 logout이 됨.
    if request.method == 'GET':
        session.pop('username')
        return redirect(url_for("Login"))


@app.route('/gpt',methods=['GET','POST'])
def GPTservice():
    if 'username' not in session: #로그인이 되어있는지 확인한다.
        nextURL = f'<script>alert("로그인 해주세요");document.location.href=\"/login\"</script>'
        return nextURL
    username = session['username'] #로그인이 되어있으면 로그인 된 user의 이름을 가져온다.
    session['username'] = username
    questiondb = client.question #quetion collection을 만든다.
    now = datetime.now()   
    now_text = now.strftime("%Y%m%d")  #년월일을 가져온다.
    now_hour = now.strftime("%H:%M:%S") #시간을 가져온다.
    session["hour"] = now_hour

    if request.method == "POST":
        session_setting() #세션값을 셋팅해주고
        user_input = request.form['user_message'] #user가 입력한 profile & chief complient? 그거를 가져온다
        print(user_input)
        reform_message = setting_message(user_message=user_input) #message를 다듬는다.
        print("reform_message",reform_message)
        gptResponse = gpt_35_kor(reform_message) #gpt에 넣고 돌린다.
        makequestions(gptResponse,username) #gpt결과값을 한 문장 단위로 끊어서 DB에 저장한다.
        print(f'gptResponse : {gptResponse}')
        question = {'username': username,"userinput": user_input, "gptresponse": gptResponse,"datetime": now_text, "questionhour" : now_hour} #맨 처음 입력한 profile과 chief complient를 저장한다.
        questiondb.questioninfo.insert_one(question)
        #cnt_session()
        cnt = session['count']
        nextURL = f'<script>document.location.href=\"/gpt/details/{cnt}/1\"</script>' #세부 질문 리스트 페이지로 이동한다.
        return nextURL

    elif request.method =="GET":
            if "nowhour" in session:
                print("hour",session['nowhour'])   
                user_history = questiondb.questioninfo.find_one(
                    {"username": username, "datetime": now_text, "questionhour": session['nowhour']})  #맨 처음 입력한 profile과 chief complient를 가져온다.
                chat_history = questiondb.finalanswer.find_one(
                    {"username": username, "datetime": now_text, "questionhour": session['nowhour']})  #최종 결과값을 가져온다
                print(user_history)
                print(chat_history)
                if chat_history:
                    print("True")
                    return render_template('chatgpt.html', name="gpt", ai_history=chat_history['gptresponse'], user_history=user_history['userinput'], username=username) #front에 ai_history변수에 gpt최종 응답값을 넣고 user_history에 우리가 #맨 처음 입력한 profile과 chief complient를 넣고 front로 전달한다.
            else:
                return render_template('chatgpt.html', name="gpt", username=username) 


@app.route("/login", methods=["GET","POST"])
def Login():
    db = client.user
    if request.method == "GET":
        return render_template("login.html")
    elif request.method =="POST":
        userid = request.form["userid"] #front에서 userid값을 가져온다.
        userpw = request.form["password"] #front에서 userpw값을 가져온다.
        #print(userid)
        #print(userpw)
        result = db.userinfo.find_one({'userid': userid, 'userpw': userpw}) #DB에 userid와 userpw를 비교한 후 계정이 있으면 가져온다.
        if result != None: #"NoneType": #정상적으로 로그인 성공한 경우
            session['username'] = result['username']
            session_setting()#세션값 0으로 초기화

        else:
            nextURL = f'<script>alert("login failed!");document.location.href=\"/login\"</script>'  #실패
            return nextURL


        return redirect(url_for("GPTservice"))


@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == "GET":
        return render_template("register.html") #html파일을 return 해준다.
    elif request.method == "POST":
        db = client.user #db와 연결을 하고 'user'라는 이름의 collection을 만든다.
        username = request.form["signup_username"] #front에서 username값을 가져온다.
        userid = request.form["signup_userid"] #front에서 userid값을 가져온다.
        userpw = request.form["signup_password"] #front에서 userpw값을 가져온다.
        user = {'username':username,"userid":userid,"userpw":userpw}
        userExist = db.userinfo.find_one(user)
        if userExist: #회원가입을 할 떄 이미 해당 이름의 유저가 있는 상황이면 회원가입이 불가능하도록 한다.
            nextURL = f'<script>alert("already registered user!");document.location.href=\"/register\"</script>' 
            return nextURL

        
        else:
            db.userinfo.insert_one(user)
            print(username,userid,userpw)
            return redirect(url_for("Login"))


def setting_message(user_message):

    # 미리 세팅된 메시지를 통해 질문을 다듬는다.

    # Profile : 나이, 성별
    # Chief complaint : 주소 --> usermessage
    text1 = q.readquestion1()
    text2 = q.readquestion2()
    text3 = q.readquestion3()

    # 세션을 이용해 count 관리
    count = session['count']
    if count == 0:
        # 미리 세팅된 메시지와 유저 메시지를 결합
        prompt = user_message + text1
        session['count'] = 1
        a = session['count']
        print(f'session1의 값은 {a}')
    elif count == 1:
        prompt = text2 + user_message
        session['count'] = 2

        a = session['count']
        print(f'session2의 값은 {a}')
    elif count == 2:
        prompt = text3 + user_message
        session['count'] = 3

        a = session['count']
        print(f'session3의 값은 {a}')
    else:
        prompt = user_message

    return prompt


def gpt_35_kor(prompt): #gpt3.5-turbo를 통해 chatgpt에 text를 넣고 돌린다.

    # gpt3.5 호출
    # 텍스트를 콘텐츠로 전달
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # AI 대답 듣고
    for result in response.choices:
        global resulttext
        # content 까지 점으로 찍어 내려가면 안되더라
        resulttext = response.choices[0].message
        # 체크, AI 영어 대답 프린트
        #print("AI: {}".format(resulttext))

    return resulttext.content


def cnt_session(): #session['cnt']를 설정한다.
    count = session['count'] 
    if count == 0:
        # 미리 세팅된 메시지와 유저 메시지를 결합
        session['count'] = 1
        a = session['count']
        print(f'session1의 값은 {a}')
    elif count == 1:
        session['count'] = 2

        a = session['count']
        print(f'session2의 값은 {a}')
    elif count == 2:
        session['count'] = 3

        a = session['count']
        print(f'session3의 값은 {a}')



if __name__ == '__main__':
    app.secret_key = os.urandom(24) #random으로 secretkey를 설정한다. session생성을 위해
    csrf = CSRFProtect()  #csrf설정을 한다. 웹 보안을 위해
    csrf.init_app(app)
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
        minutes=10) #session지속시간을 10분으로 설정한다.
    app.run(debug=True)
