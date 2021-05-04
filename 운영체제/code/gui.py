import header as h

from tkinter import *
import os

press=0

# 초기 상태
def init():

    # "input" 폴더 내의 영상들을 "video" 리스트에 추가
    # os.listdir() : 지정한 디렉토리 내의 모든 파일과 디렉토리의 리스트(list)를 리턴
    file_list=os.listdir(h.input_filepath) 
    for file_name in file_list:
        if file_name[-3:] == "mp4":
            h.video.append(file_name[:-4])
    
    # 창 생성
    global win,video_num,l1,l2
    win = Tk()
    win.geometry("500x500")
    win.title("Speech-To-Test Translation")
    win.option_add("*Font", "맑은고딕 25")

    # 어떤 버튼을 눌렀는지 받아오는 인자들
    video_num = IntVar() # IntVar()은 위젯과 연결된 정수형 변수를 생성하는 것
    l1 = IntVar()
    l2 = IntVar()
    l1.set(0)
    l2.set(1)
    


def select_language():
    Label(win, text="\n\n언어를 선택하십시오\n", justify = LEFT, padx = 20, font = 60).pack()
    Label(win, text="영상 언어(번역할 언어)", justify = LEFT, padx = 20, font = 60).pack()
    for count in range(len(h.language)):
        Radiobutton(win, text=h.language[count], padx=20,
        variable=l1, value=count, font = 50, command = l1_button).pack()
    Label(win, text="\n자막 언어(번역되는 언어)", justify = LEFT, padx = 20, font = 60).pack()
    for count in range(len(h.language)):
        Radiobutton(win, text=h.language[count], padx=20,
        variable=l2, value=count, font = 50, command = l2_button).pack()
    
    # "OK" 버튼 생성
    button = Button(win)
    button.config(text = "OK", width = 10, command = OK_button)
    button.pack()

def l1_button(): # 첫 번째 버튼은 한국어, 두 번째 버튼은 영어
    if(l1.get() == 0):
        h.video_language="ko-KR"
        h.translate_language="en-US"
        l2.set(1)
        
    elif(l1.get() == 1):
        h.video_language="en-US"
        h.translate_language="ko-KR"
        l2.set(0)

def l2_button():
    if(l2.get() == 0):
        h.video_language="en-US"
        h.translate_language="ko-KR"
        l1.set(1)

    elif(l2.get() == 1):
        h.video_language="ko-KR"
        h.translate_language="en-US"
        l1.set(0)

def select_video():
    Label(win, text="어떤 영상을 선택하시겠습니까?\n", justify = LEFT, padx = 20, font = 60).pack()
    for count in range(len(h.video)):
        Radiobutton(win, text=h.video[count], padx=20,
        variable=video_num, value=count, font = 50, command = select_video_button).pack()


def select_video_button():
    global press
    if(press == 0):
        select_language() # 이렇게 안하면 라디오 버튼을 누를 때마다 언어 선택 버튼이 생겨서 한번만 생기도록 제한을 둠
    press += 1
    h.select_video_name=h.video[video_num.get()] # 선택한 영상을 넘겨줌
    


def OK_button():
    win.quit() 
    win.destroy()

def main():
    h.init()
    init()
    select_video()
    win.mainloop()




