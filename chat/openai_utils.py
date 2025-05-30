from openai import OpenAI, OpenAIError
from typing import List
from .weather import get_weather
from .models import Message
import json
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_ai(conversation_messages: List[Message]) -> str:
    functions = [
        {
            "name": "get_weather",
            "description": "Get current weather by city name",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    ]

    messages = []
    for msg in conversation_messages:
        role = "assistant" if msg.is_assistant else "user"
        messages.append({
            "role": role,
            "content": msg.content
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
    except OpenAIError as e:
        return f"Error while contacting OpenAI API: {str(e)}"

    reply = response.choices[0].message

    if reply.function_call:
        try:
            arguments = json.loads(reply.function_call.arguments)
            city = arguments.get("city")
            if not city:
                return "City name was not provided for the weather request."
            return get_weather(city)
        except (json.JSONDecodeError, KeyError) as e:
            return f"Error while processing function call: {str(e)}"

    return reply.content or "No response from assistant"
