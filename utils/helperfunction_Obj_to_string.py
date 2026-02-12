def helperfunction_Object_to_string(user):
    return{
        "id":str(user['_id']),
        "username":user['username'],
        "email":user['email'],
        "phone":user['phone'],
        "created_at":user['created_at']
    }