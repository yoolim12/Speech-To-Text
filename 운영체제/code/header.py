# Import libraries
from pydub import AudioSegment
import pydub
import io
import wave
import os
from os import path
import sys
import urllib.request
import json # str type의 결과 코드를 dict type으로 변환하기 위함
from google.cloud import storage
from google.cloud import speech
import moviepy.editor as mp
import subprocess
import ffmpeg 
import pyaudio 
import threading
import time
import cv2
from PIL import ImageFont,ImageDraw,Image
import numpy as np
import imutils
import string

#filepath = "E://운영체제/input/"     
#Input audio file path
#output_filepath = "E://운영체제/output/" 
#Final transcript path
bucketname = "speechtotextmybucket_2" #Name of the bucket created in the step before
audio_name=".mp4"

folder=os.getcwd() # os.getcwd : 현재 디렉토리 위치 반환. "운영체제" 폴더 까지의 경로를 반환한다.
input_filepath=os.path.join(folder,"input/") # "운영체제" 폴더 내의 "input" 폴더
output_filepath=os.path.join(folder,"output/") # "운영체제" 폴더 내의 "output" 폴더
font_filepath=os.path.join(folder,"font/") # "운영체제" 폴더 내의 "font" 폴더

# api 인증키를 따로 환경변수 설정 필요 없이 자동으로 잡도록 하였다.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=input_filepath+"reference.json" 
#AudioSegment.converter = os.path.join(folder,"ffmpeg/ffmpeg-3.4.1-win64-static/bin/ffmpeg"

def init():
    global video,language,select_video_name,video_language,translate_language
    video=[] # 영상 파일을 넣게 될 리스트
    language=["한국어", "영어"] # 번역 및 음성 인식에 사용될 언어들
    select_video_name="" # 사용자가 선택한 영상 이름이 들어간다
    
    # 영상 언어는 한국어로, 번역되는 언어는 영어로 초기화
    video_language="ko-KR"
    translate_language="en-US"


