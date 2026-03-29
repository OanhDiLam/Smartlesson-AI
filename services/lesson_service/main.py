from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from services.common.db import get_connection, init_lesson_db


app = FastAPI(title="SmartLesson Lesson Service")


class LessonCreateRequest(BaseModel):
    user_id: int
    subject: str
    grade: str
    book_series: str
    lesson_title: str
    duration: str
    content_md: str


class SharedLessonCreateRequest(BaseModel):
    uploader_id: int
    uploader_name: str
    title: str
    description: str = ""
    subject: str = ""
    grade: str = ""
    file_name: str
    content_type: str
    file_base64: str


class SharedLessonCommentRequest(BaseModel):
    commenter_id: int
    commenter_name: str
    comment: str
    parent_comment_id: int | None = None


class SharedLessonLikeRequest(BaseModel):
    user_id: int
    user_name: str


class SharedLessonCommentLikeRequest(BaseModel):
    user_id: int
    user_name: str


@app.on_event("startup")
def startup_event():
    init_lesson_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/lessons")
def create_lesson(payload: LessonCreateRequest):
    lesson_title = payload.lesson_title.strip()
    if not lesson_title:
        raise HTTPException(status_code=400, detail="Tên bài dạy không được để trống.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO lessons (
                user_id, subject, grade, book_series, lesson_title, duration, content_md
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.user_id,
                payload.subject,
                payload.grade,
                payload.book_series,
                lesson_title,
                payload.duration,
                payload.content_md,
            ),
        )
        connection.commit()

    return {"id": cursor.lastrowid, "lesson_title": lesson_title}


@app.get("/lessons/{user_id}")
def get_lessons(user_id: int):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, lesson_title, created_at, content_md, subject, grade, book_series, duration
            FROM lessons
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,),
        ).fetchall()

    return [dict(row) for row in rows]


@app.post("/shared-lessons")
def create_shared_lesson(payload: SharedLessonCreateRequest):
    title = payload.title.strip()
    uploader_name = payload.uploader_name.strip()
    file_name = payload.file_name.strip()

    if not title:
        raise HTTPException(status_code=400, detail="Tiêu đề giáo án không được để trống.")
    if not uploader_name:
        raise HTTPException(status_code=400, detail="Thiếu thông tin người tải lên.")
    if not file_name or not payload.file_base64:
        raise HTTPException(status_code=400, detail="Vui lòng chọn file giáo án để tải lên.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO shared_lessons (
                uploader_id, uploader_name, title, description, subject, grade,
                file_name, content_type, file_base64
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.uploader_id,
                uploader_name,
                title,
                payload.description.strip(),
                payload.subject.strip(),
                payload.grade.strip(),
                file_name,
                payload.content_type.strip() or "application/octet-stream",
                payload.file_base64,
            ),
        )
        connection.commit()

    return {"id": cursor.lastrowid, "title": title}


