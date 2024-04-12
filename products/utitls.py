
def validate_rating(rating):
    if rating < 0 or rating > 5:
        raise ValueError('rating must be between 0 and 5')
    return rating