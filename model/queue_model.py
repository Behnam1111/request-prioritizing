from dataclasses import dataclass, field


@dataclass(order=True)
class WorkItem:
    priority: int
    data: str = field(compare=False)
    request_id: int
    user_id: int

