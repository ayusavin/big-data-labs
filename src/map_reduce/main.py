from typing import Iterable

from mrjob.job import MRJob as mjMRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol, TextProtocol

from src.map_reduce.schemas import Class


class MRJob(mjMRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = TextProtocol


class MRClassesCount(MRJob):
    def mapper(self, _, obj: str):
        lesson: Class = Class.model_validate_json(obj)
        yield lesson.lecturer.name, 1

    def reducer(self, word, counts):
        yield word, str(sum(counts))


class MRMostFrequentDiscipline(MRJob):
    def steps(self) -> Iterable[MRStep]:
        return [
            MRStep(
                mapper=self.mapper,
                combiner=self.combiner,
                reducer=self.reducer,
            ),
            MRStep(reducer=self.max_counts_reducer),
        ]

    def mapper(self, _, obj: str):
        lesson: Class = Class.model_validate_json(obj)
        lecturer = lesson.lecturer
        yield (lecturer.name, lesson.discipline_name), 1

    def combiner(
        self,
        lecturer_discipline: tuple[str, str],
        counts: Iterable[int],
    ):
        yield lecturer_discipline, sum(counts)

    def reducer(self, lecturer_discipline: tuple[str, str], counts: Iterable[int]):
        lecturer, discipline = lecturer_discipline
        yield lecturer, (sum(counts), discipline)

    def max_counts_reducer(self, lecturer: str, counts: Iterable[tuple[int, str]]):
        count, name = max(counts)
        yield lecturer, f"{name} -- {count} times"


class MRLessonTypesCounts(MRJob):
    def mapper(self, _, obj: str):
        lesson: Class = Class.model_validate_json(obj)
        lecturer = lesson.lecturer
        yield f"{lecturer.name} -- {lesson.type.value}", 1

    def reducer(self, lecturer: str, hours: Iterable[int]):
        yield lecturer, f"{sum(hours)} hours"


class MRMostFrequentAuditorium(MRJob):
    def steps(self) -> Iterable[MRStep]:
        return [
            MRStep(
                mapper=self.mapper_get_auditoriums,
                combiner=self.combiner_count_auditoriums,
                reducer=self.reducer_split_auditoriums,
            ),
            MRStep(reducer=self.reducer_count_max),
        ]

    def mapper_get_auditoriums(self, _, obj: str):
        lesson: Class = Class.model_validate_json(obj)
        lecturer = lesson.lecturer
        yield (lecturer.name, lesson.auditorium), 1

    def combiner_count_auditoriums(
        self, lecturer_auditorium: tuple[str, str], counts: Iterable[int]
    ):
        yield lecturer_auditorium, sum(counts)

    def reducer_split_auditoriums(
        self, lecturer_auditorium: tuple[str, str], occurencies: Iterable[int]
    ):
        (lecturer, auditorium) = lecturer_auditorium
        yield lecturer, (sum(occurencies), auditorium)

    def reducer_count_max(
        self,
        lecturer: str,
        auditoriums: Iterable[tuple[int, str]],
    ):
        count, name = max(auditoriums)
        yield lecturer, f"{name} -- {count} times"


if __name__ == "__main__":
    MRMostFrequentDiscipline.run()
