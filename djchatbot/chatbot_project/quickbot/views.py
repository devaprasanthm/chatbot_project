
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import re

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            # Parse the user's message from the POST request
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Validate input
            if not user_message:
                return JsonResponse({'response': "I didn't receive a message. Could you try again?"})

            # Generate a response based on user input
            response_message = generate_response(user_message)
            return JsonResponse({'response': response_message})

        except json.JSONDecodeError:
            return JsonResponse({'error': "Invalid JSON input."}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)
    
    return JsonResponse({'error': 'Invalid request. Only POST method is allowed.'}, status=400)


def generate_response(user_message):
    """
    Generates a response to the user's message using a combination of 
    predefined responses, regex pattern matching, and optional OpenAI API.
    """
    # Convert the message to lowercase for easier matching
    message = user_message.lower()

    # Predefined patterns and responses
    patterns = {
        r"(hello|hi|hey)": "Hello! How can I assist you today?",
        r"how are you": "I'm just a bot, but I'm functioning perfectly! How about you?",
        r"(bye|goodbye)": "Goodbye! Have a wonderful day!",
        r"(thanks|thank you)": "You're welcome! Let me know if there's anything else I can do for you.",
        r"(your name|who are you)": "I'm QuickBot, your friendly chatbot!",
        r"(help|assist)": "Sure! Tell me what you need help with, and I'll do my best to assist.",
        r"(weather)": "I'm unable to check the weather right now, but you can try asking your local weather app.",
        r"(joke)": "Why don't programmers like nature? It has too many bugs!",
        r"(favorite color)": "I like blue—it reminds me of the sky and endless possibilities!",
        r"(time)": "I'm not equipped with a clock, but the device you're using should tell you the time!",
        r"(age)": "I'm ageless! But I was created to assist you."
    }

    # Check the user's message against predefined patterns
    for pattern, response in patterns.items():
        if re.search(pattern, message):
            return response

    # Optional: Use OpenAI API for unmatched inputs
    # Uncomment the following block if you want to integrate OpenAI
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred with the AI service: {str(e)}"
    """

    # Default response for unmatched inputs
    return "I'm here to help. Could you please rephrase or ask another question?"


def chat(request):
    """
    Renders the chatbot page for interaction with users.
    """
    return render(request, 'quickbot/chat.html')



