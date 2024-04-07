from flask import Flask, render_template, request
import os
import shutil
import cv2
import extract_frames
import aiohttp
import asyncio
import nest_asyncio
import time
import json
import base64
from PIL import Image
import emotion_analysis
import transcript_analysis
import threading

app = Flask(__name__)

# Apply nest_asyncio
nest_asyncio.apply()

# Define the upload directories
UPLOAD_VIDEO_DIR = 'videos'
UPLOAD_TRANSCRIPT_DIR = 'transcripts'

# Create directories if they don't exist
if not os.path.exists(UPLOAD_VIDEO_DIR):
    os.makedirs(UPLOAD_VIDEO_DIR)

if not os.path.exists(UPLOAD_TRANSCRIPT_DIR):
    os.makedirs(UPLOAD_TRANSCRIPT_DIR)

# Delete video_frames directory if it exists
video_frames_dir = 'video_frames'
if os.path.exists(video_frames_dir):
    shutil.rmtree(video_frames_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

    if 'video' in request.files:
        video_file = request.files['video']
        if video_file.filename != '':
            try:
                video_file.save(os.path.join(UPLOAD_VIDEO_DIR, 'video.mp4'))
                print("Video file saved successfully")
            except Exception as e:
                print("Error saving video file:", e)

    if 'transcript' in request.files:
        transcript_file = request.files['transcript']
        if transcript_file.filename != '':
            try:
                transcript_file.save(os.path.join(UPLOAD_TRANSCRIPT_DIR, 'transcript.txt'))
                print("Transcript file saved successfully")
            except Exception as e:
                print("Error saving transcript file:", e)
    
    qualification = request.form['education']
    skills = request.form['skills']
    experience = request.form['experience']

    extract_frames.extract_frames()
    emotion_score = asyncio.run(emotion_analysis.analyze())
    # print(emotion_score)
    requirements = asyncio.run(transcript_analysis.analyze(qualification, skills, experience))
    print(requirements)
    # transcript_analysis.trial(qualification, skills, experience)

    final_score = 1
    for score in requirements:
        final_score = final_score and score
    
    if emotion_score < 0.5:
        final_score = 0

    return render_template("result.html", transcript_result = requirements, emotion_score = emotion_score, final_score = final_score)

if __name__ == '__main__':
    app.run(debug=True)
