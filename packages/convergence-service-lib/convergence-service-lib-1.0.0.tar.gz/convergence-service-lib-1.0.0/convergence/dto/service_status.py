from typing import List, Dict
from convergence.dto.base_dto import ApiResponseBody


class ServiceEndpointDTO:
    def __init__(self):
        self.url = ''
        self.methods: List[str] = []


class ServiceStatusDTO(ApiResponseBody):
    def __init__(self):
        self.service_name = ''
        self.version_hash = ''
        self.version = ''
        self.status = ''
        self.internal_endpoints: List[ServiceEndpointDTO] = []
        self.public_endpoints: List[ServiceEndpointDTO] = []
        self.extra: Dict[str, str] = {}

    def get_response_body_type(self) -> str:
        return 'service_status'
