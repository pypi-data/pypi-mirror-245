import asyncio
import traceback

import aiohttp
import async_traffic_pulse as atp
from tqdm import tqdm
from tqdm.asyncio import tqdm as atqdm


async def simulate_traffic(
    url,
    method,
    payload_schema,
    num_requests,
    timeout,
    progress_bar=False,
):
    """
    The function `simulate_traffic` is an asynchronous function that sends multiple HTTP requests to a
    specified URL using a specified method and payload schema, with a specified number of requests and
    timeout.
    
    :param url: The URL of the API endpoint that you want to send requests to
    :param method: The HTTP method to use for the requests (e.g., GET, POST, PUT, DELETE)
    :param payload_schema: The payload_schema parameter is a JSON schema that defines the structure and
    data types of the payload that will be sent in the requests. It is used to validate the payload
    before sending the requests
    :param num_requests: The number of requests to be sent to the specified URL
    :param timeout: The timeout parameter specifies the maximum amount of time (in seconds) that the
    function will wait for a response from the server before raising a timeout error
    :param progress_bar: A boolean value indicating whether to display a progress bar during the
    simulation. If set to True, a progress bar will be shown to track the progress of the simulation. If
    set to False, no progress bar will be displayed, defaults to False (optional)
    """
    
    if progress_bar:
        pbar = atqdm(total=num_requests, desc=f"Simulating {num_requests} {method} requests", bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]")
    else:
        pbar = None
        
    tasks = []
    for i in range(num_requests):
        if method == "GET":
            rand_payload = None
        else:
            rand_payload = atp.random_payload_generator(payload_schema)
        task = asyncio.create_task(
            make_async_request(
                url=url,
                method=method,
                payload=rand_payload,
                timeout=timeout,
                progress_bar=pbar,
            )
        )
        tasks.append(task)
        
    await asyncio.gather(*tasks)
    if progress_bar:
        pbar.close()
        
async def make_async_request(url, method, payload, timeout, progress_bar=None):
    """
    The `make_async_request` function is an asynchronous function that makes HTTP requests using the
    aiohttp library and returns the JSON response.
    
    :param url: The `url` parameter is the URL of the API endpoint you want to make a request to. It
    should be a string
    :param method: The `method` parameter specifies the HTTP method to be used for the request, such as
    "GET", "POST", "PUT", or "PATCH"
    :param payload: The `payload` parameter is a dictionary that contains the data to be sent in the
    request body. It is used for methods like POST, PUT, and PATCH where data needs to be sent to the
    server. The payload dictionary will be converted to JSON format and sent in the request body
    :param timeout: The `timeout` parameter is the maximum amount of time (in seconds) that the request
    is allowed to take before it times out. If the request takes longer than the specified timeout, an
    `asyncio.exceptions.TimeoutError` will be raised
    :param progress_bar: The `progress_bar` parameter is an optional argument that allows you to pass a
    progress bar object to track the progress of the request. It can be any object that has an
    `update()` method. If a progress bar object is provided, it will be updated each time a request is
    made
    :return: the result of the asynchronous request as a JSON object. If an exception occurs during the
    request, it returns None.
    """
    try:
        async with aiohttp.ClientSession() as session:
            if method in ["POST", "PUT", "PATCH"]:
                request_kwargs = {"json": payload}
            else:
                request_kwargs = {}
            async with session.request(method, url, timeout=timeout, **request_kwargs) as response:
                result = await response.json()
                if progress_bar is not None:
                    progress_bar.update()
                return result
            
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(f"Exception: {e}")
        print(traceback.format_exc())
        return None
    except asyncio.exceptions.TimeoutError as e:
        print(f"Exception: {e}")
        print(traceback.format_exc())
        return None
    except aiohttp.client_exceptions.ClientResponseError as e:
        print(f"Exception: {e}")
        print(traceback.format_exc())
        return None
    except Exception as e:
        print(f"Exception: {e}")
        print(traceback.format_exc())
        return None