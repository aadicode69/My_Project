import os
import time
from click import prompt
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import cv2
import sys
import pywhatkit
import requests
import pyautogui
import folium
import geocoder

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
    
def weatherReports():
    base_url='https://api.openweathermap.org/data/2.5/weather?'
    api_key='9a1d025ef9d919b3d9b02535ae16c36d'
    CITY='Mathura'

    def kelvin_to_cel(kelvin):
        celcius = int(kelvin - 273.15)
        return celcius    

    url=base_url+'appid='+api_key+'&q='+CITY
    response=requests.get(url).json()
    temp_kelvin=response['main']['temp']

    temp_celcius=kelvin_to_cel(temp_kelvin)

    print(f"{temp_celcius}°C")
    speak(f'The weather reports of {CITY} city is {temp_celcius} degree celcius')

def news():
    main_url='https://newsapi.org/v2/everything?domains=wsj.com&apiKey=b42b651cdf694b7d8b7b193daa5a9da4'
    main_page=requests.get(main_url).json()
    articles = main_page['articles']
    head=[]
    day=['first', 'second', 'third','fourth','fifth','sixth']
    for ar in articles:
        head.append(ar['title'])
    for  i in range(len(day)):
        print(f"Today's {day[i]} news is : {head[i]}")
        speak(f"Today's {day[i]} news is : {head[i]}" )

def open_camera():
    # Open the default camera (usually the first one)
    cap = cv2.VideoCapture(0)
    
    # Check if the camera was opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Display the frame
        cv2.imshow('Camera', frame)
        
        # Check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if  hour>=0 and hour < 12:
        speak("Good Morning!")
        print("Good Morning!")
    elif hour>=12 and hour < 18:
        speak("Good Afternoon!")
        print("Good Afternoon!")
    else:
        speak("Good Evening!")
        print("Good Evening!")
    
    speak("I am Matrix. How may i help you Sir?")

def takeCommand():
        #it takes microphone  input from the user and returns string output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        #pause threshold if the seconds of non speaking audio before  a  phrase is  considered complete(if speaker stops for a second then it ensure that ai should stop listening)
        audio = r.listen(source) #will listen to the speaker
    try:
        print("Recognizing......")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User Said: {query}\n")
    except Exception as e:
        #print(e)
        print("Say that again  please....")
        return 'None'
    return query

if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()
        #logic for executing tasks
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia...")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("Sir, what should i search on google?")
            search = takeCommand().lower()
            webbrowser.open(f'{search}')
        elif 'open gla' in query:
            webbrowser.open("https://glauniversity.in:8085/")
        elif 'open my linkedin profile' in query:
            webbrowser.open("https://www.linkedin.com/in/aaditya-goyal-8a51ab285/")
        elif 'open camera' in query:
            open_camera()
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is: {strTime}")
        elif "quit" in query:
            speak("thanks for using me sir, have a good day")
            sys.exit()
        elif 'introduction' in query:
            speak("Hello Sir! I am  Matrix, an AI based voice  assistant.")
            print(" 18th March, 2024 - 21:39")
            speak("I am developed on 18th March, 2024 at 21 hours, 39 minute.")
            speak("According to me, A I have become a revolutionary force in the age of rapid technological growth, changing many aspects of our daily life. The widespread use of voice assistants powered by A I is among the most obvious examples of its effects. These clever virtual assistants have changed the way we engage with technology by blending in perfectly with our smartphones, cars, offices, and homes. A I-based voice assistants have become essential tools, simplifying and improving our increasingly digital world. They can perform simple tasks like playing music and setting reminders, as well as more complicated ones like organizing schedules and controlling smart home devices")
        elif 'open command prompt' in query:
            os.system("start cmd")
        elif 'ip address' in query:
            ip = requests.get('https://api.ipify.org').text
            print(f"Your IP address is {ip}")
            speak(f"Your IP address is {ip}")
        elif 'play song' in query:
            pywhatkit.playonyt('Wishes')
        elif "shut down" in query:
            os.system("shutdown / s / t 5")
        elif "restart" in query:
            os.system("shutdown /r /t 5")
        elif 'switch window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
        elif 'news' in query:
            speak("Please Wait! I am fetching the latest news for you.")
            news()
        elif 'instagram' in query:
            speak("Enter the  username correctly")
            username = input("Enter the username: ")
            webbrowser.open(f'www.instagram.com/{username}')
            speak(f"Opening the  user's profile")
            time.sleep(5)
            speak("I have opened the user's  profile on instagram for you.")
        elif "screenshot" in query:
            speak("Please tell me the name for this screenshot file")
            name = takeCommand() . lower()
            speak("Please hold the screen for few seconds, i am taking sreenshot")
            time. sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png" )
            speak("I am done, the screenshot is saved in our main folder.")
        elif 'weather' in query:
            weatherReports()
            speak("Here are toda's weather reports")
        elif 'location' in query:
            g=geocoder.ip("45.127.226.113")
            myAddress=g.latlng
            speak("Fetching your location")
            print(myAddress)
            my_map1=folium.Map(location=myAddress,zoom_start=12)
            folium.CircleMarker(location=myAddress, radius=50, color='red', fill=True).add_to(my_map1)
            folium.Marker(myAddress).add_to(my_map1)
            my_map1.save("location.html")
            webbrowser.open("location.html")
