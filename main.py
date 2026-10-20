from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="BookStore API")

# Pydantic Model validation ke liye
class Book(BaseModel):
    id: int
    title: str = Field(..., min_length=1, description="Kitab ka naam")
    author: str = Field(..., min_length=1, description="Musannif ka naam")
    price: float = Field(..., gt=0, description="Price 0 se zyada honi chahiye")

# In-memory storage (Data save rakhne ke liye temporary database)
books_db: List[Book] = [
    Book(id=1, title="Python Basics", author="Guido", price=19.99),
    Book(id=2, title="FastAPI Guide", author="Tiangolo", price=29.99)
]

# 1. Saari books dekhna ya filter karna (GET)
@app.get("/books", response_model=List[Book])
def get_all_books(max_price: Optional[float] = None):
    if max_price:
        return [b for b in books_db if b.price <= max_price]
    return books_db

# 2. Kisi specific book ko ID se dekhna (GET)
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book nahi mili!")

# 3. Nayi book add karna (POST)
@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    for b in books_db:
        if b.id == book.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Yeh ID pehle se mojood hai!")
    books_db.append(book)
    return book

# 4. Book update karna (PUT)
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, b in enumerate(books_db):
        if b.id == book_id:
            books_db[index] = updated_book
            return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update ke liye book nahi mili!")

# 5. Book delete karna (DELETE)
@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int):
    for index, b in enumerate(books_db):
        if b.id == book_id:
            books_db.pop(index)
            return {"message": "Book kamyabi se delete ho gayi!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delete ke liye book nahi mili!")