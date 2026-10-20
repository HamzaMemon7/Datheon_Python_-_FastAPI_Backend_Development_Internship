from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

# 1. Database Setup
DATABASE_URL = "sqlite:///./app_data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. SQLAlchemy ORM Models
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    notes = relationship("DBNote", back_populates="owner")

class DBNote(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("DBUser", back_populates="notes")

# Tables auto create
Base.metadata.create_all(bind=engine)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Pydantic Schemas
class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    notes: List[NoteResponse] = []

    class Config:
        from_attributes = True

# 4. FastAPI Application
app = FastAPI(title="Persistent Notes API (SQLAlchemy + SQLite)")

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(DBUser).filter(DBUser.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username pehle se mojood hai")
    new_user = DBUser(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(DBUser).all()

@app.post("/users/{user_id}/notes/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note_for_user(user_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User nahi mila")
    new_note = DBNote(title=note.title, content=note.content, user_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/notes/", response_model=List[NoteResponse])
def get_all_notes(db: Session = Depends(get_db)):
    return db.query(DBNote).all()