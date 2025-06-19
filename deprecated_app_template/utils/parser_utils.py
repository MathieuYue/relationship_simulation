def cleaned_response(response):
    if isinstance(response, str):
        return response.strip()
    if hasattr(response, 'strip'):
        return response.strip()
    return response
