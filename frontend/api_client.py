import requests
from django.conf import settings

def api_request(method, endpoint, data=None, params=None, token=None, files=None):
    """
    A helper function to make API requests to a backend.
    
    :param method: HTTP method ('get', 'post', 'put', 'delete')
    :param endpoint: API endpoint to call (e.g., 'clients/')
    :param data: Data to send with the request (for 'POST' and 'PUT' requests)
    :param params: URL parameters (for 'GET' requests)
    :param token: Authorization token for authenticated requests
    :param files: Files to send with the request (optional)
    :return: Response object if successful, None if there's an error
    """
    url = settings.API_BASE_URL + endpoint

    # Prepare headers
    headers = {}
    if token:
        headers['Authorization'] = f'Token {token}'

    try:
        # Make the HTTP request based on the specified method
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            files=files
        )

        # Check if the response status code is in the 200 range (success)
        response.raise_for_status()  # This will raise an error for 4xx/5xx responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None
