from .model import TensorContraction


def parallelization(*args):
    if len(args) == 0:
        raise ValueError('At least one argument is required')

    result = args[0]
    for arg in args[1:]:
        result = result | arg
    return result


def concatenation(*args: TensorContraction) -> TensorContraction:
    if len(args) == 0:
        raise ValueError('At least one argument is required')

    result = args[0]
    for arg in args[1:]:
        result = result - arg
    return result
