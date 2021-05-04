from header import *
import header as h

def Video_Audio(file_name,run_event):
    #time.sleep(0.5)
    chunk=1024
    Audio=output_filepath+file_name+".wav"
    f=wave.open(Audio,"rb")
    p=pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)
    data=f.readframes(chunk)
    while len(data)>0:
        if run_event.is_set():
            stream.write(data)
            data=f.readframes(chunk)
        else:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

def subtitles(file_name):
    global skip
    if(h.video_language=="ko-KR"):
        time_stamp= open(output_filepath + file_name + "timestamp.txt","r",encoding="utf-8")
        video_text= open(output_filepath + file_name + "script.txt","r",encoding="utf-8")
        trans_text= open(output_filepath + file_name + "script_result.txt","r")
        skip=2
    else:
        time_stamp= open(output_filepath + file_name + "timestamp.txt","r")
        video_text= open(output_filepath + file_name + "script.txt","r")
        trans_text= open(output_filepath + file_name + "script_result.txt","r")
        skip=1

    time_line=time_stamp.readlines()
    video_line=video_text.readlines()
    trans_line=trans_text.readlines()

    #첫째 script읽어온다.
    #둘째 word단위로 읽는다.
    #셋째 script.endswitch(word)==True
    #넷쨰 time_list에 넣어준다.
    time_list=[]
    video_list=[]
    trans_list=[]
    #time_list.append(i[i.find(':')+1:i.find(')')])
    count=0
    time_count=0
    

    for video in video_line:
        video_list.append(video) 
        time_line=time_line[time_count:]
        time_count=0
        for time in time_line:
            word=time[time.find(':')+1: time.find(',')] # word: ~~~, 
            end=time[time.find(','):]
            end_time=end[end.find(':')+1:end.find(')')]# end: ~~~~~ )

            str_test= video_list[count]
            str_test=str_test[:-1*skip]
            
            if str_test.endswith(word): 
                time_list.append(end_time) 
                break
            else:
                time_count+=1
        count+=1
        
    for trans in trans_line:
        trans_list.append(trans)


    time_stamp.close()
    video_text.close()
    trans_text.close()
    return time_list,video_list,trans_list

def VideoFileOut(file_name):
    File=input_filepath+file_name+audio_name

    cap = cv2.VideoCapture(File)
    cap.set(3,240)
    cap.set(cv2.CAP_PROP_FPS, int(30))
    
    run_event=threading.Event()
    run_event.set()
    t1=threading.Thread(target=Video_Audio,args=(file_name,run_event))
    t1.start()

    basicfont = cv2.FONT_HERSHEY_SIMPLEX
    time_list,video_list,trans_list=subtitles(file_name)
    begin=time.time()
    count=0

    Font=ImageFont.truetype(font_filepath+"gulim.ttf",14)

    if not cap.isOpened():
        print("Error opening video")

    while cap.isOpened():
        ret, frame = cap.read()
        end=time.time()
        if ret:    
            pill_image=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            draw=ImageDraw.Draw(pill_image)
            frame=imutils.resize(frame,width=1600,height=800) 
            draw.text((0, 0),"Esc to exit",font=Font, fill=(255, 255, 255))
            #cv2.putText(frame, "Esc to exit", (50, 50), basicfont, 1, (0, 255, 255), 2, cv2.LINE_4)      
            result=end-begin
            limit=100
            if count<len(time_list):
                if result<float(time_list[count]):
                    video_str=video_list[count]
                    if(len(video_str)>limit):
                        check_blank=video_str[limit:]
                        check=check_blank.find(' ')
                        trans_limit=limit+check
                        draw.rectangle(((0,640),(1600,660)),(0,0,0),None,-1)
                        draw.text((0, 640),video_str[:trans_limit],font=Font, fill=(255, 255, 255))
                        draw.rectangle(((0,660),(1600,680)),(0,0,0),None,-1)
                        draw.text((0, 660),video_str[trans_limit:],font=Font, fill=(255, 255, 255))
                    else:
                        draw.rectangle(((0,660),(1600,680)),(0,0,0),None,-1)
                        draw.text((0, 660),video_str,font=Font, fill=(255, 255, 255))

                    trans_str=trans_list[count]
                    if(len(trans_str)>100):
                        check_blank=trans_str[limit:]
                        check=check_blank.find(' ')
                        trans_limit=limit+check
                        draw.rectangle(((0,680),(1600,700)),(0,0,0),None,-1)
                        draw.text((0, 680),trans_str[:trans_limit],font=Font, fill=(255, 255, 255))
                        draw.rectangle(((0,700),(1600,720)),(0,0,0),None,-1)
                        draw.text((0, 700),trans_str[trans_limit:],font=Font, fill=(255, 255, 255))
                    else:
                        draw.rectangle(((0,680),(1600,700)),(0,0,0),None,-1)
                        draw.text((0, 680),trans_str,font=Font, fill=(255, 255, 255))
                    #cv2.putText(frame, trans_list[count], (0, 880), basicfont, 0.5, (0, 255, 255), 1, cv2.LINE_4)

                else:
                    count += 1      
            frame=cv2.cvtColor(np.array(pill_image),cv2.COLOR_BGR2RGB)

            cv2.imshow("MP4 PLAYER",frame)

        key=cv2.waitKey(9)
        if key ==27 or key==1: #ESC
            #t1 terminate
            run_event.clear()
            t1.join()
            break

        #elif key == 32: #space
            #t1 상태를 확인해서 interrupt가 아니라면 interrupt 맞다면 해제
            #cv2.waitKey()     
        
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # grayscale로 출력하고싶을 경우
        # cv2.imshow('frame', gray)
    cap.release()
    cv2.destroyAllWindows()