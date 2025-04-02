from openai import AzureOpenAI
from typing import Literal, List, Optional

ENDPOINT = "https://mango-bush-0a9e12903.5.azurestaticapps.net/api/v1"
API_KEY = "bc46a4ef-4849-47c5-b810-d6e35da52f98"
API_VERSION = "2024-02-01"
MODEL_NAME = "gpt-4o-mini"

MOOD_CATEGORIES = ["Stressed", "Sad", "Angry"]

def get_mood_response(user_input):
    system_prompt = """You are a helpful study assistant for people with ADHD. Your task is to interpret the user's response to "How are you feeling?" and categorise their mood, focusing specifically on identifying if they are stressed, sad, or angry.

        The user's input is their direct response to being asked about their current emotional state. 
        They may express their feelings in various ways, such as:
        - Direct statements ("I'm feeling stressed", "I'm sad", "I'm angry")
        - Descriptions of their state ("I can't handle this", "I feel overwhelmed", "I'm frustrated")
        - Metaphors or comparisons ("I feel like I'm drowning", "Everything is falling apart", "I'm about to explode")
        - Physical sensations ("My heart is racing", "I feel exhausted", "My head is pounding")
        
        You must categorise their mood into one of these categories:
        - Stressed: When they express anxiety, pressure, feeling overwhelmed, or difficulty coping
        - Sad: When they express sadness, disappointment, low mood, or feelings of hopelessness
        - Angry: When they express frustration, irritation, anger, or feeling upset
        
        For each mood, provide specific, actionable suggestions:
        - For Stressed: 
          * Take a 5-minute break to do the 4-7-8 breathing technique (inhale for 4, hold for 7, exhale for 8)
          * Write down your top 3 most urgent tasks and tackle them one at a time
          * Set a 25-minute timer for focused work, followed by a 5-minute break
          * Take a 10-minute walk outside to clear your mind
          * Use the Pomodoro technique: 25 minutes work, 5 minutes break
        
        - For Sad:
          * Listen to your favourite upbeat song for 3 minutes
          * Write down 3 things you're grateful for right now
          * Call or text a friend or family member
          * Do a quick 5-minute stretching routine
          * Watch a funny video or read a joke
        
        - For Angry:
          * Do 10 deep breaths with your eyes closed
          * Take a 5-minute break to walk around the room
          * Write down your feelings in a journal
          * Do 20 jumping jacks to release tension
          * Use the 5-4-3-2-1 grounding technique (name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste)
        
        Remember to:
        1. Consider the full context of their response
        2. Look for both explicit and implicit mood indicators
        3. Consider the intensity of their emotions
        4. Account for any mixed feelings
        5. Provide specific, actionable recommendations that can be done immediately
        6. Always maintain a supportive and non-judgmental tone
    """
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "analyze_mood",
                "description": "Analyze the user's mood and provide specific, actionable recommendations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mood_category": {
                            "type": "string",
                            "enum": MOOD_CATEGORIES,
                            "description": "The detected mood category"
                        },
                        "confidence_score": {
                            "type": "number",
                            "description": "Confidence score between 0 and 1",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "mood_intensity": {
                            "type": "number",
                            "description": "Intensity of the mood from 1-5",
                            "minimum": 1,
                            "maximum": 5
                        },
                        "detected_emotions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of specific emotions detected in the user's response"
                        },
                        "stressors": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of potential stressors or triggers identified in the response"
                        },
                        "immediate_actions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of specific, actionable steps the user can take right now"
                        },
                        "supportive_message": {
                            "type": "string",
                            "description": "A supportive message tailored to the user's mood and also inviting them to chat if they want"
                        }
                    },
                    "required": ["mood_category", "confidence_score", "mood_intensity", "detected_emotions", "stressors", "immediate_actions", "supportive_message"]
                }
            }
        }
    ]
    
    response = get_response(user_input, system_prompt, tools)
    return response

def get_chat_response(user_input, mood_description):
    system_prompt = f"""You are a helpful study assistant for someone who is: {mood_description}.
        The user has previously expressed this mood state, and you should tailor your response accordingly.
        
        Guidelines for responding:
        1. Acknowledge their current emotional state without judgment
        2. Focus on emotional support first, then study guidance
        3. Offer specific, actionable coping strategies that can be done immediately
        4. Keep suggestions gentle and manageable
        5. Be patient and understanding
        6. If they seem in crisis, encourage seeking professional help
        
        Remember that their mood may have changed since their last response, so be attentive to any new emotional indicators in their current message.
        
        Can you return the response in markdown format also
        """
    
    response = get_response(user_input, system_prompt)
    return response

def get_response(user_input, system_prompt, tools=None):
    client = AzureOpenAI(
        azure_endpoint=ENDPOINT,
        api_key=API_KEY,
        api_version=API_VERSION,
    )

    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"{user_input}"}
    ]

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    if tools and completion.choices[0].message.tool_calls:
        return completion.choices[0].message.tool_calls[0].function.arguments
    return completion.choices[0].message.content