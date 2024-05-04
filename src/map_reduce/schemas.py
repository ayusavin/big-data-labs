import asyncio
from datetime import date, timedelta
from enum import Enum
from functools import partial
from itertools import pairwise
from typing import Iterable, AsyncIterable, Any
from urllib.parse import quote

from pydantic import BaseModel

from .utils.dependencies import http_client_factory
from .utils import range

http_client_factory = partial(
    http_client_factory,
    base_url="https://rasp.omgtu.ru/api",
)

ZERO_TIMEDELTA: timedelta = timedelta()
THIRD_YEAR: timedelta = timedelta(days=122)

# Using in model validation process to classify
# schedule api objects
_api_guard = object()
API_GUARD_KEY: str = "__api_guard"


class NestedLecturer(BaseModel):
    id: int
    name: str

    @classmethod
    def model_validate(cls, obj, *args, **kwargs) -> "NestedLecturer":
        if isinstance(obj, dict) and obj.get(API_GUARD_KEY) is _api_guard:
            return NestedLecturer(id=obj["id"], name=obj["label"])
        return super().model_validate(obj, *args, **kwargs)

    @classmethod
    async def find_lecturers(
        cls, term: str, *, http_client_factory=http_client_factory
    ) -> AsyncIterable["NestedLecturer"]:
        async with http_client_factory() as client:
            response = await client.get(
                f"/search?term={quote(term)}&type=person",
            )

        body: list[dict] = response.json()
        for obj in body:
            obj[API_GUARD_KEY] = _api_guard
            yield cls.model_validate(obj)


class ClassTypeEnum(Enum):
    practice = "Практические занятия"
    lab = "Лабораторные работы"
    lecture = "Лекция"
    retake = "Пересдача задолженностей"
    consultation = "Консультации перед экзаменом"
    exam = "Экзамен"
    no_type = None


class Class(BaseModel):
    lecturer: NestedLecturer
    discipline_name: str
    type: ClassTypeEnum
    auditorium: str

    @classmethod
    def model_validate(cls, obj, *args, **kwargs) -> "Class":
        if isinstance(obj, dict) and obj.get(API_GUARD_KEY) is _api_guard:
            return Class(
                lecturer=obj["lecturer"],
                discipline_name=obj["discipline"],
                type=obj["kindOfWork"],
                auditorium=obj["auditorium"],
            )
        return super().model_validate(obj, *args, **kwargs)

    @classmethod
    async def list_classes_by_lecturer(
        cls,
        lecturer_id: int,
        begin: date,
        end: date,
        *,
        http_client_factory=http_client_factory,
    ) -> AsyncIterable["Class"]:
        if begin - end < ZERO_TIMEDELTA:
            begin, end = end, begin
        ranges: Iterable[tuple[date, date]] = pairwise(
            range(begin, end, THIRD_YEAR),
        )

        for (begin, end) in ranges:
            async with http_client_factory() as client:
                response = await client.get(
                    f"/schedule/person/{lecturer_id}"
                    f"?start={begin:%Y.%m.%d}&finish={end:%Y.%m.%d}&lng=1"
                )
            body: list[dict] = response.json()
            for lecture in body:
                lecture[API_GUARD_KEY] = _api_guard
                lecture["lecturer"] = NestedLecturer(
                    id=lecturer_id, name=lecture["lecturer"]
                )
                yield cls.model_validate(lecture)
