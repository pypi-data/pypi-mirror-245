import time
import typing

from planqk.service.auth import DEFAULT_TOKEN_ENDPOINT, PlanqkServiceAuth
from planqk.service.sdk import (
    Job,
    JobStatus,
    GetResultResponse,
    GetInterimResultsResponse,
    InputData,
    InputParams,
    HealthCheckResponse,
)
from planqk.service.sdk.client import PlanqkServiceApi
from planqk.service.sdk.resources.service_api.client import OMIT


class PlanqkServiceClient:
    def __init__(
            self,
            service_endpoint: str,
            consumer_key: str,
            consumer_secret: str,
            token_endpoint: str = DEFAULT_TOKEN_ENDPOINT
    ):
        self._service_endpoint = service_endpoint
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._token_endpoint = token_endpoint
        self._auth = PlanqkServiceAuth(consumer_key=self._consumer_key, consumer_secret=self._consumer_secret,
                                       token_endpoint=self._token_endpoint)
        self._api = PlanqkServiceApi(token=self._auth.get_token, base_url=self._service_endpoint)

    def health_check(self) -> HealthCheckResponse:
        return self._api.status_api.health_check()

    def start_execution(
            self,
            data: typing.Optional[InputData] = OMIT,
            params: typing.Optional[InputParams] = OMIT
    ) -> Job:
        return self._api.service_api.start_execution(data=data, params=params)

    def get_status(self, job_id: str) -> Job:
        return self._api.service_api.get_status(job_id)

    def get_result(self, job_id: str) -> GetResultResponse:
        self.wait_for_final_state(job_id)
        return self._api.service_api.get_result(job_id)

    def get_interim_results(self, job_id: str) -> GetInterimResultsResponse:
        return self._api.service_api.get_interim_results(job_id)

    def cancel_execution(self, job_id: str) -> Job:
        return self._api.service_api.cancel_execution(job_id)

    def wait_for_final_state(self, job_id: str, timeout: typing.Optional[float] = None, wait: float = 5) -> None:
        """
        Poll the job status until it progresses to a final state.

        Parameters:
            - job_id: str. The id of a service execution.
            - timeout: Seconds to wait for the job. If ``None``, wait indefinitely.
            - wait: Seconds between queries.

        Raises:
            Exception: If the job does not reach a final state before the specified timeout.
        """
        start_time = time.time()
        job = self.get_status(job_id)
        while self.job_has_finished(job) is False:
            elapsed_time = time.time() - start_time
            if timeout is not None and elapsed_time >= timeout:
                raise Exception(f"Timeout while waiting for job '{job_id}'.")
            time.sleep(wait)
            job = self.get_status(job_id)
        return

    @staticmethod
    def job_has_finished(job: Job) -> bool:
        return (job.status == JobStatus.SUCCEEDED
                or job.status == JobStatus.FAILED
                or job.status == JobStatus.CANCELLED)
