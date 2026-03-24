"""
Purpose: Define all SQLModel database tables and Pydantic API schemas for User and Item entities

Structure:
    User (table): entity - User account with auth and profile data
    Item (table): entity - User-owned content item
    UserBase, UserCreate, UserUpdate, UserRegister, UserUpdateMe, UpdatePassword: schema - User API schemas
    UserPublic, UsersPublic: schema - User response schemas
    ItemBase, ItemCreate, ItemUpdate: schema - Item API schemas
    ItemPublic, ItemsPublic: schema - Item response schemas
    Token, TokenPayload, NewPassword, Message: schema - Auth and utility schemas

Relationships:
    Produces: user table, item table
    Consumes: (consumed by) api.routes, crud, core.db

Semantics:
    Domain: identity, content
    Entity: User, Item
    Logic: [Items cascade-delete with owner, UUIDs as primary keys, created_at auto-set to UTC]

Important:
    All SQLModel table classes MUST be imported before Alembic or init_db runs,
    otherwise relationships fail to initialize. See core/db.py comment.
"""

import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    """Purpose: Return current UTC datetime for default timestamps"""
    return datetime.now(timezone.utc)


class UserBase(SQLModel):
    """Purpose: Shared user fields for all user schemas"""
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    """Purpose: Schema for admin user creation (includes role flags from UserBase)"""
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    """Purpose: Schema for public self-registration (no role flags)"""
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    """Purpose: Schema for admin user update (all fields optional)"""
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    """Purpose: Schema for self-profile update (name and email only)"""
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    """Purpose: Schema for authenticated password change"""
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class User(UserBase, table=True):
    """Purpose: User database table with auth credentials and owned items"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


class UserPublic(UserBase):
    """Purpose: User response schema (excludes hashed_password)"""
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    """Purpose: Paginated user list response"""
    data: list[UserPublic]
    count: int


class ItemBase(SQLModel):
    """Purpose: Shared item fields for all item schemas"""
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ItemCreate(ItemBase):
    """Purpose: Schema for item creation"""
    pass


class ItemUpdate(ItemBase):
    """Purpose: Schema for item update (all fields optional)"""
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


class Item(ItemBase, table=True):
    """Purpose: Item database table owned by a User (cascade-deletes with owner)"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    """Purpose: Item response schema with owner reference"""
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    """Purpose: Paginated item list response"""
    data: list[ItemPublic]
    count: int


class Message(SQLModel):
    """Purpose: Generic API message response"""
    message: str


class Token(SQLModel):
    """Purpose: JWT access token response"""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    """Purpose: Decoded JWT token payload (sub = user ID)"""
    sub: str | None = None


class NewPassword(SQLModel):
    """Purpose: Schema for token-based password reset"""
    token: str
    new_password: str = Field(min_length=8, max_length=128)
