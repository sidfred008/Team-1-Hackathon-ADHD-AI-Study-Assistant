from textblob import TextBlob
import time
import random

def get_user_mood():
    mood = input("How do you feel? (Focused / Distracted / Overwhelmed): ").lower()
    return mood

def suggest_study_plan(mood):
    if mood == "focused":
        print("Great! Try a 30-minute deep focus session. Stay strong! 💪")
        time.sleep(2)  # Simulating session
    elif mood == "distracted":
        print("Let's do a short 15-minute session first. You got this! 🔥")
        time.sleep(2)
    elif mood == "overwhelmed":
        print("Take a deep breath. Try a 5-minute relaxation first. 🌿")
        time.sleep(2)
    else:
        print("I didn't get that, but let's try a 20-minute study session. 📚")
        time.sleep(2)

def ask_for_feedback():
    feedback = input("Was that session helpful? (Yes / No): ").lower()
    if feedback == "no":
        print("No worries! We'll adjust for next time. Try a different method! 🚀")
    else:
        print("Awesome! Keep going! 💡")

# Run the AI Study Assistant
print("Welcome to the AI-Powered Study Assistant for Neurodiverse Learners! 🎓")
while True:
    mood = get_user_mood()
    suggest_study_plan(mood)
    ask_for_feedback()
    more = input("Do you want another session? (Yes / No): ").lower()
    if more != "yes":
        print("Great work! See you next time! 😊")
        break

