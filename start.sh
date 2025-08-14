#! /usr/bin/env bash

if [ "$site_env" == "prod" ]; then
  cd src
  echo "collect static"
  python manage.py collectstatic --noinput --settings=settings.prod

  echo "migrate"
  python manage.py migrate --settings=settings.prod

  echo "Create super user"
  echo "from django.contrib.auth.models import User; User.objects.create_superuser('OOOkp2A16nX8aVm3', 'N8FhT@gmail.com', 'sEaL_3&fQ7u4iqDe') if not User.objects.filter(username='OOOkp2A16nX8aVm3').count() else print('Super user already exist')" | python manage.py shell --settings=settings.prod

  echo "uwsgi"
  uwsgi --ini ../config/uwsgi.prod.ini

else
  cd src
  echo "collect static"
  python manage.py collectstatic --noinput --settings=settings.stage

  echo "migrate"
  python manage.py migrate --settings=settings.stage

  echo "Create super user"
  echo "from django.contrib.auth.models import User; User.objects.create_superuser('nppppU8rwbd5KMjYqixl', 'WHBfd@cc.com', 'NZFcTOPutIy&vkj#o') if not User.objects.filter(username='nppppU8rwbd5KMjYqixl').count() else print('Super user already exist')" | python manage.py shell --settings=settings.stage


  echo "uwsgi"
  uwsgi --ini ../config/uwsgi.stage.ini
fi

