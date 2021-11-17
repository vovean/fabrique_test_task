## Deployment
1. Create settings/secrets.py and define there next Django settings:
   * `DATABASE_PASSWORD`
   * `SECRET_KEY`
2. Create .env file and define there next variables:
   * `POSTGRES_PASSWORD` (value must be the same as `DATABASE_PASSWORD`)
3. `docker-compose up`

## Документация
Документацию решил сделать в виде Postman коллекции с примерами запросов.  
Файл: Fabrique.postman_collection.json
