"""
Purpose: Define all SQLModel database tables and Pydantic API schemas for User, Item, Project, and TimeEntry entities

Structure:
    User (table): entity - User account with auth and profile data
    Item (table): entity - User-owned content item
    Project (table): entity - User-owned project for time tracking
    TimeEntry (table): entity - Time entry linked to a project and owned by a user
    UserBase, UserCreate, UserUpdate, UserRegister, UserUpdateMe, UpdatePassword: schema - User API schemas
    UserPublic, UsersPublic: schema - User response schemas
    ItemBase, ItemCreate, ItemUpdate: schema - Item API schemas
    ItemPublic, ItemsPublic: schema - Item response schemas
    ProjectBase, ProjectCreate, ProjectUpdate: schema - Project API schemas
    ProjectPublic, ProjectsPublic: schema - Project response schemas
    TimeEntryBase, TimeEntryCreate, TimeEntryUpdate: schema - TimeEntry API schemas
    TimeEntryPublic, TimeEntriesPublic: schema - TimeEntry response schemas
    Token, TokenPayload, NewPassword, Message: schema - Auth and utility schemas

Relationships:
    Produces: user table, item table, project table, timeentry table
    Consumes: (consumed by) api.routes, crud, core.db

Semantics:
    Domain: identity, content, time-tracking
    Entity: User, Item, Project, TimeEntry
    Logic: [Items/Projects/TimeEntries cascade-delete with owner, UUIDs as primary keys, created_at auto-set to UTC]

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
    projects: list["Project"] = Relationship(back_populates="owner", cascade_delete=True)
    time_entries: list["TimeEntry"] = Relationship(back_populates="owner", cascade_delete=True)


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


# Project models and schemas


class ProjectBase(SQLModel):
    """Purpose: Shared project fields for all project schemas"""
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    status: str = Field(default="active", max_length=50)


class ProjectCreate(ProjectBase):
    """Purpose: Schema for project creation"""
    pass


class ProjectUpdate(ProjectBase):
    """Purpose: Schema for project update (all fields optional)"""
    name: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    status: str | None = Field(default=None, max_length=50)  # type: ignore


class Project(ProjectBase, table=True):
    """Purpose: Project database table owned by a User (cascade-deletes with owner)"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="projects")
    time_entries: list["TimeEntry"] = Relationship(back_populates="project", cascade_delete=True)


class ProjectPublic(ProjectBase):
    """Purpose: Project response schema with owner reference"""
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ProjectsPublic(SQLModel):
    """Purpose: Paginated project list response"""
    data: list[ProjectPublic]
    count: int


# TimeEntry models and schemas


class TimeEntryBase(SQLModel):
    """Purpose: Shared time entry fields for all time entry schemas"""
    date: datetime = Field(sa_type=DateTime(timezone=True))
    hours: float = Field(ge=0.25, le=24)
    description: str | None = Field(default=None, max_length=255)
    billable: bool = True
    project_id: uuid.UUID


class TimeEntryCreate(TimeEntryBase):
    """Purpose: Schema for time entry creation"""
    pass


class TimeEntryUpdate(TimeEntryBase):
    """Purpose: Schema for time entry update (all fields optional)"""
    date: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))  # type: ignore
    hours: float | None = Field(default=None, ge=0.25, le=24)  # type: ignore
    project_id: uuid.UUID | None = None  # type: ignore


class TimeEntry(TimeEntryBase, table=True):
    """Purpose: TimeEntry database table owned by a User and linked to a Project (cascade-deletes with owner and project)"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    project_id: uuid.UUID = Field(
        foreign_key="project.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="time_entries")
    project: Project | None = Relationship(back_populates="time_entries")


class TimeEntryPublic(TimeEntryBase):
    """Purpose: TimeEntry response schema with owner and project references"""
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class TimeEntriesPublic(SQLModel):
    """Purpose: Paginated time entry list response"""
    data: list[TimeEntryPublic]
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
