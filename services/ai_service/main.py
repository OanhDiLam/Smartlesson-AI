import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "models/gemini-flash-latest")

if API_KEY:
    genai.configure(api_key=API_KEY)

app = FastAPI(title="SmartLesson AI Service")


class GenerateLessonRequest(BaseModel):
    subject: str
    grade: str
    book_series: str
    lesson_title: str
    duration: str = ""
    note: str = ""
    reference_material: str = ""


class GenerateMaterialsRequest(BaseModel):
    subject: str
    grade: str
    lesson_title: str
    lesson_content: str


def format_ai_error(error: Exception) -> str:
    message = str(error)
    lowered = message.lower()

    if "reported as leaked" in lowered or "api key was reported as leaked" in lowered:
        return "API key Gemini hiện tại đã bị Google vô hiệu hóa vì bị lộ. Hãy tạo key mới trong Google AI Studio và cập nhật file .env."
    if "api key not valid" in lowered or "invalid api key" in lowered:
        return "Gemini API key không hợp lệ. Hãy kiểm tra lại GOOGLE_API_KEY trong file .env."
    if "permission denied" in lowered or "403" in lowered:
        return "Gemini API đang bị từ chối truy cập. Hãy kiểm tra lại API key và quyền truy cập model."
    return f"Lỗi hệ thống AI: {message}"


def ensure_ai_ready():
    if not API_KEY or API_KEY.startswith("REPLACE_WITH_"):
        raise HTTPException(status_code=400, detail="Chưa cấu hình Gemini API key hợp lệ trong file .env.")


def generate_text(prompt: str) -> str:
    try:
        response = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
        return response.text
    except Exception as error:
        raise HTTPException(status_code=502, detail=format_ai_error(error)) from error


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/generate")
def generate_lesson(payload: GenerateLessonRequest):
    ensure_ai_ready()

    if not payload.lesson_title.strip():
        raise HTTPException(status_code=400, detail="Tên bài dạy không được để trống.")

    reference_block = ""
    if payload.reference_material.strip():
        reference_block = (
            "\nTài liệu tham chiếu giáo viên cung cấp:\n"
            f"{payload.reference_material[:12000]}\n"
            "Hãy ưu tiên bám sát tài liệu này khi soạn giáo án, nhưng vẫn trình bày rõ ràng và đúng cấu trúc."
        )

    prompt = (
        f"Hãy soạn giáo án môn {payload.subject} lớp {payload.grade} theo sách {payload.book_series}, "
        f"bài dạy: {payload.lesson_title}. Thời lượng: {payload.duration}. "
        f"Yêu cầu thêm: {payload.note}. Trình bày theo đúng cấu trúc Công văn 5512 của Bộ Giáo dục."
        f"{reference_block}"
    )

    return {"content": generate_text(prompt)}


@app.post("/generate-materials")
def generate_materials(payload: GenerateMaterialsRequest):
    ensure_ai_ready()

    if not payload.lesson_content.strip():
        raise HTTPException(status_code=400, detail="Nội dung giáo án không được để trống.")

    prompt = f"""
Bạn là trợ lý sư phạm cho giáo viên Việt Nam.
Hãy đọc giáo án dưới đây và tạo bộ tài liệu hỗ trợ giảng dạy cho bài "{payload.lesson_title}" môn {payload.subject} lớp {payload.grade}.

Yêu cầu đầu ra gồm đúng 3 phần, theo định dạng markdown rõ ràng:
1. CÂU HỎI KIỂM TRA
- 5 câu trắc nghiệm
- 3 câu tự luận ngắn
- đáp án ngắn gọn cho từng câu

2. RUBRIC ĐÁNH GIÁ
- bảng tiêu chí hoặc danh sách tiêu chí
- 4 mức: Xuất sắc, Tốt, Đạt, Cần cố gắng
- mô tả ngắn, dễ dùng trên lớp

3. PHIẾU HỌC TẬP
- mục tiêu phiếu
- 3 đến 5 nhiệm vụ học sinh cần làm
- phần trả lời hoặc ghi chú ngắn cho học sinh

Giáo án nguồn:
{payload.lesson_content[:18000]}
"""

    raw_content = generate_text(prompt)

    sections = {"questions": raw_content, "rubric": raw_content, "worksheet": raw_content}
    normalized = raw_content.replace("\r\n", "\n")
    matches = list(
        __import__("re").finditer(
            r"(?im)^\s*(?:#{1,6}\s*)?(CÂU HỎI KIỂM TRA|RUBRIC ĐÁNH GIÁ|PHIẾU HỌC TẬP)\s*$",
            normalized,
        )
    )
    if matches:
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
            content = normalized[start:end].strip()
            title = match.group(1).upper()
            if "CÂU HỎI" in title:
                sections["questions"] = content or sections["questions"]
            elif "RUBRIC" in title:
                sections["rubric"] = content or sections["rubric"]
            elif "PHIẾU" in title:
                sections["worksheet"] = content or sections["worksheet"]

    return {"raw_content": raw_content, **sections}
