# 🚀 SmartLesson AI - Trợ Lý Soạn Giảng Thông Minh (AI Lesson Planner)

**SmartLesson AI** là một ứng dụng hỗ trợ giáo viên soạn thảo giáo án tự động dựa trên Trí tuệ nhân tạo (AI), giúp tối ưu hóa thời gian soạn bài và đảm bảo cấu trúc sư phạm chuẩn theo **Công văn 5512** của Bộ Giáo dục & Đào tạo.

---

## 👥 Nhóm Thực Hiện (Project Team)
Dự án được thực hiện bởi nhóm học viên Cao học Công nghệ phần mềm:
* **Thạch Lâm Oanh Đi (Team Leader):** * Thiết kế kiến trúc hệ thống (System Architecture).
    * Tích hợp và tối ưu hóa Prompt cho **Google Gemini 3 Flash API**.
    * Quản trị Cơ sở dữ liệu **SQLite** & Bảo mật người dùng (SHA-256).
* **Phạm Trần Minh Thuận (Frontend Developer):**
    * Thiết kế giao diện người dùng (UX/UI) trên nền tảng **Streamlit**.
    * Xử lý module xuất bản định dạng văn bản chuyên nghiệp (.docx).
    * Kiểm thử hệ thống và xây dựng tài liệu hướng dẫn.

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)
* **Ngôn ngữ:** Python 3.10+
* **Giao diện:** Streamlit (Tông màu chủ đạo: Trắng - Tím Sư phạm)
* **Trí tuệ nhân tạo:** Google Gemini 1.5/3 Flash (Xử lý ngôn ngữ tự nhiên)
* **Cơ sở dữ liệu:** SQLite3 (Lưu trữ tài khoản & Lịch sử soạn giảng)
* **Thư viện chính:** * `google-generativeai`: Kết nối bộ não AI.
    * `python-docx`: Trình xuất bản giáo án chuẩn Word.
    * `python-dotenv`: Bảo mật thông tin cấu hình và API Key.

---

## ✨ Tính Năng Nổi Bật
1. **Quản lý người dùng:** Đăng ký/Đăng nhập riêng tư, bảo mật dữ liệu giáo án cá nhân.
2. **Soạn bài đa năng:** Hỗ trợ nhiều môn học (Tiếng Anh, Tin học, Toán...) và các khối lớp (10, 11, 12).
3. **Tùy chỉnh linh hoạt:** Lựa chọn bộ sách (Cánh Diều, Kết nối tri thức...) và phong cách soạn thảo (Trọng tâm/Chi tiết).
4. **Kho lưu trữ thông minh:** Tự động lưu và cho phép xem lại các giáo án đã soạn trong quá khứ.
5. **Xuất bản nhanh chóng:** Tải giáo án về máy dưới dạng file Word (.docx) chỉ với một cú click.

---

## 🏁 Hướng Dẫn Cài Đặt (Setup)
1. **Clone Repo:**
   ```bash
   git clone [https://github.com/OanhDiLam/Smartlesson-AI.git](https://github.com/OanhDiLam/Smartlesson-AI.git)
   cd Smartlesson-AI
2. **Cài đặt thư viện**
   ```bash
   pip install -r requirements.txt
   
3. **Cấu hình: Tạo file .env và thêm GOOGLE_API_KEY=your_key_here.**
4. **Khởi chạy:**

    ```bash
   streamlit run app.py
**Dự án phục vụ mục đích nghiên cứu và hỗ trợ giảng dạy tại Việt Nam.**

