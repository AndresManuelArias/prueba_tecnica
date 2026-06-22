## paso 1

Se crea el objeto cache el cual va contender un map para consultar y guardar los datos por llaves, se agrega un tiempo de creacion y un tamaño maximo para eliminar datos y con esto no sobre cargar la memoria.

Para generar una estructura reentrante y Segura (try...finally) se maneja el uso del bloque finally para hacer this.inFlightPromises.delete(key) ayuda a que la aplicacion no sufra de promesas congeladas perpetuas cuando el fetcher de la base de datos llega a fallar con un timeout o error de red.

Para un aislamiento de contexto asíncrono fetchPromise se autoejecuta inmediatamente como una función IIFE asíncrona. Esto permite guardar la referencia de la Promesa pura en el mapa antes de que los hilos lógicos de JavaScript cedan el control en el await fetcher().

<a href="ejercicio3_cache/src/cache.js"> cache </a>

