def fib(n):
    """
    Compute the nth Fibonacci number.

    Args:
        n (int): Ordinal.

    Returns:
        Fibonacci number.
    """
    assert n > 0
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a
