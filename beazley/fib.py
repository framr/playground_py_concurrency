
def fib(n):
    """
    exponential implementation simply for demo purposes, it should work slooowly!
    """
    if n <= 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
     
