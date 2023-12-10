from convergence.dto.service_status import ServiceEndpointDTO


def matches_any(internal_endpoint_urls, path):
    return path in internal_endpoint_urls


def load_service_urls(service, internal_endpoint_urls):
    internal_endpoints = []
    public_endpoints = []
    for route in service.app.routes:
        if route.include_in_schema:
            endpoint_list = internal_endpoints if matches_any(internal_endpoint_urls, route.path) else public_endpoints
            ep = ServiceEndpointDTO()
            ep.url = route.path
            ep.methods = route.methods

            endpoint_list.append(ep)

    return internal_endpoints, public_endpoints
