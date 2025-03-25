def present_supplement(supplement):
    return {
        "id": supplement.id,
        "name": supplement.name,
        "description": supplement.description,
        "time": supplement.time
    }

def present_user(user):
    return {
        'id': user.id,
        'name': user.name,
        'login': user.login,
    }
