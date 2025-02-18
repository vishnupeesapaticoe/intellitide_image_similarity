import time
from starlette.middleware.base import BaseHTTPMiddleware

class add_process_time_header(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ''' This will add processing time on every request '''
        start_timestamp = time.time()
        request.state.timestamp = start_timestamp
        response = await call_next(request)
        process_time = time.time() - start_timestamp
        response.headers["X-Process-Time"] = str(process_time)
        print('add_process_time_header middleware')
        print(f'Took {process_time} to process')
        return response
