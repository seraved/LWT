from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class Pagination:
    page: int = 1
    per_page: int = 3

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page
