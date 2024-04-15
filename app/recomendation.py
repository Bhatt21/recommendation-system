import requests

class GooglePlacesAPI:
    def __init__(self, api_key):
        self.api_key = "KEY"

    def get_nearby_places(self, location, type, radius=3000, types=None):
        """
        Get nearby places based on a given place ID and radius.

        Args:
            place_id (str): The place ID to search nearby.
            radius (int): Radius in meters to search around the place. Default is 3000 meters.
            types (list): List of place types to restrict results to. See Google Places API documentation for details.

        Returns:
            list: A list of nearby places as dictionaries.
        """
        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": location,
            "radius": radius,
            "type": type,
            "key": self.api_key,
            "rankby": "prominence"  # Use prominence for a more reliable ranking by importance
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "OK":
            # Sort the results by rating in descending order
            sorted_results = sorted(data.get("results", []), key=lambda x: x.get("rating", 0), reverse=True)
            # Limit the results to 10 places
            top_10_places = sorted_results[:10]
            print(len(top_10_places))
            # Print or do further processing with the top 10 places
            for place in top_10_places:
                print(place["name"])
        else:
            error_message = data.get("error_message", "Unknown error")
            raise Exception(f"Error: {error_message}")


# Example usage:
if __name__ == "__main__":
    api_key = "YOUR_GOOGLE_PLACES_API_KEY"
    google_places = GooglePlacesAPI(api_key)
    place_id = "ChIJbz8lP_Z544kRBFV6ZMsNgKI"
    radius = 3000  # 3 km
    nearby_places = google_places.get_nearby_places(place_id, radius=radius)
    for place in nearby_places:
        print(place["name"], place.get("vicinity", ""))
