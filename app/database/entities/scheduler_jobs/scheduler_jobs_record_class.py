from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from database.entities.users import UserRecord
from database.entities.scheduler_jobs.work_class import SchedulerJob


@dataclass(slots=True)
class SchedulerJobsRecord:
    id: UUID
    executeTime: datetime
    data: SchedulerJob
    user: UserRecord
    createdAt: datetime
    updatedAt: datetime
    lock: bool
    done: bool
