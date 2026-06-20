## requerimientos
```sh
pip freeze > requirements.txt
```


## correr ejericio 1
```sh
#crear simulacion de email
docker run -d --name mailpit -p 1025:1025 -p 8025:8025 axllent/mailpit
cd ejercicio1
uvicorn app.main:app --reload


```
# abrir el navegador 

## probar endpoint
http://127.0.0.1:8000/docs

## ver envio de email
http://localhost:8025


## agregar el canal de whaTSAPP

```sh
EXPORT META_WHATSAPP_TOKEN="tu_permanent_access_token_aqui"
EXPORT META_PHONE_NUMBER_ID="tu_phone_number_id_aqui"
EXPORT META_VERSION_API="v20.0"
``
