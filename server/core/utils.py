from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.translation import gettext as _


def timedelta_to_time(delta):
    return (datetime.min + delta).time()


def humanize_time(dt):
    day_description = ""
    now_date = timezone.now().date()
    if dt.date() == now_date:
        day_description = _("сегодня")
    elif dt.date() == now_date - timedelta(days=1):
        day_description = _("вчера")
    elif dt.date() == now_date - timedelta(days=2):
        day_description = _("позавчера")
    else:
        day_description = _("%d %b %Y года")
    return dt.strftime(f"{day_description} в %-H часов %-M минут")
