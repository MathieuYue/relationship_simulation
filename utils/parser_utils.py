import re

def cleaned_response(response):
    """
    Cleans the response by removing <think>...</think> tags and stripping whitespace.
    """
    if isinstance(response, str):
        # Remove <think>...</think> tags (including multiline)
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL | re.IGNORECASE)
        return response.strip()
    if hasattr(response, 'strip'):
        # If not a string but has strip, try to strip and remove <think> tags if possible
        resp_str = str(response)
        resp_str = re.sub(r'<think>.*?</think>', '', resp_str, flags=re.DOTALL | re.IGNORECASE)
        return resp_str.strip()
    return response
