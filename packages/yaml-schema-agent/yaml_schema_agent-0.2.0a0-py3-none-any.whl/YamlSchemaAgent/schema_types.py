def add_str():
    return dict(type="string")


def add_int():
    return dict(type="integer")


def add_list():
    return dict(type="array")


def add_nonetype():
    return dict(type='null')


def add_number():
    return dict(type='number')


def add_float():
    return add_number()


def add_bool():
    return dict(type='boolean')
