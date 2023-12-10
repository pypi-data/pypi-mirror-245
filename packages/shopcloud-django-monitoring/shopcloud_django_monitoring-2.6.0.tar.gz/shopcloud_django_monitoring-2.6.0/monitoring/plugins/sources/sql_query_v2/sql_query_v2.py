from typing import Optional, Tuple

from django.db import connection, connections
from shopcloud_django_instrumenting import tracing

from monitoring import models


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class Plugin:
    NAME = "SQL_QUERY_V2"

    def proceed(self, span: tracing.Span, metric: models.Metric, **kwargs) -> Tuple[bool, Optional[int]]:
        total = 0
        fn_cursor = connection.cursor
        if metric.source.meta_db in connections:
            fn_cursor = connections[metric.source.meta_db].cursor
        with fn_cursor() as cursor:
            cursor.execute(metric.query)
            results = dictfetchall(cursor)
            if len(results) <= 0:
                total = 0
            else:
                total = results[0].get('total', 0)

        return True, int(total)
