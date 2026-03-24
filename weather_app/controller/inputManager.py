from datetime import datetime
from db.writer import Writer


class InputManager:
    """
    Handles user input validation and coordinates DB write operations.
    """

    @staticmethod
    def validate(city, date, temperature):
        """
        Validate user input.

        Raises:
            ValueError: if input is invalid
        """
        if not city:
            raise ValueError("City cannot be empty")

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format")

        try:
            float(temperature)
        except ValueError:
            raise ValueError("Temperature must be a number")

    @staticmethod
    def insert(city, date, temperature):
        """
        Validate and insert a new record into DB.

        Returns:
            dict: result message
        """
        # 1. validate
        InputManager.validate(city, date, temperature)

        # 2. 写数据库
        try:
            Writer.insert(city, date, float(temperature))
            return {
                "status": "success",
                "message": "Insert successful"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }