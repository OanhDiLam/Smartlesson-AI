import base64
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.common.db import get_connection, init_auth_db
from services.common.security import hash_password


app = FastAPI(title="SmartLesson Auth Service")


class RegisterRequest(BaseModel):
    username: str
    fullname: str
    password: str
    avatar_base64: str = ""
    avatar_content_type: str = ""


class LoginRequest(BaseModel):
    username: str
    password: str


class FullnameUpdateRequest(BaseModel):
    fullname: str


class PasswordUpdateRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class AvatarUpdateRequest(BaseModel):
    avatar_base64: str = ""
    avatar_content_type: str = ""


@app.on_event("startup")
def startup_event():
    init_auth_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


def normalize_avatar(avatar_base64: str, avatar_content_type: str):
    avatar_base64 = (avatar_base64 or "").strip()
    avatar_content_type = (avatar_content_type or "").strip()

    if not avatar_base64:
        return "", ""

    if not avatar_content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Ảnh đại diện phải là file hình ảnh hợp lệ.")

    try:
        base64.b64decode(avatar_base64, validate=True)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Dữ liệu ảnh đại diện không hợp lệ.") from error

    return avatar_base64, avatar_content_type


@app.post("/register")
def register(payload: RegisterRequest):
    username = payload.username.strip()
    fullname = payload.fullname.strip()
    avatar_base64, avatar_content_type = normalize_avatar(
        payload.avatar_base64,
        payload.avatar_content_type,
    )

    if not username or not fullname or not payload.password:
        raise HTTPException(status_code=400, detail="Vui lòng điền đầy đủ thông tin đăng ký.")
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Mật khẩu phải có ít nhất 6 ký tự.")

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (username, password_hash, fullname, avatar_base64, avatar_content_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    username,
                    hash_password(payload.password),
                    fullname,
                    avatar_base64,
                    avatar_content_type,
                ),
            )
            connection.commit()
            return {
                "id": cursor.lastrowid,
                "username": username,
                "fullname": fullname,
                "avatar_base64": avatar_base64,
                "avatar_content_type": avatar_content_type,
            }
    except sqlite3.IntegrityError as error:
        raise HTTPException(status_code=409, detail="Tên đăng nhập này đã được sử dụng.") from error


@app.post("/login")
def login(payload: LoginRequest):
    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT id, username, fullname, avatar_base64, avatar_content_type
            FROM users
            WHERE username=? AND password_hash=?
            """,
            (payload.username.strip(), hash_password(payload.password)),
        ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác.")

    return dict(user)


@app.get("/users/{user_id}")
def get_user(user_id: int):
    with get_connection() as connection:
        user = connection.execute(
            "SELECT id, username, fullname, avatar_base64, avatar_content_type FROM users WHERE id=?",
            (user_id,),
        ).fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")

    return dict(user)


@app.put("/users/{user_id}/fullname")
def update_fullname(user_id: int, payload: FullnameUpdateRequest):
    fullname = payload.fullname.strip()
    if not fullname:
        raise HTTPException(status_code=400, detail="Họ và tên không được để trống.")

    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE users SET fullname=? WHERE id=?",
            (fullname, user_id),
        )
        connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")

    return {"id": user_id, "fullname": fullname}


@app.put("/users/{user_id}/avatar")
def update_avatar(user_id: int, payload: AvatarUpdateRequest):
    avatar_base64, avatar_content_type = normalize_avatar(
        payload.avatar_base64,
        payload.avatar_content_type,
    )

    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE users SET avatar_base64=?, avatar_content_type=? WHERE id=?",
            (avatar_base64, avatar_content_type, user_id),
        )
        connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")

    return {
        "id": user_id,
        "avatar_base64": avatar_base64,
        "avatar_content_type": avatar_content_type,
        "message": "Đã cập nhật ảnh đại diện.",
    }


@app.put("/users/{user_id}/password")
def update_password(user_id: int, payload: PasswordUpdateRequest):
    if not payload.new_password:
        raise HTTPException(status_code=400, detail="Mật khẩu mới không được để trống.")
    if len(payload.new_password) < 6:
        raise HTTPException(status_code=400, detail="Mật khẩu mới phải có ít nhất 6 ký tự.")
    if payload.new_password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Xác nhận mật khẩu mới chưa khớp.")
    if payload.current_password == payload.new_password:
        raise HTTPException(status_code=400, detail="Mật khẩu mới phải khác mật khẩu hiện tại.")

    with get_connection() as connection:
        user = connection.execute(
            "SELECT id FROM users WHERE id=? AND password_hash=?",
            (user_id, hash_password(payload.current_password)),
        ).fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Mật khẩu hiện tại không chính xác.")

        connection.execute(
            "UPDATE users SET password_hash=? WHERE id=?",
            (hash_password(payload.new_password), user_id),
        )
        connection.commit()

    return {"message": "Đã cập nhật mật khẩu."}
