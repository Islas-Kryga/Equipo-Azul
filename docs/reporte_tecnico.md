# Reporte técnico

## Proyecto 1: Reconocimiento de figuras

**Integrantes:** Julio César Islas Espino, Jesús Eliuth Martínez Mendoza,
Miroslava Mora Espinosa y Leo Tintos.

**Tipo de documento:** Reporte técnico del proyecto. Este documento explica el
problema, la solución implementada, las decisiones del equipo y las pruebas
realizadas. El reporte separado sobre el uso de modelos de lenguaje no forma
parte de este documento.

## 1. Definición del problema

El proyecto consiste en crear un programa capaz de reconocer figuras
geométricas dentro de una imagen BMP. La imagen puede contener una o varias
figuras, siempre que tengan colores sólidos, que no se encimen y que sean
distintas del color del fondo.

El programa se ejecuta desde la terminal. La persona que lo utiliza le indica
la ubicación de una imagen y el programa analiza su contenido. Al terminar,
debe decir cuántas figuras encontró, qué categoría tiene cada una y cuál es su
color en formato hexadecimal.

Las categorías solicitadas son:

- **C:** cuadriláteros, por ejemplo cuadrados, rectángulos, rombos o
  trapezoides.
- **T:** triángulos.
- **O:** círculos.
- **X:** cualquier figura que no corresponda a las categorías anteriores.

La entrada se proporciona así:

```bash
python -m src.main imagenes/prueba01.bmp
```

Por ejemplo, para una imagen con un triángulo rojo, la salida esperada es
semejante a:

```text
Figuras encontradas: 1

Figura 1
Categoría: T
Color: #FF0000
```

## 2. Arsenal

Elegimos **Python 3** porque nos permite concentrarnos en el problema de
procesar la imagen sin tener que construir una interfaz gráfica. Además, el
programa se puede ejecutar fácilmente desde una terminal y el código queda
dividido en partes que se pueden leer y probar por separado.

Para realizar el proyecto usamos principalmente herramientas incluidas en
Python:

- `struct` para leer los datos binarios que forman un archivo BMP.
- `collections.deque` para administrar la cola utilizada en la búsqueda BFS.
- `dataclasses` para representar de forma ordenada puntos, colores, regiones y
  límites de las figuras.
- `math` para hacer los cálculos de distancias y variación necesarios para
  reconocer círculos.
- `pytest` para ejecutar las pruebas automáticas.

No usamos una biblioteca externa de procesamiento de imágenes para que el
equipo pudiera explicar y controlar directamente cómo se lee el BMP, cómo se
separan las figuras y cómo se obtienen sus características.

## 3. Análisis del problema

### 3.1 Supuestos de las imágenes

El enunciado establece ciertas condiciones para las imágenes de prueba y
nuestra solución trabaja con ellas:

1. El fondo tiene un solo color uniforme.
2. Cada figura está formada por un color sólido.
3. Las figuras tienen colores distintos del fondo.
4. Las figuras no se superponen.
5. No hay suavizado de bordes ni colores intermedios.
6. Las figuras pueden cambiar de tamaño, posición y rotación.
7. La imagen puede contener una o varias figuras.

Estos supuestos son importantes porque permiten separar las figuras a partir
de sus colores y de la conectividad de sus píxeles.

### 3.2 Cómo se resolvió el problema

El programa está organizado como una cadena de pasos. Primero se abre la
imagen y se comprueba que realmente sea un BMP compatible. Después se detecta
el color del fondo observando el perímetro de la imagen. Los píxeles que no
pertenecen al fondo se agrupan en regiones conectadas; cada región representa
una figura.

Una vez aislada una figura, se estudia su forma. Se obtiene su frontera, se
calcula una envolvente de los puntos y se simplifica para estimar cuántos
vértices importantes tiene. También se revisa si sus distancias al centro son
parecidas, lo cual ayuda a identificar círculos. Con esas características se
elige la categoría final y se imprime el color.

### 3.3 Requisitos funcionales

Los requisitos funcionales describen lo que el programa debe hacer:

1. Recibir desde la terminal la ruta de una imagen BMP.
2. Avisar si no se recibió exactamente una ruta.
3. Abrir el archivo en modo binario.
4. Validar la firma, dimensiones, profundidad y compresión del BMP.
5. Convertir los datos de color del formato BGR a RGB.
6. Identificar el color del fondo.
7. Recorrer los píxeles de la imagen.
8. Separar las regiones que no pertenecen al fondo.
9. Agrupar los píxeles conectados de cada figura.
10. Guardar el color y los límites de cada figura.
11. Analizar la forma de cada región.
12. Reconocer círculos, triángulos, cuadriláteros y otras figuras.
13. Asignar las categorías `O`, `T`, `C` o `X`.
14. Convertir cada color a formato hexadecimal `#RRGGBB`.
15. Mostrar un reporte claro con el total y los datos de cada figura.
16. Mostrar un mensaje entendible cuando el archivo no existe o no es válido.

### 3.4 Requisitos no funcionales

También consideramos características de calidad:

- **Claridad:** la salida debe poder entenderse sin conocer el código.
- **Usabilidad:** el programa debe funcionar con un comando sencillo.
- **Mantenibilidad:** cada etapa está separada en su propio módulo.
- **Portabilidad:** el procesamiento principal no depende de una interfaz
  gráfica ni de un sistema operativo específico.
