import os
import re
import speech_recognition as sr
import pygame
import random

def voice_input(prompt):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        else:
            return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand you.")
        return None
    except sr.RequestError as e:
        print("Sorry, an error occurred:", e)
        return None
   
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index to select a different voice (0 , 1)

import pywhatkit
import datetime
import wikipedia
import pyjokes
import PyPDF2
import requests
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

r = sr.Recognizer()
engine = pyttsx3.init()
name = "Sigma"

import openai
openai.api_key = "Your_API_key"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def command():
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User said: {query}\n")

        if query.split()[0].lower() == 'sigma':
            query = ' '.join(query.split()[1:])
        else:
            query = ''

    except Exception as e:
        print("Sorry, I did not understand what you said.")
        return ""

    return query

def get_location(place):
    url = f'https://nominatim.openstreetmap.org/search?q={place}&format=json&addressdetails=1'
    response = requests.get(url)
    data = response.json()
    if not data:
        raise ValueError(f'Could not find location for "{place}"')
    location = {
        'lat': data[0]['lat'],
        'lng': data[0]['lon']
    }
    return location

def show_map(location):
    lat = location['lat']
    lng = location['lng']
    url = f'https://www.google.com/maps/search/?api=1&query={lat},{lng}'
    webbrowser.open_new_tab(url)

def play_media(media_type):
    if media_type == "music":
        media_folder = "your_music_Folder_directory"
        media_files = [f for f in os.listdir(media_folder) if f.endswith(".mp3")]

        if len(media_files) == 0:
            speak("No music files found in the folder.")
            return

        # Speak out the available songs
        speak("Which song do you want to play?")
        for i, media_file in enumerate(media_files):
            print(f"{i+1}. {os.path.splitext(media_file)[0]}")

        # Get the user input for song selection
        selection = int(input("Please select a song by number:- "))
        if selection is None:
            speak("Invalid selection.")
            return
        if not isinstance(selection, int) or selection not in range(1, len(media_files)+1):
            speak("Invalid selection.")
            return


        # Play the selected song
        pygame.mixer.init()
        media_path = os.path.join(media_folder, media_files[selection-1])
        speak(f"Playing {os.path.splitext(media_files[selection-1])[0]}")
        pygame.mixer.music.load(media_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass

    elif media_type == "video":
        # specify the path of the directory where your video files are stored
        video_dir = "your_video_Folder_directory"

        # get a list of all the files in the directory
        files = os.listdir(video_dir)

        # filter out the non-video files (e.g. music)
        video_files = [f for f in files if f.endswith((".mp4", ".avi", ".mkv"))]

        if len(video_files) == 0:
            speak("No video files found in directory.")
            return

        # Speak out the available videos
        speak("Which video do you want to play?")
        for i, video_file in enumerate(video_files):
            print(f"{i+1}. {os.path.splitext(video_file)[0]}")

        # Get the user input for video selection
        selection = int(input("Please select a video by number."))
        if selection is None or int(selection) not in range(1, len(video_files)+1):
            speak("Invalid selection.")
            return

        # Play the selected video
        video_path = os.path.join(video_dir, video_files[int(selection)-1])
        speak(f"Playing {os.path.splitext(video_files[int(selection)-1])[0]}")
        os.startfile(video_path)

    else:
        speak("Sorry, I can only play music or video files.")

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)
    speak(f"Here are the search results for {query} on Google.")

def send_email(to, subject, body, cc=None):
    # Replace the placeholders below with your own information
    email_address = 'your_email'
    email_password = 'password'

    # Set up the email message
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = to
    message['Subject'] = subject

    if cc is not None:
        # Add CC recipients if provided
        if isinstance(cc, list):
            message['Cc'] = ", ".join(cc)
        else:
            message['Cc'] = cc

    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    recipients = [to]
    if cc is not None:
        if isinstance(cc, list):
            recipients.extend(cc)
        else:
            recipients.append(cc)
    text = message.as_string()
    server.sendmail(email_address, recipients, text)
    server.quit()
    print(f"Email sent to {to} with subject '{subject}'")
    if cc is not None:
        print(f"Email sent to CC: {cc}")

Greeting = ["Ready to take on the day together?","I'm your virtual assistant, What can I do for you today?",f" I'm {name}! How can I assist you today?",
            "Welcome back! Ready to tackle your to-do list?", "Let's make your day more productive with my help","Good to see you! How can I assist you today?",
            "how can I be of service to you today?", "let's make today a great one with my help!", " Good to see you again! What can I do for you today?",
            "It's always a pleasure to talk to you. What do you need?", "I'm your personal assistant. How can I make your day easier?",
            "What can I do to help you achieve your goals today?","It's great to hear from you. How can I assist you today?",
            "Let's get to work. What can I help you with today?" ]

