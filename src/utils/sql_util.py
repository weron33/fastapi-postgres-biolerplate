from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import class_mapper


def kwargs_to_sqlalchemy(table, **kwargs):
    gt = and_(*[getattr(table, k) > v for k, v in kwargs.pop('gt').items()]) if 'gt' in kwargs else None
    lt = and_(*[getattr(table, k) < v for k, v in kwargs.pop('lt').items()]) if 'lt' in kwargs else None
    ge = and_(*[getattr(table, k) >= v for k, v in kwargs.pop('ge').items()]) if 'ge' in kwargs else None
    le = and_(*[getattr(table, k) <= v for k, v in kwargs.pop('le').items()]) if 'le' in kwargs else None
    eq = and_(*[getattr(table, k) == v for k, v in kwargs.items()])
    query = [q for q in [gt, lt, ge, le, eq] if q is not None]
    return and_(*query)


def dictify(model_instance):
    mapper = class_mapper(model_instance.__class__)
    columns = [column.key for column in mapper.columns]
    model_dict = {}
    for column in columns:
        value = getattr(model_instance, column)
        if isinstance(value, datetime):
            value = value.isoformat()  # Convert datetime to string representation
        model_dict[column] = value
    return model_dict
