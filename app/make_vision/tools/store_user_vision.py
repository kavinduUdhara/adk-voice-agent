"""
Tool for storing a new vision statement for a user.
"""

from .db_utils import run_non_query


def store_user_vision(user_id: str, vision_text: str) -> dict:
    """
    Store a new vision statement for the specified user.

    This tool is useful when the user shares their long-term goals or aspirations,
    and the agent needs to record it for future guidance or personalization.

    Args:
        user_id (str): The unique ID of the user (Firebase UID)
        vision_text (str): The vision statement to be stored

    Returns:
        dict: Status of the operation and confirmation of saved vision text
    """
    try:
        print("Storing new user vision")
        print("User ID:", user_id)
        print("Vision Text:", vision_text)

        query = """
            INSERT INTO "Vision" ("user_user_id", "created_at", "vision_text")
            VALUES (%s, Now(), %s);
        """

        row_count = run_non_query(query, (user_id, vision_text))

        if row_count == 0:
            return {
                "status": "error",
                "message": "No rows inserted. Vision may not have been saved.",
            }

        return {
            "status": "success",
            "message": "Vision saved successfully.",
            "user": {
                "userId": user_id,
                "storedVisionText": vision_text,
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to store vision: {str(e)}",
        }
