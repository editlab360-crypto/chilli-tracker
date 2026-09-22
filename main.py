import requests
import os
from google import genai
from datetime import datetime

def send_chilli_updates():
    # නිවැරදි Gemini API Key එක
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 
    TELEGRAM_BOT_TOKEN = "8691990282:AAH47_UaybjVWzdGL6XiE0miiLSWNS9RWzc"
    TELEGRAM_CHAT_ID = "8206066556"
    WEATHER_API_KEY = "e497834b0902926e551f81c94c3b352"

    LAT = "6.988084"
    LON = "81.370014"

    PLANTED_DATE = datetime(2026, 9, 18) 

    today = datetime.now()
    age_in_days = (today - PLANTED_DATE).days

    weather_info = "කාලගුණ දත්ත ලබාගැනීමට නොහැකි විය."
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={WEATHER_API_KEY}&units=metric"
        w_res = requests.get(weather_url).json()
        
        temp = w_res['main']['temp']
        desc = w_res['weather'][0]['description']
        humidity = w_res['main']['humidity']
        weather_info = f"උෂ්ණත්වය: {temp}°C, වාතාවරණය: {desc}, ආර්ද්‍රතාවය: {humidity}%"
    except Exception as e:
        print("Weather API Error:", e)

    user_question = f"""
මම නයි මිරිස් ඇට තවන් කරලා තියෙන්නේ Tray වල. 
අද දිනට තවනට වයස දවස් {age_in_days} යි.
අපේ වගාබිම පිහිටි ස්ථානයේ අද කාලගුණය: {weather_info}

කරුණාකර මට පහත සඳහන් කරුණු ඇතුළත් කරලා අද දිනට අදාළ උපදෙස් මාලාවක් සිංහලෙන් දෙන්න:

1. අද දින (දවස් {age_in_days} දී) ට්‍රේ (Tray) එළියට (අව්වට) දාන්න හොඳම වෙලාව සහ නැවත සෙවණට ගන්න ඕන වෙලාව.
2. දවස් {age_in_days} ක් වයස නයි මිරිස් පැළ වලට අද සහ ඉදිරි දවස් ටිකේ වෙන්න ඕන විශේෂ සත්කාර.
3. උඩ සඳහන් කරපු අද කාලගුණය අනුව (රස්නය/වැස්ස) අද වතුර දාන්න ඕන ප්‍රමාණය සහ හෙට දවස සඳහා වතුර පාලනය කරන්නේ කොහොමද කියන එක.

කරුණාකර Telegram එකේ කියවන්න ලේසි වෙන විදියට කරුණු (Bullet points) සහ Emojis යොදාගෙන පිළිතුර ලබාදෙන්න.
"""

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_question
        )
        ai_answer = response.text
    except Exception as e:
        print("Gemini API Error:", e)
        ai_answer = f"Gemini API Error: {e}"

    # Telegram එකට Message එක යැවීම
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🌶️ නයි මිරිස් වගා උපදෙස් (දවස {age_in_days}) 🌶️\n📍 Location Weather Included\n\n{ai_answer}"
        }

        tg_response = requests.post(telegram_url, json=payload)
        print("Telegram Status Code:", tg_response.status_code)
    except Exception as e:
        print("Telegram Error:", e)

if __name__ == "__main__":
    send_chilli_updates()
