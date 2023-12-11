import random


def lambdafy(source_code):
    """
    Converts the given source code into a lambda function.

    Args:
        source_code (str): The source code to convert.

    Returns:
        str: The converted source code.
    """
    magic_number = random.randint(31456, 999999)
    chr_code = [ord(c) + magic_number for c in source_code]
    lambda_code = f"(lambda o, oo, ooo: o.join([oo(oooo-int(b'{hex(magic_number)}',0)) for oooo in ooo]))('', chr, {chr_code})"
    return f"exec({lambda_code})"
