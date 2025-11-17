import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import create_document, get_documents, db
from schemas import Booking

app = FastAPI(title="Choose Marketers API", description="Backend for booking page")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Choose Marketers Backend Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# -------- Recruitment Booking Endpoints --------

class BookingResponse(BaseModel):
    id: str
    full_name: str
    company: str
    email: str
    phone: Optional[str] = None
    role_title: str
    hiring_need: str
    candidates_needed: Optional[int] = None
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None
    timezone: Optional[str] = None
    message: Optional[str] = None
    status: str


@app.post("/bookings", response_model=BookingResponse)
def create_booking(booking: Booking):
    try:
        inserted_id = create_document("booking", booking)
        return BookingResponse(
            id=inserted_id,
            **booking.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/bookings", response_model=List[BookingResponse])
def list_bookings(limit: int = 50):
    try:
        docs = get_documents("booking", limit=limit)
        results: List[BookingResponse] = []
        for d in docs:
            # Convert ObjectId
            doc_id = str(d.get("_id")) if d.get("_id") else ""
            payload = {
                "id": doc_id,
                "full_name": d.get("full_name", ""),
                "company": d.get("company", ""),
                "email": d.get("email", ""),
                "phone": d.get("phone"),
                "role_title": d.get("role_title", ""),
                "hiring_need": d.get("hiring_need", ""),
                "candidates_needed": d.get("candidates_needed"),
                "preferred_date": d.get("preferred_date"),
                "preferred_time": d.get("preferred_time"),
                "timezone": d.get("timezone"),
                "message": d.get("message"),
                "status": d.get("status", "new"),
            }
            results.append(BookingResponse(**payload))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
