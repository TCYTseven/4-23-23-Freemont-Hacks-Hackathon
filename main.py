from flask import Flask, render_template, request
import requests
import os
import random
import pickle
import openai
import re
from time import time, sleep

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/chatbot')
def chatbot():
  return render_template('chatbot.html')    

@app.route('/zenden')
def zenden():
    video_urls = [
        'https://www.youtube.com/embed/S-W1GFBJbt0',
        'https://www.youtube.com/embed/uTN29kj7e-w',
        'https://www.youtube.com/embed/P-8ALcF8AGE',
        'https://www.youtube.com/embed/pxWOpGm4d7U',
        'https://www.youtube.com/embed/rKBEGpzK25s',
        'https://www.youtube.com/embed/vj0JDwQLof4'
    ]
    random_video = random.choice(video_urls)
    return render_template('zenden.html', video=random_video)  

@app.route('/selfcare')
def selfcare():
  return render_template('selfcare.html')       
     
def open_file(filepath):
  with open(filepath, 'r', encoding='utf-8') as infile:
    return infile.read()

#blurred for privacy reasons
openai.api_key = "blur"



def is_valid_input(input_text):
    
    cleaned_input = re.sub(r'\W+', '', input_text)

    
    if len(cleaned_input) < 5:
        return False
    else:
        return True

def bot(prompt,
        engine='text-davinci-002',
        temp=0.9,
        top_p=1.0,
        tokens=1000,
        freq_pen=0.0,
        pres_pen=0.5,
        stop=['<<END>>']):
  max_retry = 1
  retry = 0
  while True:
    try:
      response = openai.Completion.create(engine=engine,
                                          prompt=prompt,
                                          temperature=temp,
                                          max_tokens=tokens,
                                          top_p=top_p,
                                          frequency_penalty=freq_pen,
                                          presence_penalty=pres_pen,
                                          stop=[" User:", " AI:"])
      text = response['choices'][0]['text'].strip()
      print(text)
      filename = '%s_gpt3.txt' % time()
      with open('gpt3_logs/%s' % filename, 'w') as outfile:
        outfile.write('PROMPT:\n\n' + prompt +
                      '\n\n==========\n\nRESPONSE:\n\n' + text)
      return text
    except Exception as oops:
      retry += 1
      if retry >= max_retry:
        return "GPT3 error: %s" % oops
      print('Error communicating with OpenAI:', oops)
      sleep(1)


@app.route("/get")
def get_bot_response():
  userText = request.args.get('msg')
  if is_valid_input(userText):
    botresponse = bot(prompt=userText)
  else:
    botresponse = "Sorry, I didn't catch that - try again."
  return str(botresponse)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)