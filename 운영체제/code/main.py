import translate_test
import speech_to_text
import video_out
import gui
import header as h
SelectGui=gui.main()
Video_name=h.select_video_name
Video_path=h.output_filepath+h.select_video_name+"script.txt"
Os=h.os
if(not Video_name==""):
    if (not Os.path.isfile(Video_path)):
        speech_to_text.write_transcripts(Video_name+"script", speech_to_text.google_transcribe(Video_name))
        translate_test.Translate(Video_name+"script.txt", Video_name+"script_result.txt")
    else:
        print("Translate file already exist!")
    video_out.VideoFileOut(Video_name)
else:
    print("Not selected video!")