"""
Tool for updating a user's list of interests.
"""

from .db_utils import run_non_query


def update_user_interests(user_id: str, new_interests: list[str]) -> dict:
    """
    Update the list of interests for a specific user.

    This tool is useful when the agent helps the user express their hobbies or preferences,
    and those need to be saved to their user profile.

    Args:
        user_id (str): The unique ID of the user (Firebase UID)
        new_interests (list[str]): A list of interests or hobbies (e.g., ["reading", "coding", "swimming"])

    Returns:
        dict: Result of the update operation, including status and updated interests.
    """
    try:
        print("Updating user interests")
        print("User ID:", user_id)
        print("New Interests:", new_interests)

        query = """
            UPDATE "User"
            SET "interests" = %s
            WHERE "user_id" = %s;
        """

        row_count = run_non_query(query, (new_interests, user_id))

        if row_count == 0:
            return {
                "status": "error",
                "message": f"No user found with ID: {user_id}. Interests not updated.",
            }

        return {
            "status": "success",
            "message": "User interests updated successfully.",
            "user": {
                "userId": user_id,
                "updatedInterests": new_interests,
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to update user interests: {str(e)}",
        }
