## requerimientos
```sh
pip freeze > requirements.txt
```


## Analisis

### fase 1

se utiliza Pydantic para realizar validación de tipos en tiempo de ejecución
se deja frozen = True para que sea un objeto congelado asi evita efectos secundarios 

para que en el futuro no existan migraciones complejas se utiliza un diccionario dinamico, para que se respete el principio de abierto a cambios cerrado a modificaciones

### fase 2
Se crea una clase abstracta para el envio de notificaciones, se trabaja con el principio de sustitución de liskov, esto con el fin que en un futuro se pueda agregar cualquier nuevo canal
para el manejo de la falla se utilia una excepción de ConnectionError, para que se muestre el error tecnico

### fase 3
Al tratar de cumplir con los principios SOLID, se crea una clase abstracta para el el filtro y objetos que definen estas reglas.
El manejo del tiempo se hace utilizando la hora universal y no la hora del servidor