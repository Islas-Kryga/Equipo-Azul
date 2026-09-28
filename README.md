# PROYECTO-1-MYP — Reconocimiento de figuras geométricas

Proyecto de Modelado y Programación para detectar y clasificar figuras geométricas en imágenes BMP.

## Objetivo

El programa recibirá la ruta de una imagen `.bmp` y reportará las figuras encontradas, indicando:

- Tipo de figura: `C` (cuadrilátero), `T` (triángulo), `O` (círculo) o `X` (otro).
- Color de la figura en formato hexadecimal.

## Estructura

```text
.
├── docs/       # Reporte técnico y documentación
├── imagenes/   # Imágenes de prueba y resultados esperados
├── src/        # Código fuente
└── tests/      # Pruebas automatizadas
```

## Ejecución

El programa se ejecuta desde la raíz del repositorio indicando la ruta de una imagen BMP:

```bash
python3 -m src.main <ruta_imagen.bmp>
```

Por ejemplo:

```bash
python3 -m src.main imagenes/prueba01.bmp
```

La salida muestra la cantidad de figuras encontradas y, para cada una, su categoría y color en formato hexadecimal.

Ejemplo:

```text
Figuras encontradas: 1

Figura 1
Categoría: T
Color: #FF0000
```

## Integrantes

- Jesús Eliuth Martínez Mendoza.
- Pendiente de completar.

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

