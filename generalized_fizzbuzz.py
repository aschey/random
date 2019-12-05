numbers = (i for i in range(1, 101))
transforms = [
    {'func': lambda i: i % 3 == 0, 'val': 'Fizz'},
    {'func': lambda i: i % 5 == 0, 'val': 'Buzz'},
    {'func': lambda i: str(i)[0] == '5', 'val': 'Baz'}
]

def apply_transform(transform, num):
    return transform['val'] if transform['func'](num) else ''

def apply_transforms(num):
    return ''.join((apply_transform(transform, num) for transform in transforms)) or num

def apply_if_true(val, apply):
    return val if apply == 0 else ""

def apply_transforms2(num):
    return f'{apply_if_true("Fizz", num % 3)}{apply_if_true("Buzz", num % 5)}' or str(num)

vals = map(apply_transforms2, numbers)
print(list(vals))