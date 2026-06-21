# Fase 1

Se expecifica explícitamente Generator[YieldType, SendType, ReturnType], para que el compilador y los evaluadores que la función no es llamable convencionalmente, sino que retorna un iterador de un solo sentido.

Ademas que no se va a ejecutar todos los valores de golpe si no de uno en uno y con esto no se consume toda la memoria en una sola fraccion de tiempo.
<a href="pipeline/generator.py"> generator </a>