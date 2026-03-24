from datetime import datetime, timedelta
from db.writer import Writer
from db.reader import Reader


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
        if not city or not city.strip():
            raise ValueError("City cannot be empty")
        city = city.strip()
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format")

        try:
            temp = float(temperature)
        except ValueError:
            raise ValueError("Temperature must be a number")

        if temp < -225 or temp > 60:
            raise ValueError("Temperature out of realistic range (-225 ~ 60°C)")
        return {
            "city": city,
            "date": dt.strftime("%Y-%m-%d"),
            "temperature": temp
        }
    @staticmethod
    def search(city, start_date, end_date):
        """
        Handle search logic.

        Returns:
            dict:
            {
                "status": "success",
                "data": [ {city, date, temperature}, ... ]
            }
        """

        if not city or not city.strip():
            return {"status": "error", "message": "City cannot be empty"}

        city = city.strip()

        # 情况 1：都没填 → 查全部
        if not start_date and not end_date:
            rows = Reader.get_by_city(city)

        # 情况 2：只填一个 → 查单天
        elif start_date and not end_date:
            rows = Reader.get_by_city_and_range(city, start_date, start_date)

        elif not start_date and end_date:
            rows = Reader.get_by_city_and_range(city, end_date, end_date)

        # 情况 3：两个都填 → 查范围
        else:
            rows = Reader.get_by_city_and_range(city, start_date, end_date)

        # 转成前端友好格式
        data = [
            {
                "city": r[0],
                "date": r[1],
                "temperature": r[2]
            }
            for r in rows
        ]

        return {
            "status": "success",
            "data": data
        }
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