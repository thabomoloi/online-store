from typing import Any, Dict


def create_response(
    code: int, description: str, message, data: Any = None
) -> Dict[str, Any]:
    response = {"code": code, "description": description, "message": message}
    if data is not None:
        response["data"] = data
    return response
