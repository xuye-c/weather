class GoogleMapsAPI:
    """
    Google Maps API service for generating map links
    """
    
    @staticmethod
    def get_map_link(city):
        """
        Generate Google Maps link for a city
        
        Args:
            city (str): Name of the city
        
        Returns:
            dict: {
                "city": str,
                "map_link": str,
                "status": str
            }
        """
        if not city or not city.strip():
            return {
                "status": "error",
                "message": "City cannot be empty"
            }
        
        city = city.strip()
        
        # URL encode the city name for safe URL
        import urllib.parse
        encoded_city = urllib.parse.quote(city)
        
        # Generate Google Maps search link
        map_link = f"https://www.google.com/maps?q={encoded_city}"
        
        return {
            "status": "success",
            "city": city,
            "map_link": map_link
        }