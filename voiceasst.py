from flask import Flask, render_template, request, jsonify
import pyttsx3
import datetime
import webbrowser
import os
import pyautogui
import cv2
import operator
import time
import requests
import wikipedia
import speech_recognition as sr
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from counsler import takeCommand

# Initialize Flask app
app = Flask(__name__)

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

def speak(audio):
    try:
        # Set properties (optional)
        engine.setProperty('rate', 150)    # Speed percent (can go over 100)
        engine.setProperty('volume', 0.9)  # Volume 0-1

        # Speak the text
        engine.say(audio)
        engine.runAndWait()

    except RuntimeError as e:
        print(f"Error occurred in speak(): {e}")
        # Handle the error gracefully, for example, logging the error
        # and returning a default response
        return "Error occurred while processing your request."

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"

def handle_command(command):
    command = command.lower()

    if 'assistant' in command:
        speak("Yes, Sir")
        response_text = "Yes, Ma'am"
        speak(response_text)
        return response_text

    elif 'how are you' in command:
        speak("I am awesome")
        response_text = "I am awesome"
        speak(response_text)
        return response_text

    elif 'who created you' in command:
        speak("The great TiMi")
        response_text = "The great Timi"
        speak(response_text)
        return response_text

    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        response_text = "Opening YouTube"
        speak(response_text)
        return response_text

    elif 'make summary' in command:
        try:
            speak("Running the summary application.")
            os.system(f"streamlit run \"C:\\Users\\MITALI PAWAR\\Downloads\\advance_voice_assistant\\advance_voice_assistant\\summary.py\"")
            response_text = "Running the summary application."
            return response_text
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)
            speak(error_message)
            return error_message


    elif 'close youtube' in command:
        os.system("taskkill /f /im chrome.exe")
        response_text = "Closing YouTube"
        speak(response_text)
        return response_text

    elif 'open google' in command:
        try:
            speak("What should I search?")
            qry = takeCommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={qry}")
            try:
                results = wikipedia.summary(qry, sentences=2)
                speak(results)
                return results
            except Exception as e:
                speak("Sorry, I couldn't find any information on that topic.")
                return "Sorry, I couldn't find any information on that topic."
        except Exception as e:
            print(f"Error opening Google: {str(e)}")
            return "Error opening Google"

    elif 'close google' in command:
        os.system("taskkill /im chrome.exe /f")
        response_text = "Closing Google"
        speak(response_text)
        return response_text

    elif 'open chrome' in command:
        webbrowser.open("https://www.google.com")
        response_text = "Opening Chrome"
        speak(response_text)
        return response_text

    elif 'close chrome' in command:
        os.system("taskkill /im chrome.exe /f")
        response_text = "Closing Chrome"
        speak(response_text)
        return response_text

    elif 'open facebook' in command:
        webbrowser.open("https://www.facebook.com")
        response_text = "Opening Facebook"
        speak(response_text)
        return response_text

    elif 'close facebook' in command:
        os.system("taskkill /im chrome.exe /f")
        response_text = "Closing Facebook"
        speak(response_text)
        return response_text

    elif 'open notepad' in command:
        os.startfile("notepad.exe")
        speak("Opening Notepad")
        time.sleep(2)
        speak("What should I write?")
        text = takeCommand()
        pyautogui.write(text)
        response_text = "Opening Notepad"
        speak(response_text)
        return response_text

    elif "volume up" in command:
        for _ in range(15):
            pyautogui.press("volumeup")
        response_text = "Volume Up"
        speak(response_text)
        return response_text

    elif "volume down" in command:
        for _ in range(15):
            pyautogui.press("volumedown")
        response_text = "Volume Down"
        speak(response_text)
        return response_text

    elif "mute" in command:
        pyautogui.press("volumemute")
        response_text = "Volume Muted"
        speak(response_text)
        return response_text

    elif "open camera" in command:
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('webcam', img)
            if cv2.waitKey(50) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        response_text = "Camera Opened"
        speak(response_text)
        return response_text

    elif "close camera" in command:          
        cv2.destroyAllWindows()
        response_text = "Camera Closed"
        speak(response_text)
        return response_text

    elif 'search on youtube' in command:
        command = command.replace("search on youtube", "")
        webbrowser.open(f"www.youtube.com/results?search_command={command}")
        response_text = f"Searching on YouTube: {command}"
        speak(response_text)
        return response_text

    elif 'the time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response_text = f"Ma'am, the time is {strTime}"
        speak(response_text)
        return response_text

    elif "close notepad" in command:
        os.system("taskkill /f /im notepad.exe")
        response_text = "Notepad Closed"
        speak(response_text)
        return response_text

    elif "open command prompt" in command:
        os.system("start cmd")
        response_text = "Command Prompt Opened"
        speak(response_text)
        return response_text

    elif "close command prompt" in command:
        os.system("taskkill /f /im cmd.exe")
        response_text = "Command Prompt Closed"
        speak(response_text)
        return response_text

    elif "take screenshot" in command:
        speak('Tell me a name for the file')
        name = takeCommand().lower()
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        response_text = f"Screenshot saved as {name}.png"
        speak(response_text)
        return response_text

    elif "calculate" in command:
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Ready")
                print("Listening...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string = r.recognize_google(audio)
            print(my_string)
            def get_operator_fn(op):
                return {
                    '+': operator.add,
                    '-': operator.sub,
                    'x': operator.mul,
                    'divided': operator.__truediv__,
                }[op]
            def eval_binary_expr(op1, oper, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            result = eval_binary_expr(*(my_string.split()))
            speak("Your result is")
            speak(result)
            return result
        except Exception as e:
            print(f"Error calculating: {str(e)}")
            return "Error calculating"

    elif "what is my ip address" in command:
        speak("Checking")
        try:
            ipAdd = requests.get('https://api.ipify.org').text
            response_text = f"Your IP address is {ipAdd}"
            speak(response_text)
            return response_text
        except Exception as e:
            response_text = "Network is weak, please try again some time later"
            speak(response_text)
            return response_text

    elif "rectangular spiral" in command:
        try:
            pyautogui.hotkey('win')
            time.sleep(1)
            pyautogui.write('paint')
            time.sleep(1)
            pyautogui.press('enter')
            pyautogui.moveTo(100, 193, 1)
            pyautogui.rightClick()
            pyautogui.click()
            distance = 300
            while distance > 0:
                pyautogui.dragRel(distance, 0, 0.1, button="left")
                distance -= 10
                pyautogui.dragRel(0, distance, 0.1, button="left")
                pyautogui.dragRel(-distance, 0, 0.1, button="left")
                distance -= 10
                pyautogui.dragRel(0, -distance, 0.1, button="left")
            response_text = "Rectangular spiral drawn"
            speak(response_text)
            return response_text
        except Exception as e:
            print(f"Error drawing rectangular spiral: {str(e)}")
            response_text = "Error drawing rectangular spiral"
            speak(response_text)
            return response_text

    elif "close paint" in command:
        os.system("taskkill /f /im mspaint.exe")
        response_text = "Paint Closed"
        speak(response_text)
        return
        response_text

    elif 'type' in command:
        text = command.replace("type", "")
        pyautogui.write(text)
        response_text = f"Typed: {text}"
        speak(response_text)
        return response_text

    elif 'open new window' in command:
        pyautogui.hotkey('ctrl', 'n')
        response_text = "New window opened"
        speak(response_text)
        return response_text

    elif 'open incognito window' in command:
        pyautogui.hotkey('ctrl', 'shift', 'n')
        response_text = "Incognito window opened"
        speak(response_text)
        return response_text

    elif 'minimize this window' in command:
        pyautogui.hotkey('alt', 'space')
        time.sleep(1)
        pyautogui.press('n')
        response_text = "Window minimized"
        speak(response_text)
        return response_text

    elif 'open history' in command:
        pyautogui.hotkey('ctrl', 'h')
        response_text = "History opened"
        speak(response_text)
        return response_text

    elif 'open downloads' in command:
        pyautogui.hotkey('ctrl', 'j')
        response_text = "Downloads opened"
        speak(response_text)
        return response_text

    elif 'select all' in command:
        pyautogui.hotkey('ctrl', 'a')
        response_text = "All text selected"
        speak(response_text)
        return response_text

    elif 'copy' in command:
        pyautogui.hotkey('ctrl', 'c')
        response_text = "Text copied"
        speak(response_text)
        return response_text

    elif 'paste' in command:
        pyautogui.hotkey('ctrl', 'v')
        response_text = "Text pasted"
        speak(response_text)
        return response_text

    elif 'go back' in command:
        pyautogui.hotkey('alt', 'left')
        response_text = "Went back"
        speak(response_text)
        return response_text

    elif 'go forward' in command:
        pyautogui.hotkey('alt', 'right')
        response_text = "Went forward"
        speak(response_text)
        return response_text

    elif 'refresh' in command:
        pyautogui.hotkey('ctrl', 'r')
        response_text = "Page refreshed"
        speak(response_text)
        return response_text

    elif 'close this tab' in command:
        pyautogui.hotkey('ctrl', 'w')
        response_text = "Tab closed"
        speak(response_text)
        return response_text

    elif 'maximize window' in command:
        pyautogui.hotkey('alt', 'space')
        time.sleep(1)
        pyautogui.press('x')
        response_text = "Window maximized"
        speak(response_text)
        return response_text

    elif 'scroll up' in command:
        pyautogui.scroll(300)
        response_text = "Scrolled up"
        speak(response_text)
        return response_text

    elif 'scroll down' in command:
        pyautogui.scroll(-300)
        response_text = "Scrolled down"
        speak(response_text)
        return response_text

    elif 'sentiment' in command:
        speak("Please say something for me to analyze.")
        text = takeCommand()
        sentiment = analyze_sentiment(text)
        if sentiment == "positive":
            speak("It sounds like you're feeling positive. That's great!")
        elif sentiment == "neutral":
            speak("I see. Your sentiment seems neutral.")
        elif sentiment == "negative":
            speak("I'm sorry to hear that you're feeling negative. Is there anything I can do to help?")
        return

    else:
        speak("I am not sure how to do that.")
        response_text = "Command not recognized"
        speak(response_text)
        return response_text

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.get_json()
    command = data.get('command', '')

    response_text = handle_command(command)

    return jsonify(response=response_text)

# Run the app
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
