from .models import User , Transaction , Game

def getEmail(userId):
    try:
        user = User.objects.get(id=userId)
        return user.email
    except User.DoesNotExist:
        # Handle the case where the user with the given ID doesn't exist
        return None  # or raise an exception, depending on your requirements

def getRentalPrice(userId, gameId):
    try:
        user = User.objects.get(id=userId)
        for_rent_dict = user.forRent  # Assuming forRent is a field in the User model

        # Check if the forRent field exists and contains the specified game
        if for_rent_dict and gameId in for_rent_dict:
            return for_rent_dict[gameId]
        else:
            return None  # or a default value, depending on your requirements

    except User.DoesNotExist:
        # Handle the case where the user with the given ID doesn't exist
        return None  # or raise an exception, depending on your requirements
