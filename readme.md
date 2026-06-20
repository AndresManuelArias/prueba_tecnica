## requerimientos
```sh
pip freeze > requirements.txt
```


## Analisis

### fase 1

se utiliza Pydantic para realizar validación de tipos en tiempo de ejecución
se deja frozen = True para que sea un objeto congelado asi evita efectos secundarios 

para que en el futuro no existan migraciones complejas se utiliza un diccionario dinamico, para que se respete el principio de abierto a cambios cerrado a modificaciones