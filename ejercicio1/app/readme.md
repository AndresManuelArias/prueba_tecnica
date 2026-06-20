## Analisis

### fase 1

se utiliza Pydantic para realizar validación de tipos en tiempo de ejecución
se deja frozen = True para que sea un objeto congelado asi evita efectos secundarios 

para que en el futuro no existan migraciones complejas se utiliza un diccionario dinamico, para que se respete el principio de abierto a cambios cerrado a modificaciones
<a href="core/models.py"> model </a>

### fase 2
Se crea una clase abstracta para el envio de notificaciones, se trabaja con el principio de sustitución de liskov, esto con el fin que en un futuro se pueda agregar cualquier nuevo canal
para el manejo de la falla se utilia una excepción de ConnectionError, para que se muestre el error tecnico
<a href="core/channels.py"> channels </a>

### fase 3
Al tratar de cumplir con los principios SOLID, se crea una clase abstracta para el el filtro y objetos que definen estas reglas.
El manejo del tiempo se hace utilizando la hora universal y no la hora del servidor

<a href="core/filters.py"> filter </a>


### fase 4

se maneja la inyeccion de dependencias, agregando una lista de abstracciones, donde los modulos de alto nivel depende de los de bajo nivel si no que estos dependen de abstracciones

se aplica un corto circuito para el no envio de la notificaciones, si en algun momento el filtro determina que el mensaje no se debe enviar entonces se interumpe el flujo

<a href="core/services.py"> services </a>