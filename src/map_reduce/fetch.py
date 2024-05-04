import asyncio
from operator import methodcaller
from typing import Iterable
from datetime import date
import json

from src.map_reduce.schemas import NestedLecturer, Class


async def main() -> None:
    # Fetch lecturers
    with open('teachers', 'r') as file:
        lecturer_names = {
            line.strip("\n").lower()
            for line in file.readlines()
        }
    lecturers: Iterable[NestedLecturer] = [
        lecturer
        for name in lecturer_names
        async for lecturer in NestedLecturer.find_lecturers(name)
    ]

    # Fetch lectures
    lectures: Iterable[Class] = [
        lecture
        for lecturer in lecturers
        async for lecture in Class.list_classes_by_lecturer(
            lecturer.id,
            begin=date(2024, 2, 1),
            end=date(2024, 6, 1)
        )
        if " ".join(lecture.lecturer.name.strip().split(" ")[-2:]).lower() in lecturer_names
    ]

    # Dump lectures
    lectures_json: Iterable[str] = [
        lecture.model_dump_json()
        for lecture in lectures
    ]
    with open('lectures.json', 'wb') as file:
        file.write(
            "\n".join(
                json.dumps(lecture, ensure_ascii=False)
                for lecture in lectures_json
            ).encode("utf-8")
        )

if __name__ == '__main__':
    asyncio.run(main())
