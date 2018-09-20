def type_str(types):
    return ' or '.join(t.__name__ for t in types)


def validate(name, value, *types):
    if not isinstance(value, types):
        raise TypeError('{} must be {}'.format(
            name, type_str(types)
        ))
    return value


def validate_list(name, value, *types):
    if not isinstance(value, list):
        raise TypeError('{} must be a list'.format(name))
    for v in value:
        if not isinstance(v, types):
            raise TypeError('elements of {} must be {}'.format(
                name, type_str(types)
            ))
    return value


def validate_dict(name, value, key_types, value_types):
    if not isinstance(value, dict):
        raise TypeError('{} must be a dict'.format(name))
    for k, v in value.items():
        if not isinstance(k, key_types):
            raise TypeError('keys of {} must be {}'.format(
                name, type_str(key_types)
            ))
        if not isinstance(v, value_types):
            raise TypeError('values of {} must be {}'.format(
                name, type_str(value_types)
            ))
    return value


def validate_enum(name, value, enum_type):
    value = validate(name, value, str, enum_type)
    if isinstance(value, str):
        return enum_type[value.upper()]
    return value
