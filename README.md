# PROYECTO-1-MYP — Reconocimiento de figuras geométricas

Proyecto de Modelado y Programación para detectar y clasificar figuras geométricas en imágenes BMP.

## Objetivo

El programa recibirá la ruta de una imagen `.bmp` y reportará las figuras encontradas, indicando:

- Tipo de figura: `C` (cuadrilátero), `T` (triángulo), `O` (círculo) o `X` (otro).
- Color de la figura en formato hexadecimal.

## Estructura

```text
.
├── imagenes/   # Imágenes de prueba y resultados esperados
├── reportes/   # Reporte técnico y reporte de uso de modelo de lenguaje
├── diagramas/  # Diagramas de flujo en PDF, PNG y Mermaid
├── src/        # Código fuente
├── tests/      # Pruebas automatizadas
└── tools/      # Herramienta para regenerar el banco de imágenes
```

## Ejecución

El programa se ejecuta desde la raíz del repositorio indicando la ruta de una imagen BMP:

```bash
python -m src.main <ruta_imagen.bmp>
```

Por ejemplo:

```bash
python -m src.main imagenes/prueba01.bmp
```

La salida muestra la cantidad de figuras encontradas y, para cada una, su categoría y color en formato hexadecimal.

Ejemplo:

```text
Figuras encontradas: 1

Figura 1
Categoría: T
Color: #FF0000
```

## Preparación y pruebas

Se necesita Python 3. Para instalar la herramienta de pruebas:

```bash
python -m pip install pytest
```

Para ejecutar todas las pruebas:

```bash
python -m pytest -q
```

Para regenerar el banco de imágenes:

```bash
python tools/generar_imagenes.py
```

Si la ruta no existe, el archivo no es un BMP compatible o se ejecuta el
programa sin una ruta, se muestra un mensaje de error y el programa termina
con código 1.

## Integrantes

- Julio César Islas Espino
- Jesús Eliuth Martínez Mendoza
- Miroslava Mora Espinosa
- Leo Tintos

## Entregables

- [Reporte técnico](reportes/reporte_tecnico.md)
- [Reporte de uso de modelo de lenguaje](reportes/reporte_lm.md)
- [Diagrama de flujo en PDF](diagramas/diagrama_flujo.pdf)
- [Diagrama de flujo en PNG](diagramas/diagrama_flujo.png)
- [Código Mermaid del diagrama](diagramas/diagrama_flujo.mmd)
- [Banco de imágenes y resultados esperados](imagenes/README.md)

## Cómo colaborar

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Islas-Kryga/PROYECTO-1-MYP.git
   cd PROYECTO-1-MYP
   ```

2. Crea una rama para tu cambio:

   ```bash
   git checkout -b nombre-de-tu-rama
   ```

3. Guarda tus cambios y crea un commit:

   ```bash
   git add .
   git commit -m "Describe el cambio"
   ```

4. Sube la rama y abre un Pull Request:

   ```bash
   git push -u origin nombre-de-tu-rama
   ```

No trabajen directamente sobre `main`; cada cambio debe pasar por una rama y un Pull Request.
