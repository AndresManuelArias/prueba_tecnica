# Fase 1

Se expecifica explícitamente Generator[YieldType, SendType, ReturnType], para que el compilador y los evaluadores que la función no es llamable convencionalmente, sino que retorna un iterador de un solo sentido.

Ademas que no se va a ejecutar todos los valores de golpe si no de uno en uno y con esto no se consume toda la memoria en una sola fraccion de tiempo.
<a href="pipeline/generator.py"> generator </a>

# Fase 2

con window_aggregation_stage se crean bloques de 5 minutos definidos por el timestamp, de esta manera solo se procesa la informacion por grupos de tiempo.
<a href="pipeline/stages.py"> generator </a>


# Fase 3

Se agrega funcion reduce esto con el objetivo, de esta forma se puedan agregar nuevos flujos




