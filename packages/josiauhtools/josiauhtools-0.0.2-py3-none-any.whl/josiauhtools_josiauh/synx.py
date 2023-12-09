def then(first, thenDo):
    """
    Works like making a promise in javascript.
    The first paramater is what to do first. 
    This is turned into the second parameter as parameters for the function.
    """
    params = first()
    print(params)
    thenDo(params)