def run_assistant():

    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
        
    speak(random.choice(Greeting))

    print(""" 
    Please say SIGMA before every command ( for help say Sigma help)

    Play :-         For playing youtube videos.
    Time :-         For time.
    Search :-       To search something on Google.
    Joke :-         To tell a joke.
    Scan :-         To read PDF from your local file.
    Weather :-      To know weather for any city in the world.
    Location of :-  To search from Google map.
    Music :-        To play music from your local directory.
    Video :-        To watch video from your local Directory
    Wikipedia :-    To search something on Wikipedia.
    Send Email :-   To send email to anybody
    GPT :-          To use Chat-GPT (Can provide basic information)
    Stop :-         To close Sigma
    """)
   
    while True:
        command_text = command().lower()

        if 'play' in command_text:
            song = command_text.replace('play', '')
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'time' in command_text:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {time}")

        elif 'wikipedia' in command_text:
            topic = command_text.replace('search', '')
            info = wikipedia.summary(topic, sentences=2)
            speak(info)

        elif 'joke' in command_text:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'scan' in command_text:
            pdf_files = [f for f in os.listdir('your_PDF_folder_location') if f.endswith('.pdf')]

            if pdf_files:
                speak("Here are the PDF files in this folder:")
                for i, pdf_file in enumerate(pdf_files):
                    print(f"{i + 1}. {pdf_file}")
                    print()
                speak("Which PDF you want me to read")
                pdf_choice = int(input("Enter the number of the PDF: "))
                if 0 < pdf_choice <= len(pdf_files):
                    pdf_file = pdf_files[pdf_choice - 1]
                    book = open(pdf_file, 'rb')
                    pdfReader = PyPDF2.PdfReader(book)
                    pages = len(pdfReader.pages)
                    speak(f"The book has {pages} pages")
                    speak("Which page number you want me to read")
                    page = int(input("Enter the page number: "))
                    if 1 <= page <= pages:
                        pageObj = pdfReader.pages[page - 1]
                        text = pageObj.extract_text()
                        speak(text)
                    else:
                        speak("Sorry, that page doesn't exist in the book.")
                else:
                    speak("Sorry, I didn't recognize that PDF number.")
            else:
                speak("Sorry, there are no PDF files in this folder.")

        elif 'weather' in command_text:
            api_key = "your_weather_API_key" # Replace with your API key from OpenWeatherMap
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("Which city do you want to know the weather for?")
            city = voice_input("Please say the name of the city")
            if city:
                complete_url = base_url + "appid=" + api_key + "&q=" + city
                response = requests.get(complete_url)
                data = response.json()
                if data["cod"] != "404":
                    weather = data["weather"][0]["description"]
                    temperature = int(data["main"]["temp"] - 273.15)
                    humidity = data["main"]["humidity"]
                    wind_speed = data["wind"]["speed"]
                    speak(f"The weather in {city} is {weather}")
                    speak(f"The temperature is {temperature} degrees Celsius")
                    speak(f"The humidity is {humidity} percent")
                    speak(f"The wind speed is {wind_speed} meters per second")
                else:
                    speak("City not found. Please try again.")
            else:
                speak("Sorry, I didn't hear the name of the city.")

        elif 'location of' in command_text:
            place = re.search(r'location of (.+)', command_text)
            if place:
                place = place.group(1)
                try:
                    location = get_location(place)
                    show_map(location)
                    speak(f"Here's the location of {place}")
                except ValueError as e:
                    speak(str(e))
            else:
                speak("Sorry, I didn't understand the location you requested.")
        elif 'music' in command_text:
            play_media("music")

        elif 'video' in command_text:
            play_media("video")

        elif "search" in command_text:
            search_query = command_text.replace("search", "").strip()
            search_google(search_query)

        elif 'send email' in command_text:
            speak("Enter the recipient email address: ")
            recipient = input("Enter the recipient email address: ")
            speak("Enter the subject: ")
            subject = input("Enter the subject: ")
            speak("Enter the email body: ")
            body = input("Enter the email body: ")
            speak("Do you want to include a CC email address? ")
            cc = input("Do you want to include a CC email address? (Y/N): ")
    
            if cc.upper() == "Y":
                speak("Enter the CC email address: ")
                cc_address = input("Enter the CC email address: ")
                send_email(recipient, subject, body, cc_address)
            else:
                send_email(recipient, subject, body)
        
            print("Email sent successfully!")

        elif 'gpt' in command_text:
            speak("Initiating ChatGPT")
            prompt = input("Your query: ")
            chat_history = ""
            while True:
                response = openai.Completion.create(
                    engine="curie",
                    prompt=f"{prompt}\n{chat_history}",
                    max_tokens=512,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                message = response.choices[0].text.strip()
                chat_history += f"\nUser: {prompt}\nAI: {message}"
                print(message)
                prompt = input("Your query: ")

        elif 'help' in command_text:
            print(""" 
                    Please say SIGMA before every command ( for help say Sigma help)

                    Play :-         For playing youtube videos.
                    Time :-         For time.
                    Wikipedia :-    To search something on Google.
                    Joke :-         To tell a joke.
                    Scan :-         To read PDF from your local file.
                    Weather :-      To know weather for any city in the world.
                    Location of :-  To search from Google map.
                    Music :-        To play music from your local directory.
                    Video :-        To watch video from your local Directory
                    Wikipedia :-    To search something on Wikipedia.
                    Send Email :-   To send email to anybody
                    GPT :-          To use Chat-GPT (Can provide basic information)
                    Stop :-         To close Sigma
            """)

        elif 'stop' in command_text:
            speak(f"Bye, Until next time!")
            break

if __name__ == '__main__':
    run_assistant()