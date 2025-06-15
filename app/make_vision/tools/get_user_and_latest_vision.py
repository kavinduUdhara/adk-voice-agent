"""
Tool for retrieving user information along with their latest vision data.
"""

from .db_utils import run_query_single


def get_user_and_latest_vision(user_id: str) -> dict:
    """
    Get the user's profile information and their most recent vision statement.

    This tool is useful when the agent needs to understand the user's interests, goals,
    or personalize the conversation based on their past input.

    Args:
        user_id (str): The unique ID of the user (Firebase UID)

    Returns:
        dict: Contains user's display name, list of interests, and latest vision text.
              If not found, includes an appropriate error message.
    """
    try:
        print("Fetching user and vision data")
        print("User ID:", user_id)

        query = """
            SELECT
              "User"."display_name",
              "User"."interests",
              "Vision"."vision_text"
            FROM
              "User"
            LEFT JOIN
              "Vision"
            ON
              "User"."user_id" = "Vision"."user_user_id"
            WHERE
              "User"."user_id" = %s
            ORDER BY
              "Vision"."created_at" DESC
            LIMIT 1;
        """
        print(query)
        result = run_query_single(query, (user_id,))
        print(f"result:  {result}")
        if not result:
            return {
                "status": "error",
                "message": f"No user or vision data found for user ID: {user_id}",
                "user": None,
            }

        display_name, interests, vision_text = result

        # Fallback messages
        interests_value = interests if interests else ["No interests yet."]
        vision_value = vision_text if vision_text else "User hasn't made a vision yet."

        return {
            "status": "success",
            "message": "User and vision data retrieved successfully.",
            "user": {
                "userId": user_id,
                "displayName": display_name,
                "interests": interests_value,
                "latestVisionText": vision_value,
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving user and vision data: {str(e)}",
            "user": None,
        }