@app.get("/shared-lessons")
def get_shared_lessons(viewer_id: int | None = Query(default=None)):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                sl.id,
                sl.uploader_id,
                sl.uploader_name,
                u.avatar_base64 AS uploader_avatar_base64,
                u.avatar_content_type AS uploader_avatar_content_type,
                sl.title,
                sl.description,
                sl.subject,
                sl.grade,
                sl.file_name,
                sl.content_type,
                sl.created_at,
                COUNT(DISTINCT c.id) AS comment_count,
                COUNT(DISTINCT l.id) AS like_count
            FROM shared_lessons sl
            LEFT JOIN users u ON u.id = sl.uploader_id
            LEFT JOIN shared_lesson_comments c ON c.shared_lesson_id = sl.id
            LEFT JOIN shared_lesson_likes l ON l.shared_lesson_id = sl.id
            GROUP BY sl.id
            ORDER BY sl.id DESC
            """
        ).fetchall()

        lessons = []
        for row in rows:
            item = dict(row)
            if viewer_id is not None:
                liked_row = connection.execute(
                    "SELECT id FROM shared_lesson_likes WHERE shared_lesson_id=? AND user_id=?",
                    (item["id"], viewer_id),
                ).fetchone()
                item["liked_by_viewer"] = bool(liked_row)
            lessons.append(item)

    return lessons


@app.delete("/shared-lessons/{shared_lesson_id}")
def delete_shared_lesson(shared_lesson_id: int, requester_id: int = Query(...)):
    with get_connection() as connection:
        lesson = connection.execute(
            "SELECT uploader_id FROM shared_lessons WHERE id=?",
            (shared_lesson_id,),
        ).fetchone()
        if not lesson:
            raise HTTPException(status_code=404, detail="Không tìm thấy giáo án chia sẻ.")
        if lesson["uploader_id"] != requester_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền xóa giáo án này.")

        connection.execute("DELETE FROM shared_lesson_likes WHERE shared_lesson_id=?", (shared_lesson_id,))
        connection.execute(
            """
            DELETE FROM shared_lesson_comment_likes
            WHERE comment_id IN (
                SELECT id FROM shared_lesson_comments WHERE shared_lesson_id=?
            )
            """,
            (shared_lesson_id,),
        )
        connection.execute("DELETE FROM shared_lesson_comments WHERE shared_lesson_id=?", (shared_lesson_id,))
        connection.execute("DELETE FROM shared_lessons WHERE id=?", (shared_lesson_id,))
        connection.commit()

    return {"message": "Đã xóa giáo án chia sẻ."}


@app.post("/shared-lessons/{shared_lesson_id}/likes")
def toggle_shared_lesson_like(shared_lesson_id: int, payload: SharedLessonLikeRequest):
    with get_connection() as connection:
        lesson = connection.execute(
            "SELECT id FROM shared_lessons WHERE id=?",
            (shared_lesson_id,),
        ).fetchone()
        if not lesson:
            raise HTTPException(status_code=404, detail="Không tìm thấy giáo án chia sẻ.")

        existing_like = connection.execute(
            "SELECT id FROM shared_lesson_likes WHERE shared_lesson_id=? AND user_id=?",
            (shared_lesson_id, payload.user_id),
        ).fetchone()

        if existing_like:
            connection.execute(
                "DELETE FROM shared_lesson_likes WHERE id=?",
                (existing_like["id"],),
            )
            liked = False
        else:
            connection.execute(
                """
                INSERT INTO shared_lesson_likes (shared_lesson_id, user_id, user_name)
                VALUES (?, ?, ?)
                """,
                (shared_lesson_id, payload.user_id, payload.user_name.strip()),
            )
            liked = True

        like_count = connection.execute(
            "SELECT COUNT(*) AS count FROM shared_lesson_likes WHERE shared_lesson_id=?",
            (shared_lesson_id,),
        ).fetchone()["count"]
        connection.commit()

    return {"liked": liked, "like_count": like_count}


@app.get("/shared-lessons/{shared_lesson_id}/download")
def download_shared_lesson(shared_lesson_id: int):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, title, file_name, content_type, file_base64
            FROM shared_lessons
            WHERE id=?
            """,
            (shared_lesson_id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Không tìm thấy giáo án chia sẻ.")

    return dict(row)


@app.get("/shared-lessons/{shared_lesson_id}/comments")
def get_shared_lesson_comments(shared_lesson_id: int, viewer_id: int | None = Query(default=None)):
    with get_connection() as connection:
        lesson = connection.execute(
            "SELECT id, uploader_id FROM shared_lessons WHERE id=?",
            (shared_lesson_id,),
        ).fetchone()
        if not lesson:
            raise HTTPException(status_code=404, detail="Không tìm thấy giáo án chia sẻ.")

        rows = connection.execute(
            """
            SELECT
                c.id,
                c.commenter_id,
                c.commenter_name,
                u.avatar_base64 AS commenter_avatar_base64,
                u.avatar_content_type AS commenter_avatar_content_type,
                c.comment,
                c.created_at,
                c.parent_comment_id,
                COUNT(DISTINCT cl.id) AS like_count
            FROM shared_lesson_comments c
            LEFT JOIN users u ON u.id = c.commenter_id
            LEFT JOIN shared_lesson_comment_likes cl ON cl.comment_id = c.id
            WHERE c.shared_lesson_id=?
            GROUP BY c.id
            ORDER BY c.id ASC
            """,
            (shared_lesson_id,),
        ).fetchall()
        comments = []
        for row in rows:
            item = dict(row)
            if viewer_id is not None:
                liked_row = connection.execute(
                    "SELECT id FROM shared_lesson_comment_likes WHERE comment_id=? AND user_id=?",
                    (item["id"], viewer_id),
                ).fetchone()
                item["liked_by_viewer"] = bool(liked_row)
            else:
                item["liked_by_viewer"] = False
            comments.append(item)

    return comments


@app.post("/shared-lessons/{shared_lesson_id}/comments/{comment_id}/likes")
def toggle_shared_lesson_comment_like(
    shared_lesson_id: int,
    comment_id: int,
    payload: SharedLessonCommentLikeRequest,
):
    with get_connection() as connection:
        comment = connection.execute(
            "SELECT id FROM shared_lesson_comments WHERE id=? AND shared_lesson_id=?",
            (comment_id, shared_lesson_id),
        ).fetchone()
        if not comment:
            raise HTTPException(status_code=404, detail="Không tìm thấy bình luận.")

        existing_like = connection.execute(
            "SELECT id FROM shared_lesson_comment_likes WHERE comment_id=? AND user_id=?",
            (comment_id, payload.user_id),
        ).fetchone()

        if existing_like:
            connection.execute(
                "DELETE FROM shared_lesson_comment_likes WHERE id=?",
                (existing_like["id"],),
            )
            liked = False
        else:
            connection.execute(
                """
                INSERT INTO shared_lesson_comment_likes (comment_id, user_id, user_name)
                VALUES (?, ?, ?)
                """,
                (comment_id, payload.user_id, payload.user_name.strip()),
            )
            liked = True

        like_count = connection.execute(
            "SELECT COUNT(*) AS count FROM shared_lesson_comment_likes WHERE comment_id=?",
            (comment_id,),
        ).fetchone()["count"]
        connection.commit()

    return {"liked": liked, "like_count": like_count}


@app.post("/shared-lessons/{shared_lesson_id}/comments")
def create_shared_lesson_comment(shared_lesson_id: int, payload: SharedLessonCommentRequest):
    commenter_name = payload.commenter_name.strip()
    comment = payload.comment.strip()

    if not commenter_name:
        raise HTTPException(status_code=400, detail="Thiếu thông tin người nhận xét.")
    if not comment:
        raise HTTPException(status_code=400, detail="Nội dung góp ý không được để trống.")

    with get_connection() as connection:
        lesson = connection.execute(
            "SELECT id FROM shared_lessons WHERE id=?",
            (shared_lesson_id,),
        ).fetchone()
        if not lesson:
            raise HTTPException(status_code=404, detail="Không tìm thấy giáo án chia sẻ.")

        if payload.parent_comment_id is not None:
            parent = connection.execute(
                "SELECT id FROM shared_lesson_comments WHERE id=? AND shared_lesson_id=?",
                (payload.parent_comment_id, shared_lesson_id),
            ).fetchone()
            if not parent:
                raise HTTPException(status_code=404, detail="Không tìm thấy góp ý gốc để trả lời.")

        cursor = connection.execute(
            """
            INSERT INTO shared_lesson_comments (
                shared_lesson_id, commenter_id, commenter_name, comment, parent_comment_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                shared_lesson_id,
                payload.commenter_id,
                commenter_name,
                comment,
                payload.parent_comment_id,
            ),
        )
        connection.commit()

    return {"id": cursor.lastrowid, "message": "Đã gửi góp ý."}


@app.delete("/shared-lessons/{shared_lesson_id}/comments/{comment_id}")
def delete_shared_lesson_comment(shared_lesson_id: int, comment_id: int, requester_id: int = Query(...)):
    with get_connection() as connection:
        lesson = connection.execute(
            "SELECT uploader_id FROM shared_lessons WHERE id=?",
            (shared_lesson_id,),
        ).fetchone()
        if not lesson:
            raise HTTPException(status_code=404, detail="Không tìm thấy giáo án chia sẻ.")

        comment = connection.execute(
            "SELECT commenter_id FROM shared_lesson_comments WHERE id=? AND shared_lesson_id=?",
            (comment_id, shared_lesson_id),
        ).fetchone()
        if not comment:
            raise HTTPException(status_code=404, detail="Không tìm thấy góp ý.")
        if requester_id not in {comment["commenter_id"], lesson["uploader_id"]}:
            raise HTTPException(status_code=403, detail="Bạn không có quyền xóa góp ý này.")

        child_comment_ids = [
            row["id"]
            for row in connection.execute(
                "SELECT id FROM shared_lesson_comments WHERE parent_comment_id=? AND shared_lesson_id=?",
                (comment_id, shared_lesson_id),
            ).fetchall()
        ]
        if child_comment_ids:
            placeholders = ",".join("?" for _ in child_comment_ids)
            connection.execute(
                f"DELETE FROM shared_lesson_comment_likes WHERE comment_id IN ({placeholders})",
                tuple(child_comment_ids),
            )
        connection.execute(
            "DELETE FROM shared_lesson_comment_likes WHERE comment_id=?",
            (comment_id,),
        )
        connection.execute(
            "DELETE FROM shared_lesson_comments WHERE parent_comment_id=? AND shared_lesson_id=?",
            (comment_id, shared_lesson_id),
        )
        connection.execute(
            "DELETE FROM shared_lesson_comments WHERE id=? AND shared_lesson_id=?",
            (comment_id, shared_lesson_id),
        )
        connection.commit()

    return {"message": "Đã xóa góp ý."}
