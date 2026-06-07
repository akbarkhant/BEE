from __future__ import annotations

import json
import uuid
from itertools import combinations
from typing import Any

from sqlalchemy import select

from app.database.session import AsyncSessionLocal
from app.models.problem import Problem
from app.models.relationship import Relationship
from app.models.tag import ProblemTag, Tag
from app.repositories.problem_repo import ProblemRepository, slugify
from app.core.config import get_settings


def build_markdown(entry: dict[str, Any]) -> str:
    title = entry["title"]
    description = entry.get("description", "")
    algorithm = entry.get("algorithm", "N/A")
    category = entry.get("category", "")
    difficulty = entry.get("difficulty", "Medium")
    technologies = entry.get("technologies") or []
    complexity = entry.get("complexity") or {}
    time_c = complexity.get("time") or "Varies"
    space_c = complexity.get("space") or "Varies"
    tech_lines = "\n".join(f"- {t}" for t in technologies) if technologies else "- General"

    return f"""# {title}

## Overview

{description}

## Algorithm

**{algorithm}**

## When to Apply

Use this pattern when you encounter: *{title.lower()}*.

## Category & Difficulty

| Field | Value |
|-------|-------|
| Category | {category} |
| Difficulty | {difficulty} |

## Technologies

{tech_lines}

## Complexity

| Metric | Value |
|--------|-------|
| Time | {time_c} |
| Space | {space_c} |

## Key Takeaways

- Understand the root cause before applying a fix.
- Measure impact with profiling and observability tooling.
- Combine with related patterns for production-grade resilience.
"""


async def load_seed_data() -> int:
    settings = get_settings()
    seed_file = settings.SEED_PROBLEMS_FILE
    if not seed_file.exists():
        return 0

    async with AsyncSessionLocal() as session:
        count_result = await session.execute(select(Problem).limit(1))
        if count_result.scalar_one_or_none():
            return 0

        with open(seed_file, encoding="utf-8") as f:
            data = json.load(f)

        repo = ProblemRepository(session)
        id_map: dict[int, uuid.UUID] = {}
        problems: list[Problem] = []
        problem_tag_names: dict[uuid.UUID, set[str]] = {}
        used_slugs: set[str] = set()
        
        # Collect ALL unique tags from your 150 entries up front
        all_unique_tags: set[str] = set()
        problems_list = data.get("problems", [])
        for entry in problems_list:
            all_unique_tags.update(entry.get("tags") or [])

        # Bulk pre-populate or resolve tags in-memory to prevent N+1 queries
        tag_cache: dict[str, Tag] = {}
        for tag_name in all_unique_tags:
            tag_cache[tag_name] = await repo.get_or_create_tag(tag_name)

        # Process Problems
        for entry in problems_list:
            problem_id = uuid.uuid4()
            legacy_id = entry.get("id")
            if legacy_id is not None:
                id_map[legacy_id] = problem_id

            slug = slugify(entry["title"])
            if slug in used_slugs:
                slug = f"{slug}-{str(problem_id)[:8]}"
            used_slugs.add(slug)
            explanation = entry.get("description", "")[:500]

            problem = Problem(
                id=problem_id,
                slug=slug,
                title=entry["title"],
                category=entry.get("category", "General"),
                algorithm=entry.get("algorithm"),
                difficulty=entry.get("difficulty", "Medium"),
                explanation=explanation,
                markdown_content=build_markdown(entry),
                technologies=entry.get("technologies") or [],
                complexity=entry.get("complexity"),
            )
            session.add(problem)
            problems.append(problem)

            # Link tags instantly out of cache without hitting the DB again
            tag_names = set(entry.get("tags") or [])
            problem_tag_names[problem_id] = tag_names
            for tag_name in tag_names:
                resolved_tag = tag_cache[tag_name]
                session.add(ProblemTag(problem_id=problem_id, tag_id=resolved_tag.id))

        await session.flush()

        # Explicit Relationships from JSON
        existing_pairs: set[tuple] = set()
        for entry in problems_list:
            legacy_id = entry.get("id")
            if legacy_id not in id_map:
                continue
            source_id = id_map[legacy_id]
            for related in entry.get("related_problems") or []:
                target_id = id_map.get(related)
                if not target_id or source_id == target_id:
                    continue
                pair = tuple(sorted((source_id, target_id)))
                if pair in existing_pairs:
                    continue
                existing_pairs.add(pair)
                session.add(
                    Relationship(
                        source_id=source_id,
                        target_id=target_id,
                        relationship_type="related_to",
                        strength=1.0,
                    )
                )

        # Implicit Graph Generation (Category proximity + shared tags)
        for p1, p2 in combinations(problems, 2):
            if p1.category != p2.category:
                continue
            shared = problem_tag_names.get(p1.id, set()).intersection(
                problem_tag_names.get(p2.id, set())
            )
            if not shared:
                continue
            pair = tuple(sorted((p1.id, p2.id)))
            if pair in existing_pairs:
                continue
            existing_pairs.add(pair)
            strength = min(1.0, 0.3 + 0.2 * len(shared))
            session.add(
                Relationship(
                    source_id=p1.id,
                    target_id=p2.id,
                    relationship_type="related_to",
                    strength=strength,
                )
            )

        await session.commit()
        return len(problems)
