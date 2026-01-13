# =^__^= SPY CATS


```bash
cd SCA
```
## !!! Rename .env.example to .env !!!

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

## Postman collection link
https://www.postman.com/beardedcat/workspace/910593e5-46c6-43b4-8ccb-2ad17586fa70/share?collection=26460439-cb97e9cd-2dab-4d9e-b4a9-f3a65f6f4150&target=link

##  Quick API Docs

- **GET** all cats / **POST** create new cat
> http://localhost:8000/api/cats/

```JSON
{
    "name": "Mathilda",
    "years_of_experience": 3,
    "breed": "Abyssinian",
    "salary": 1500.00
}
```

- **GET** one cat / **PUT** change cat’s data (for Example, salary) / **DELETE** cat
> http://localhost:8000/api/cats/1/

```JSON
{
    "name": "Mathilda",
    "years_of_experience": 3,
    "breed": "Abyssinian",
    "salary": 180.00
}
```
- **GET** all missions / **POST** create mission with targets
> http://localhost:8000/api/missions/
```JSON
{
    "cat": null,
    "targets": [
        {
            "name": "Agent X",
            "country": "Iran",
            "notes": "Suspected nuclear scientist"
        },
        {
            "name": "Dr. Evil",
            "country": "Germany",
            "notes": "Bio-weapons research"
        }
    ]
}
```
- **GET** one mission / 
> http://localhost:8000/api/missions/1/

- **POST** assign cat on mission 
> http://localhost:8000/api/missions/1/assign_cat/

```JSON
{
    "cat_id": 1
}
```
- **DELETE** mission (if no cat on it)
> http://localhost:8000/api/missions/2/

- **PUT** changing target data (by target id)
> http://localhost:8000/api/targets/1/
```JSON
{
    "name": "Agent X",
    "country": "Iraq",
    "notes": "Confirmed nuclear scientist. Meetings every Tuesday.",
    "is_completed": false
}
```
- **POST** Target completing 
> http://localhost:8000/api/targets/1/complete/

