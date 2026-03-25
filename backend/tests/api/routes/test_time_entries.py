import uuid
from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.time_entry import create_random_time_entry
from tests.utils.project import create_random_project


def test_create_time_entry(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    project = create_random_project(db)
    data = {
        "date": datetime.now(timezone.utc).isoformat(),
        "hours": 2.5,
        "description": "Test work",
        "project_id": str(project.id),
    }
    response = client.post(
        f"{settings.API_V1_STR}/time-entries/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["hours"] == data["hours"]
    assert content["description"] == data["description"]
    assert content["project_id"] == str(project.id)
    assert "id" in content
    assert "owner_id" in content


def test_create_time_entry_invalid_project(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "date": datetime.now(timezone.utc).isoformat(),
        "hours": 1.0,
        "description": "Test",
        "project_id": str(uuid.uuid4()),
    }
    response = client.post(
        f"{settings.API_V1_STR}/time-entries/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_time_entry_hours_too_low(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    project = create_random_project(db)
    data = {
        "date": datetime.now(timezone.utc).isoformat(),
        "hours": 0.1,
        "description": "Test",
        "project_id": str(project.id),
    }
    response = client.post(
        f"{settings.API_V1_STR}/time-entries/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422


def test_create_time_entry_hours_too_high(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    project = create_random_project(db)
    data = {
        "date": datetime.now(timezone.utc).isoformat(),
        "hours": 25,
        "description": "Test",
        "project_id": str(project.id),
    }
    response = client.post(
        f"{settings.API_V1_STR}/time-entries/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422


def test_read_time_entry(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    time_entry = create_random_time_entry(db)
    response = client.get(
        f"{settings.API_V1_STR}/time-entries/{time_entry.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(time_entry.id)
    assert content["owner_id"] == str(time_entry.owner_id)
    assert content["project_id"] == str(time_entry.project_id)


def test_read_time_entry_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/time-entries/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Time entry not found"


def test_read_time_entry_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    time_entry = create_random_time_entry(db)
    response = client.get(
        f"{settings.API_V1_STR}/time-entries/{time_entry.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_read_time_entries(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_time_entry(db)
    create_random_time_entry(db)
    response = client.get(
        f"{settings.API_V1_STR}/time-entries/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_time_entry(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    time_entry = create_random_time_entry(db)
    data = {"hours": 3.0, "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/time-entries/{time_entry.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["hours"] == 3.0
    assert content["description"] == "Updated description"
    assert content["id"] == str(time_entry.id)


def test_update_time_entry_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"hours": 3.0}
    response = client.put(
        f"{settings.API_V1_STR}/time-entries/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Time entry not found"


def test_update_time_entry_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    time_entry = create_random_time_entry(db)
    data = {"hours": 3.0}
    response = client.put(
        f"{settings.API_V1_STR}/time-entries/{time_entry.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_delete_time_entry(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    time_entry = create_random_time_entry(db)
    response = client.delete(
        f"{settings.API_V1_STR}/time-entries/{time_entry.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Time entry deleted successfully"


def test_delete_time_entry_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/time-entries/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Time entry not found"


def test_delete_time_entry_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    time_entry = create_random_time_entry(db)
    response = client.delete(
        f"{settings.API_V1_STR}/time-entries/{time_entry.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_read_time_entries_summary(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_time_entry(db)
    response = client.get(
        f"{settings.API_V1_STR}/time-entries/summary",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    if len(content) > 0:
        assert "project_id" in content[0]
        assert "project_name" in content[0]
        assert "total_hours" in content[0]


def test_read_time_entries_summary_with_date_filter(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/time-entries/summary",
        headers=superuser_token_headers,
        params={
            "start_date": "2020-01-01T00:00:00Z",
            "end_date": "2020-12-31T23:59:59Z",
        },
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
