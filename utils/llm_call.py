import os
import json

# Attempt to import litellm but allow the module to import even if the
# library is not installed. We'll raise a clear error later when the
# function is actually used. This keeps module import-time failures
# from blocking static analysis or unit tests that don't exercise LLM.
try:
    from litellm import completion
except Exception:
    completion = None


LLM_MODEL = os.environ.get("LLM_MODEL", "mistral/mistral-large-latest")


def get_response_from_llm(prompt):
    """
    Calls the LLM and returns the response.

    Args:
        prompt (str): The string to prompt the LLM with.

    Returns:
        str: The response from the LLM.
    """
    if completion is None:
        raise ModuleNotFoundError(
            "The 'litellm' package is not installed. Install requirements with:\n"
            "    pip install -r requirements.txt\n"
            "or install 'litellm' directly to enable LLM functionality."
        )

    response = completion(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def parse_json_response(response):
    # Parse the JSON response
    try:
        response = response.strip("```json")
        response = response.strip("```")
        return json.loads(response)
    except json.JSONDecodeError:
        return None
