# backend/scripts/seed.py
"""Database seeder script for initial data."""

from __future__ import annotations

import sys
from datetime import UTC, datetime

from app.domain.entities.post import Post
from app.infrastructure.database.session import get_session_factory
from app.infrastructure.repositories.post_repository import SqlAlchemyPostRepository

SAMPLE_POSTS: list[dict[str, str]] = [
    {
        "title": "Introduction to FastAPI",
        "description": (
            "FastAPI is a modern, fast web framework for building APIs with Python "
            "based on standard Python type hints. It offers high performance thanks "
            "to Starlette and automatic data validation."
        ),
    },
    {
        "title": "SQLAlchemy 2.0 Features",
        "description": (
            "SQLAlchemy 2.0 introduces a new declarative approach with Mapped "
            "annotations, better async typing support, and a more intuitive "
            "ORM. It is a major update that significantly improves the developer "
            "experience."
        ),
    },
    {
        "title": "Design Patterns in Python",
        "description": (
            "Design patterns like Repository, Unit of Work, and Dependency Injection "
            "are fundamental to keeping applications clean and testable. Python "
            "provides mechanisms like ABC and dataclasses to implement these patterns "
            "elegantly."
        ),
    },
    {
        "title": "Alembic Migrations",
        "description": (
            "Alembic is the migration tool for SQLAlchemy. It allows managing database "
            "schema changes in a versioned and reproducible way, supporting both "
            "auto-generation and manual migrations."
        ),
    },
    {
        "title": "Testing with pytest",
        "description": (
            "pytest is the most popular testing framework in Python. With fixtures, "
            "mocks, and the httpx plugin for FastAPI, it is possible to write clean "
            "and efficient integration tests without needing a real database."
        ),
    },
]


def _build_summary(description: str) -> dict[str, list[str] | str]:
    """Build a deterministic summary and keywords for a sample post."""
    summary_text = description[:80].rstrip() + ("..." if len(description) > 80 else "")
    words = [
        w
        for w in description.lower().replace(".", "").replace(",", "").split()
        if len(w) > 3
    ][:5]
    return {"summary": summary_text, "keywords": words}


def seed_posts() -> None:
    """Insert sample posts into the database if the table is empty."""
    session_factory = get_session_factory()
    session = session_factory()

    try:
        # Check if table is empty using raw SQL to avoid ORM overhead
        from sqlalchemy import text

        result = session.execute(text("SELECT COUNT(*) FROM posts"))
        existing_count = result.scalar()

        if existing_count > 0:
            print(f"Posts table already has {existing_count} rows. Skipping seed.")
            return

        repository = SqlAlchemyPostRepository(session)

        for post_data in SAMPLE_POSTS:
            domain_post = Post(
                title=post_data["title"],
                description=post_data["description"],
                summary=_build_summary(post_data["description"]),
                file_path=None,
                created_at=datetime.now(UTC),
            )
            repository.create(domain_post)

        session.commit()
        print(f"Seeded {len(SAMPLE_POSTS)} sample posts successfully.")

    except Exception as exc:
        session.rollback()
        print(f"Error seeding posts: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    seed_posts()
