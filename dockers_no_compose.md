docker network create bookNetwork

docker build -t booking_image .

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=booking \
    --network=bookNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

``` docker volume rm pg-booking-data if user data was changed! ```

docker run --name booking_cache \
    -p 7379:6379 \
    --network=bookNetwork \
    -d redis:7.4

docker run --name booking_back \
    -p 7777:8000 \
    --network=bookNetwork \
    booking_image


docker run --name booking_celery_worker \
    --network=bookNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat \
    --network=bookNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance beat -l INFO

docker run --name booking_nginx \
    --network=bookNetwork \
    --restart unless-stopped \
    -p 80:80 \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    nginx

```
docker stop $(docker ps -q)
docker stop $(docker ps -aqf name='^booking')
docker start $(docker ps -aqf name='^booking')

docker rm $(docker ps -aqf name='^booking')
OR
docker rm -f $(docker ps -q)
```
