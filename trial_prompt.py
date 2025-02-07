import requests

LM_STUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"

def test_lm_studio():
    """
    Test if LM Studio's local API is working correctly.
    """
    request_payload = {
        "model": "llama-3.2-1b-instruct",  # Match the model ID in LM Studio
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello."}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, json=request_payload)
        response.raise_for_status()
        print("Response from LM Studio:", response.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_lm_studio()
