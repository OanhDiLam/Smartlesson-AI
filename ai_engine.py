import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Dùng đúng cấu hình cũ của thầy
MODEL_NAME = 'models/gemini-flash-latest'

def generate_lesson_plan(mon, lop, nxb, ten, tg, note):
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = f"""
    Hãy đóng vai một giáo viên giỏi, soạn giáo án chi tiết cho:
    Môn: {mon}, Lớp: {lop}, Bộ sách: {nxb}
    Tên bài dạy: {ten}, Thời lượng: {tg}
    Yêu cầu bổ sung: {note}
    
    Yêu cầu trình bày: Sử dụng định dạng Markdown, ngôn ngữ Tiếng Việt, 
    đầy đủ các bước lên lớp (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng).
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi gọi AI: {str(e)}"