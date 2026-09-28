# Banco de pruebas

Este directorio contiene las imágenes BMP utilizadas para probar el reconocimiento
y clasificación de figuras geométricas.

Todas las imágenes tienen fondo uniforme, figuras de colores sólidos, sin
antialiasing y sin superposición.

## Resultados esperados

| Imagen | Contenido | Resultado esperado |
|---|---|---|
| `prueba01.bmp` | Triángulo rojo | T - `#FF0000` |
| `prueba02.bmp` | Cuadrado azul | C - `#0000FF` |
| `prueba03.bmp` | Círculo verde | O - `#00FF00` |
| `prueba04.bmp` | Pentágono magenta | X - `#FF00FF` |
| `prueba05.bmp` | Triángulo rojo y cuadrado azul | T - `#FF0000`, C - `#0000FF` |
| `prueba06.bmp` | Triángulo rojo, cuadrado azul y círculo verde | T - `#FF0000`, C - `#0000FF`, O - `#00FF00` |
| `prueba07.bmp` | Cuadrado rotado cian | C - `#00FFFF` |
| `prueba08.bmp` | Triángulo rojo, cuadrado azul y círculo verde de diferentes tamaños | T - `#FF0000`, C - `#0000FF`, O - `#00FF00` |
| `prueba09.bmp` | Cuadrilátero naranja tocando una esquina | C - `#FF8000` |
| `prueba10.bmp` | Triángulo rojo, cuadrado azul, círculo verde y pentágono magenta | T - `#FF0000`, C - `#0000FF`, O - `#00FF00`, X - `#FF00FF` |

## Generación

Las imágenes pueden regenerarse ejecutando desde la raíz del proyecto:

```bash
python3 tools/generar_imagenes.py
