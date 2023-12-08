from typing import List, Tuple
from karrio.core.utils import (
    DP,
    request as http,
    Serializable,
    Deserializable,
    exec_async,
)
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.sendle.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(
        self, request: Serializable
    ) -> Deserializable[List[Tuple[str, dict]]]:
        def _get_tracking(ref: str):
            response = http(
                url=f"{self.settings.server_url}/api/tracking/{ref}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
            )
            return ref, response

        responses: List[Tuple[str, str]] = exec_async(
            _get_tracking, request.serialize()
        )
        return Deserializable(
            responses,
            lambda res: [
                (num, DP.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )
