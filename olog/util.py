from datetime import date, datetime

_TS_FORMATS = [
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M',  # these 2 are not as originally doc'd,
    '%Y-%m-%d %H',     # but match previous pandas behavior
    '%Y-%m-%d',
    '%Y-%m',
    '%Y']


def ensure_time(time):
    if isinstance(time, datetime):
        pass
    elif isinstance(time, date):
        time = datetime.fromisoformat(time.isoformat())
    elif isinstance(time, float) or isinstance(time, int):
        time = datetime.fromtimestamp(time)
    else:
        for fmt in _TS_FORMATS:
            try:
                time = datetime.strptime(time, fmt)
                break
            except ValueError:
                pass
        else:
            raise ValueError("Your time is in wrong format.")

    return time.isoformat(sep=' ', timespec='milliseconds')


def ensure_name(name):
    if not isinstance(name, str):
        raise TypeError(f'name should be a str, {name} is not a str.')
    return name


def ensure_value(value):
    if value is None:
        return value
    if not isinstance(value, str):
        raise TypeError(f'value should be a str or None, {value} is not.')
    return value


def simplify_attr(d):
    d_cp = d.copy()
    d_cp['attributes'] = {e['name']: e['value'] for e in d['attributes']}
    return d_cp


def simplify_logbook(logbook):
    logbook_cp = logbook.copy()
    name = logbook_cp.pop('name')
    return dict({name: logbook_cp})


class UncaughtServerError(Exception):
    pass
