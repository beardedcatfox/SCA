# =^__^= SPY CATS


```bash
cd SCA
```
### Rename .env.example to .env

### Basic data fixtures will be in DB by auto-management command

## Docker run:
```bash
docker run -d \
  --name spycat-db \
  -e POSTGRES_DB=spycats \
  -e POSTGRES_USER=maincat \
  -e POSTGRES_PASSWORD=password12 \
  -p 5433:5432 \
  postgres:15-alpine
```
```bash
docker network create spycat-net
```
```bash
docker network connect spycat-net spycat-db
```
```bash
docker build -t spy-cat-app .
```
```bash
docker run -it \
  --name spycat-app \
  --network spycat-net \
  -p 8000:8000 \
  --env-file .env \
  spy-cat-app
```

## Postman link
https://www.postman.com/beardedcat/workspace/910593e5-46c6-43b4-8ccb-2ad17586fa70/share?collection=26460439-cb97e9cd-2dab-4d9e-b4a9-f3a65f6f4150&target=link