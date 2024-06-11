
def validate_rating(rating):
    if rating < 0 or rating > 5:
        raise ValueError('rating must be 5 - 0')
    return rating