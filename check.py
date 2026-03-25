import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- Danh sách Model mà API Key của bro có quyền dùng ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"ID chuẩn: {m.name}")
except Exception as e:
    print(f"Lỗi khi list model: {e}")