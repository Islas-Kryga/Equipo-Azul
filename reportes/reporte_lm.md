# Reporte de uso de modelo de lenguaje

Durante el desarrollo utilizamos un modelo de lenguaje únicamente como apoyo
para revisar la documentación y entender algunos problemas del código. El
equipo tomó las decisiones finales, revisó los cambios y comprobó el
funcionamiento del programa.

## Prompt 1: apoyo para revisar el código

**Prompt resumido:** Revisar el código del análisis geométrico y proponer una
forma de mejorar la detección de círculos en las imágenes de prueba.

**¿Por qué lo usamos?**  
Porque algunas figuras circulares podían confundirse con otra categoría y
queríamos revisar si el criterio utilizado era demasiado estricto.

**¿Qué aceptamos?**  
La idea de revisar la variación de las distancias entre los píxeles del borde y
el centro de la figura, además de comprobar el resultado con pruebas.

**¿Qué corregimos o descartamos?**  
El equipo revisó la propuesta junto con el código existente y ajustó el límite
de variación de `0.02` a `0.04`. No se tomó la respuesta del modelo como una
solución automática: se probó el cambio y se conservaron únicamente los
ajustes que funcionaron con el banco de imágenes.

## Prompt 2: apoyo para revisar los requisitos

**Prompt resumido:** Revisar el PDF del proyecto y ayudar a organizar los
apartados del reporte técnico.

**¿Por qué lo usamos?**  
Para comprobar que el reporte incluyera la definición del problema, el arsenal,
el análisis, los requisitos, la alternativa elegida y el diagrama de flujo.

**¿Qué aceptamos?**  
La estructura general de los apartados y algunas sugerencias de redacción.

**¿Qué corregimos o descartamos?**  
El equipo revisó el contenido y lo adaptó al funcionamiento real del programa.
El diagrama de flujo utilizado es el que elaboró un integrante del equipo, no
uno generado por el modelo.

## Prompt 3: integración del programa

**Prompt resumido:** Ayudar a organizar un archivo `main.py` que conecte el
lector BMP, el segmentador, el analizador geométrico, el clasificador y el
reporte de consola.

**¿Por qué lo usamos?**  
Para revisar que las partes desarrolladas por los integrantes pudieran
ejecutarse juntas desde la terminal y siguieran el orden correcto.

**¿Qué aceptamos?**  
La propuesta de organizar el flujo en etapas: leer la imagen, segmentar las
figuras, analizar cada región, clasificarla y mostrar los resultados.

**¿Qué corregimos o descartamos?**  
El equipo comparó la propuesta con las clases y métodos que ya existían y
conservó únicamente lo que coincidía con el código integrado. Después probamos
el programa con las imágenes del banco.

## Caso en que se detectó un problema

Durante las pruebas, algunos círculos no se reconocían correctamente porque el
analizador exigía una variación radial menor que `0.02`. El equipo revisó el
código y las pruebas, cambió ese límite a `0.04` para tolerar las pequeñas
variaciones producidas por los píxeles de la imagen y volvió a ejecutar el
banco de pruebas. Después del ajuste, las pruebas automatizadas pasaron y las
diez imágenes produjeron los resultados esperados.

## Comprensión del algoritmo

Sin apoyo del modelo, el equipo puede explicar el funcionamiento: el programa
lee y valida el BMP, identifica el color del fondo, separa las figuras
conectadas mediante BFS, analiza sus fronteras y características geométricas,
las clasifica como `C`, `T`, `O` o `X` y finalmente muestra su color en formato
hexadecimal.
