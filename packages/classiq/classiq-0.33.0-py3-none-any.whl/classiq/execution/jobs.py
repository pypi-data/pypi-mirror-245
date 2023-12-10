from typing import Optional

from pydantic import PrivateAttr

from classiq.interface.executor.execution_request import (
    ExecutionJobDetails,
    ResultsCollection,
)
from classiq.interface.jobs import JobStatus, JSONObject
from classiq.interface.server.routes import EXECUTION_JOBS_FULL_PATH

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import syncify_function
from classiq._internals.jobs import JobID, JobPoller
from classiq.exceptions import ClassiqAPIError


class ExecutionJob(ExecutionJobDetails):
    _result: Optional[ResultsCollection] = PrivateAttr(default=None)

    def __init__(self, details: ExecutionJobDetails) -> None:
        super().__init__(**details.dict())

    def _update_details(self, details: ExecutionJobDetails) -> None:
        for k, v in details.dict().items():
            setattr(self, k, v)

    @classmethod
    async def from_id_async(cls, id: str) -> "ExecutionJob":
        details = await ApiWrapper.call_get_execution_job_details(JobID(job_id=id))
        return cls(details)

    @classmethod
    def from_id(cls, id: str) -> "ExecutionJob":
        return syncify_function(cls.from_id_async)(id)

    @property
    def _job_id(self) -> JobID:
        return JobID(job_id=self.id)

    async def result_async(
        self, timeout_sec: Optional[float] = None
    ) -> ResultsCollection:
        await self.poll_async(timeout_sec=timeout_sec)

        if self.status == JobStatus.FAILED:
            raise ClassiqAPIError(self.error or "")
        if self.status == JobStatus.CANCELLED:
            raise ClassiqAPIError("Job has been cancelled.")

        if self._result is None:
            self._result = (
                await ApiWrapper.call_get_execution_job_result(self._job_id)
            ).results
        return self._result

    result = syncify_function(result_async)

    async def poll_async(self, timeout_sec: Optional[float] = None) -> None:
        if not self.status.is_final():
            await self._poll_job(timeout_sec=timeout_sec)

    poll = syncify_function(poll_async)

    async def _poll_job(self, timeout_sec: Optional[float] = None) -> None:
        def response_parser(json_response: JSONObject) -> Optional[bool]:
            self._update_details(ExecutionJobDetails.parse_obj(json_response))
            if self.status.is_final():
                return True
            return None

        poller = JobPoller(base_url=EXECUTION_JOBS_FULL_PATH)
        await poller.poll(
            job_id=self._job_id,
            response_parser=response_parser,
            timeout_sec=timeout_sec,
        )
