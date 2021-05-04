from header import *
import header as h

client_id = "SS94KPovEIiHWaJqW4k2" # 개발자센터에서 발급받은 Client ID 값
client_secret = "PXIqX40BAI" # 개발자센터에서 발급받은 Client Secret 값

# 텍스트 파일을 받아서 번역하여 번역본을 다른 텍스트 파일에 적어서 저장해주는 함수
# what_to_translate : 음성을 텍스트로 변환한 파일 , translate_result : 번역한 파일
def Translate(what_to_translate, translate_result): 

    what_to_translate=output_filepath+what_to_translate
    translate_result=output_filepath+translate_result

    #번역할 텍스트 불러와서 읽기
    with open(what_to_translate,'r',encoding='utf-8') as f:
        translate_this = f.read()

    #결과를 옮길 텍스트 파일 지정하여 출력 결과를 텍스트 파일에 write
    origin=sys.stdout
    sys.stdout = open(translate_result, 'w')
    encText = urllib.parse.quote(translate_this)
    from_language=h.video_language[0:2]
    to_language=h.translate_language[0:2]

    # source=ko : 한국말로 받는다 / target=en : 영어로 번역
    data = "source=" + from_language + "&target=" + to_language + "&text=" + encText
    
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode() #결과 코드를 받아오는데에 성공하면 200을 리턴

    #결과 코드를 성공적으로 받아왔다면
    if(rescode==200):
        response_body = response.read() #결과 코드 읽어와서 response_body에 저장. 이때 번역본 외의 다양한 코드들이 섞여있음
        a = response_body.decode('utf-8') # a는 str type
        sentence = json.loads(a) #json.loads 함수를 이용하여 dict type 으로 변환
        print(sentence['message']['result']['translatedText']) #섞여있는 코드들 중 번역본만 출력이 되고 그 외에는 출력이 안되도록 한다.
        sys.stdout=origin
        f.close()
        print("Translate success")
    else:
        print("Error Code:" + rescode)

#Translate('E://운영체제/script.txt', 'E://운영체제/script_result.txt', 'ko', 'en') #1번째 번역할 텍스트
#Translate('E://운영체제/translate2.txt', 'E://운영체제/translate2_result.txt', 'ko', 'en') #2번째 번역할 텍스트