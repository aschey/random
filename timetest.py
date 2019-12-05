import sys

from dateparser import parse as dp_parse
from datetime import datetime, timedelta
from dateutil.parser import parse as du_parse
from timefhuman import timefhuman
from daterangeparser import parse as dr_parse

NOW = datetime.now()
DP_SETTINGS = {
    'RELATIVE_BASE': NOW,
}
EXPECTED_DATETIME = datetime(year=2016, month=9, day=1)
DATASET = (
    # (query, expected)
    ('2016/09/01', EXPECTED_DATETIME),
    ('2016-09-01', EXPECTED_DATETIME),
    ('09/01/2016', EXPECTED_DATETIME),
    ('09-01-2016', EXPECTED_DATETIME),
    ('09012016', EXPECTED_DATETIME),
    ('09/01/2016 15:20', EXPECTED_DATETIME.replace(hour=15, minute=20)),
    ('09/01/2016 at 15h20', EXPECTED_DATETIME.replace(hour=15, minute=20)),
    ('09/01/2016 3:20 PM', EXPECTED_DATETIME.replace(hour=15, minute=20)),
    ('Sept 01 2016 3:20 PM', EXPECTED_DATETIME.replace(hour=15, minute=20)),
    ('Sept 01, 2016 at 3:20 PM', EXPECTED_DATETIME.replace(hour=15, minute=20)),
    ('15 min ago', NOW - timedelta(minutes=15)),
    ('two hours ago', NOW - timedelta(hours=2)),
    ('a day ago', NOW - timedelta(days=1)),
    ('tuesday', (
        NOW.replace(hour=0, minute=0, second=0, microsecond=0) - \
        timedelta(days=(NOW.weekday() - 1)))),
    ('monday at noon', (
        NOW.replace(hour=12, minute=0, second=0, microsecond=0) - \
        timedelta(days=NOW.weekday()))),
)


def is_equal(time1, time2):
    return time1 == time2


def parse(parser, query, expected, **options):
    try:
        result = parser(query, **options)
    except:
        return 0
    if result and is_equal(result, expected):
        return 1
    return 0


def bench(dataset):
    du_scores = []
    dp_scores = []
    tf_scores = []
    dr_scores = []
    template = '| {:25} | {:>10} | {:>10} | {:>10} | {:>10} |'
    separator = template.format('-' * 25, '-' * 10, '-' * 10, '-' * 10, '-' * 10)

    print(template.format('query', 'dateutil', 'dateparser', 'timefhuman', 'daterangeparser'))
    print(separator)

    for query, expected in dataset:
        du_score = parse(du_parse, query, expected, fuzzy=True)
        dp_score = parse(dp_parse, query, expected, settings=DP_SETTINGS)
        tf_score = parse(timefhuman, query, expected)
        dr_score = parse(dr_parse, query, expected)
        du_scores.append(du_score)
        dp_scores.append(dp_score)
        tf_scores.append(tf_score)
        dr_scores.append(dr_score)

        print(template.format(query, du_score, dp_score, tf_score, dr_score))

    print(separator)
    print(template.format(
        'total ({})'.format(len(du_scores)),
        sum(du_scores),
        sum(dp_scores),
        sum(tf_scores),
        sum(dr_scores))
    )


def main():
    bench(DATASET)
    return 0

main()