def determinant(value: str) -> str:
    intersection = {chr(symbol) for symbol in range(97, 123)}.intersection(set(list(value)))
    return 'email' if intersection != set() else 'phone'