- **Confiabilidad:** se validan los archivos y se manejan errores de entrada.
- **Pruebas:** las partes importantes cuentan con pruebas automatizadas.
- **Desempeño:** el algoritmo recorre la imagen y las regiones sin realizar
  búsquedas innecesarias de archivos o procesos externos.

### 3.5 Casos límite

Durante el diseño consideramos situaciones que podían causar problemas:

- Que se ejecute el programa sin argumentos.
- Que se indiquen dos o más argumentos.
- Que la ruta no exista.
- Que el archivo no sea realmente un BMP.
- Que el BMP esté incompleto o use un formato no soportado.
- Que una imagen tenga una sola figura o varias.
- Que una figura toque un borde o una esquina.
- Que un cuadrilátero esté rotado.
- Que aparezca un pentágono u otra figura que deba clasificarse como `X`.
- Que no se encuentre ninguna figura.

## 4. Selección de la mejor alternativa

Consideramos que la alternativa más adecuada era dividir el programa en cinco
responsabilidades. Así, si una parte necesita cambiarse, no es necesario
reescribir todo el proyecto.

### 4.1 Lectura del BMP

`BmpReader` se encarga de abrir el archivo, revisar sus cabeceras y leer sus
filas. También toma en cuenta el relleno que algunos BMP agregan al final de
cada fila y convierte el orden de color BGR a RGB.

### 4.2 Segmentación con BFS

`FigureSegmenter` detecta el color del fondo y recorre la imagen. Cuando
encuentra un píxel que no es del fondo, inicia una búsqueda en anchura, o BFS.
La búsqueda visita los vecinos de arriba, abajo, izquierda y derecha que
tienen el mismo color. Al terminar, todos esos píxeles forman una región y se
guardan como una figura.

Elegimos BFS porque se adapta bien a imágenes formadas por píxeles. Nos permite
obtener cada componente conectado sin tener que adivinar primero cuántas
figuras existen. También conserva la información necesaria para conocer el
color y los límites de cada región.

### 4.3 Análisis geométrico

`GeometryAnalyzer` estudia cada región ya separada. Primero obtiene los
píxeles de la frontera. Después calcula una envolvente convexa y la simplifica
para eliminar pequeños cambios producidos por la forma pixelada.

El número de vértices restantes ayuda a distinguir triángulos y
cuadriláteros. Para reconocer círculos se comprueba que el ancho y la altura
sean parecidos y que las distancias de los píxeles de la frontera al centro
tengan poca variación.

### 4.4 Clasificación y reporte

`ShapeClassifier` aplica las reglas finales:

1. Si la región parece un círculo, se clasifica como `O`.
2. Si tiene tres esquinas, se clasifica como `T`.
3. Si tiene cuatro esquinas, se clasifica como `C`.
4. En cualquier otro caso, se clasifica como `X`.

Finalmente, `ConsoleReporter` muestra los resultados y transforma los valores
RGB a un color hexadecimal fácil de leer.

## 5. Diagrama de flujo

El diagrama de flujo fue realizado por un integrante del equipo y representa
el funcionamiento completo del programa. Incluye la lectura del BMP, la
segmentación con BFS, el análisis geométrico, la clasificación y el reporte
final.

Se entregan las dos versiones originales:

- [Diagrama de flujo en PDF](diagrama_flujo.pdf)
- [Código fuente Mermaid del diagrama](diagrama_flujo.mmd)

El archivo Mermaid se conserva para que el equipo pueda hacer cambios si el
profesor solicita alguna aclaración, mientras que el PDF sirve como versión
lista para consultar o anexar al reporte.

## 6. Pruebas y resultados

El banco de pruebas contiene diez imágenes, como solicita el enunciado. La
descripción de cada imagen y su resultado esperado está en
[imagenes/README.md](../imagenes/README.md).

Las pruebas automatizadas cubren:

- Lectura y validación de BMP.
- Segmentación de regiones.
- Detección de características geométricas.
- Clasificación de figuras.
- Conversión y presentación de colores.

La ejecución completa se realiza con:

```bash
python -m pytest -q
```

También se puede probar una imagen específica:

```bash
python -m src.main imagenes/prueba10.bmp
```

Durante la revisión del proyecto se ejecutaron las 25 pruebas automatizadas y
todas pasaron. También se procesaron las diez imágenes del banco: triángulos,
cuadriláteros, círculos, combinaciones de figuras y una figura clasificada como
`X`.

En términos de desempeño, la lectura y la segmentación recorren la imagen una
cantidad constante de veces. Si la imagen tiene `W × H` píxeles, el recorrido
principal requiere tiempo `O(W·H)`. El análisis geométrico se realiza por
figura y depende de la cantidad de píxeles de esa figura. Esto resulta
adecuado para las imágenes de tamaño moderado utilizadas en el proyecto y no
requiere servicios externos ni procesamiento en la nube.

## 7. Organización del trabajo

El equipo trabajó en ramas separadas y después integró los cambios mediante
Pull Requests en `main`:

- **Julio César Islas Espino:** arquitectura base, modelos, excepciones,
  lector BMP y pruebas de lectura.
- **Miroslava Mora Espinosa:** segmentación de figuras mediante BFS y pruebas
  del segmentador.
- **Jesús Eliuth Martínez Mendoza:** modelo de resultados, reporte de consola,
  banco de imágenes y punto de entrada `main.py`.
- **Leo Tintos:** análisis geométrico, clasificación y pruebas relacionadas.

El reporte técnico, el diagrama y el reporte de uso de modelo de lenguaje se
mantienen como documentos separados para que cada entregable sea fácil de
localizar.
