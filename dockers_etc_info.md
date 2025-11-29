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

### CERTBOT (SSL Cert)

'''https://phoenixnap.com/kb/letsencrypt-docker''' let\'s encrypt SSL

(docker compose <-> docker-compose)
```
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d [domain-name]
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d` [domain-name]
```
 =>
````
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/my-samples.ru/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/my-samples.ru/privkey.pem
This certificate expires on 2026-01-23.
````
(certbot container removed, but /etc/letsencrypt mapped to /certbot/conf, see docker-compose.yaml)

SO getting certificates first time => add 443 to nginx.conf =>
```
docker-compose restart
OR
docker-compose exec booking_nginx nginx -s reload
```
In three months:
````
docker-compose run --rm certbot renew
````


### GITLAB RUNNER
```
docker run -d --name gitlab-runner --restart=unless-stopped  \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine
```
Register:
get TOKEN-FROM-GITLAB: (Project, Settings -> CI/CD -> Runners -> Create project runner)

```
  docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register \
      --url https://gitlab.com \
      --token TOKEN-FROM-GITLAB
```
DIALOG: executor: docker, image: docker:dind

To enable starting real docker containers on server (not only inside gitlab-runner container):
nano /srv/gitlab-runner/config/config.toml
Replace volumes = ["/cache"] -> 
```
volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
```

#### FOR .env files:
Gitlab Project, Settings -> CI/CD -> Variables -> Type (variable >> file) KEY=name, VALUE=file content

