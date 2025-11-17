"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Recruitment Booking schema for clients (Choose Marketers)
class Booking(BaseModel):
    """
    Bookings from clients wanting to schedule a call about hiring needs.
    Collection name: "booking"
    """
    full_name: str = Field(..., min_length=2, description="Client's full name")
    company: str = Field(..., min_length=2, description="Client company name")
    email: EmailStr = Field(..., description="Business email")
    phone: Optional[str] = Field(None, description="Contact number")
    role_title: str = Field(..., min_length=2, description="Role or function they want to hire for")
    hiring_need: Literal[
        "Single hire",
        "Multiple hires",
        "Ongoing hiring",
        "Exploratory call"
    ] = Field(..., description="Type of hiring need")
    candidates_needed: Optional[int] = Field(None, ge=1, le=1000, description="Approximate number of hires")
    preferred_date: Optional[str] = Field(None, description="Preferred date (YYYY-MM-DD)")
    preferred_time: Optional[str] = Field(None, description="Preferred time (HH:MM)")
    timezone: Optional[str] = Field(None, description="Client's timezone (e.g., UTC, PST, IST)")
    message: Optional[str] = Field(None, max_length=2000, description="Additional context or notes")
    status: Literal["new", "contacted", "scheduled", "closed"] = Field("new", description="Internal status")
