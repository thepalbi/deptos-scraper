from dataclasses import dataclass

@dataclass
class FetcherResponse:
    status_code: int
    text: str