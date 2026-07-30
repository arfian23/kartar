from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.core.security import hash_password
from app.models.anggota import Anggota

router = APIRouter(
    prefix="/api/users",
    tags=["Users API"]
)


# =====================================
# GET ALL USERS
# =====================================
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return (
        db.query(User)
        .order_by(User.id.desc())
        .all()
    )

# =====================================
# GET LIST ANGGOTA
# =====================================
@router.get("/anggota/list")
def get_anggota_list(db: Session = Depends(get_db)):

    anggota = (
        db.query(Anggota)
        .order_by(Anggota.nama.asc())
        .all()
    )

    return anggota


# =====================================
# GET USER BY ID
# =====================================
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    return user


# =====================================
# CREATE USER
# =====================================
@router.post("/", response_model=UserResponse)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    cek = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if cek:
        raise HTTPException(
            status_code=400,
            detail="Username sudah digunakan"
        )

    hashed_password = hash_password(data.password)

    user = User(
        username=data.username,
        password=hashed_password,
        nama_lengkap=data.nama_lengkap,
        role=data.role,
        status=data.status,
        anggota_id=data.anggota_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =====================================
# UPDATE USER
# =====================================
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    user.username = data.username
    user.nama_lengkap = data.nama_lengkap
    user.role = data.role
    user.status = data.status
    user.anggota_id = data.anggota_id

    if data.password:
        user.password = hash_password(data.password)

    db.commit()
    db.refresh(user)

    return user


# =====================================
# DELETE USER
# =====================================
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User berhasil dihapus"
    }
