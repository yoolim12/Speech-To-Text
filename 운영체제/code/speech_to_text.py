from header import *
import header as h
import upload_wav

#채널 return해 주는 코드
def mp4_to_mp3(fr,des):
    videoclip=mp.VideoFileClip(fr)
    audioclip=videoclip.audio
    audioclip.write_audiofile(des) #mp3 생성
    videoclip.reader.close()
    audioclip.reader.close_proc()


def frame_rate_channel(audio_file_name,file_name):
    #with wave.open(audio_file_name, "rb") as wave_file:
        #frame_rate = wave_file.getframerate()
       # channels = wave_file.getnchannels()
        #return frame_rate,channels
    wav_f=output_filepath+file_name+".wav"
    mp3_f=output_filepath+file_name+".mp3"
    if not os.path.isfile(wav_f):
        try:
            mp4_to_mp3(audio_file_name,mp3_f)
        except:
            print("mp3로 변환하는 과정에서 오류가 발생했습니다!")

        try:
            sound=AudioSegment.from_mp3(mp3_f)
            sound=sound.set_channels(1)
            sound.export(wav_f,format="wav")
        except Exception as e:
            print("wav로 변환하는 과정에서 오류가 발생했습니다!",e)
    else:
        print("wav file already exist")

    try:
        with wave.open(wav_f, "rb") as wave_file:
            frame_rate = wave_file.getframerate()
            channels = wave_file.getnchannels() 
        return frame_rate,channels
    except:
        print("wav에서 채널을 구하는데 오류가 발생했습니다!")
        return 0,0
   

    

#wav to text

def google_transcribe(audio_file_name):
    file_name = input_filepath + audio_file_name + audio_name
    # The name of the audio file to transcribe
    frame_rate, channels = frame_rate_channel(file_name,audio_file_name)
    transcript = ''
    if frame_rate ==0 and channels ==0:
        return transcript

    file_list=os.listdir(output_filepath)
    # 폴더에서 wav파일 가져옴.
    for file_li in file_list:
        if file_li[-3:] == "wav" and file_li[:-4]==audio_file_name:
            upload_wav.upload_blob(bucketname,output_filepath+file_li,file_li[:-4])

    gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code=h.video_language,
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )
    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=1000)
        
    f= open(output_filepath + audio_file_name + "timestamp.txt","w",encoding="utf-8")
    for result in response.results:
        alternative = result.alternatives[0]
        transcript += alternative.transcript
        #print("Transcript: {}".format(alternative.transcript))
        #print("Confidence: {}".format(alternative.confidence))
        
        for word_info in alternative.words:
            word = word_info.word
            #word= word.translate(str.maketrans('', '', string.punctuation)) # , . ! ? 제거
            #start_time = word_info.start_time
            end_time = word_info.end_time
            #if(word.endswith("다") or word.endswith("요") or word.endswith("까")):
            timeline=f"(word:{word}, endtime:{end_time.total_seconds()})"
            f.write(timeline+'\n')
    f.close()
    return transcript

def write_transcripts(transcript_filename,transcript):
    f= open(output_filepath + transcript_filename + ".txt","w",encoding="utf-8")
    trans_list=transcript.split()
    for text in trans_list:
        #if(text.endswith("다") or text.endswith("요")or text.endswith("까")):
            #f.write(text+ ". ")
        #else:
        if text.endswith('.') or text.endswith('?') or text.endswith('!'):
            f.write(text+ '\n')
        else:
            f.write(text+ " ")
    f.close()
    print(transcript_filename+" Worked out!")


#write_transcripts("script", google_transcribe("test"))


