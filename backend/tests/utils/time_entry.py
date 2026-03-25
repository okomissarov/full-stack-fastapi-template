from datetime import datetime, timezone

from sqlmodel import Session

from app import crud
from app.models import TimeEntry, TimeEntryCreate
from tests.utils.project import create_random_project
from tests.utils.utils import random_lower_string


def create_random_time_entry(db: Session) -> TimeEntry:
    project = create_random_project(db)
    owner_id = project.owner_id
    assert owner_id is not None
    time_entry_in = TimeEntryCreate(
        date=datetime.now(timezone.utc),
        hours=1.5,
        description=random_lower_string(),
        project_id=project.id,
    )
    return crud.create_time_entry(session=db, time_entry_in=time_entry_in, owner_id=owner_id)
