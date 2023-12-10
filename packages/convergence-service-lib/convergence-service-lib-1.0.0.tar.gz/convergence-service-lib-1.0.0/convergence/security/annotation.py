from convergence.convergence_service import ConvergenceService


def convergence_endpoint(router, url, method='GET', authorization=None, is_public_endpoint=False):
    if not is_public_endpoint and authorization is None:
        raise ValueError(f'An endpoint must either have authorization rule or be a public endpoint ({method}: {url})')
    ConvergenceService.register_endpoint_info(url, method, authorization, is_public_endpoint)

    def wrapper(func):
        if method.upper() == 'GET':
            router.get(url)(func)
        elif method.upper() == 'POST':
            router.post(url)(func)
        elif method.upper() == 'PUT':
            router.put(url)(func)
        elif method.upper() == 'PATCH':
            router.patch(url)(func)
        elif method.upper() == 'DELETE':
            router.delete(url)(func)

        return func

    return wrapper
