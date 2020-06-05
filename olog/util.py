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


def check_name(name):
    if not isinstance(name, str):
        raise TypeError(f'name should be a str, {name} is not a str.')
    return name


def simplify_attr(d):
    d['attributes'] = {e['name']: e['value'] for e in d['attributes']}
    return d


class UncaughtServerError(Exception):
    pass
