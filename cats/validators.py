import requests
from django.core.exceptions import ValidationError


def validate_breed(value):
    try:
        response = requests.get('https://api.thecatapi.com/v1/breeds', timeout=3)

        if response.status_code == 200:
            breeds_data = response.json()
            valid_breeds = [breed['name'] for breed in breeds_data]

            if value not in valid_breeds:
                raise ValidationError(
                    f"Breed '{value}' is not a valid cat breed. "
                    f"Please check TheCatAPI for valid breeds."
                )

    except requests.exceptions.Timeout:
        raise ValidationError(
            "Breed validation service timeout. Please try again later."
        )

    except requests.exceptions.ConnectionError:
        raise ValidationError(
            "Cannot connect to breed validation service. Please check your internet connection."
        )

    except requests.exceptions.RequestException as e:
        raise ValidationError(
            f"Error validating breed: {str(e)}"
        )

    except ValueError as e:
        raise ValidationError(
            "Invalid response from breed validation service. Please try again later."
        )
