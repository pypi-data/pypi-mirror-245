# shopcloud-django-monitoring

Monitoring App

## Quickstart

```
pip3 istall shopcloud-django-monitoring
```

1. Add "monitoring" to your INSTALLED_APPS setting like this::

```py
INSTALLED_APPS = [
    ...
    'monitoring',
]
```

```py
PLUGINS = {
    'MONITORING_SOURCES': {
        'INSTALLED': [
            'SQL_QUERY_V1',
            'SQL_QUERY_V2',
            'SQL_SAGE_GATEWAY_V1',
            'NOT_SUCCESS_V1',
        ]
    }
}
```

```py


APP_TITLE = os.environ.get("APP_TITLE", "Foobar-Services")

```

2. Include the polls URLconf in your project urls.py like this::

```
path('monitoring/', include('monitoring.urls')),
```

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a metric (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/monitoring/ to participate in the Monitoring Metrics.

6. Queue `monitoring-metrics-proceed` anlegen.

## Release

```sh
$ rm -rf build dist
$ pip3 install wheel twine
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/*
```
