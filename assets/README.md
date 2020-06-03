# Quick Start Guide
Para empezar a trabajar con COVID-19, necesitas tener instalado Python3.8, pip, y un par de librerías.
Familiaridad con lenguajes estilo C te darán una sensación de familiaridad a la hora de trabajar con este nuevo lenguaje.

## Instalación

Clona el repositorio y extrae el directorio principal a tu computadora.
Para utilizarlo necesitas:
* Python3.8 y pip
* Las librerías [pyplot](https://matplotlib.org/api/pyplot_api.html) y [pandas](https://pandas.pydata.org/). Puedes instalarlas a través de pip

Las siguientes son instrucciones para utilizar las librerías en sistemas UNIX
```bash
python3.8 -m pip install -U matplotlib
python3.8 -m pip install -U pandas

```

## Cómo navegar
```
├── compis-covid
│   ├── compiler
│   ├── vmachine
│   ├── ...
│   ├── executer.py
│   ├── tests/
│   └── ply
```
El archivo executer.py es quien se encarga de localizar el archivo con código que vas a interpretar. Asegúrate de modificar este archivo para que pueda correr el archivo que deseas.

```python
    parse("tests/TU_ARCHIVO.txt", false)

```

Para mayor comodidad durante esta etapa de desarrollo, recomendamos que mantengas tu código fuente en la carpeta tests, en donde están ya otros ejemplos que puedes correr para probar el lenguaje.


## Tu primer programa
Esta es la estructura básica de un programa en COVID-19
```cpp
program prueba;

main ()
var int: x;
{
}
```
Salvo algunas particularidades de la estructura, como el requerir un token program seguido del nombre de tu programa, así como la declaración de variables al inicio de un módulo, este debe resultar familiar a los veteranos de la programación en C o C++

## Ejecución
Ya que hayas actualizado el archivo executer.py con el nombre de tu archivo de código, puedes correr el siguiente script en una terminal, desde el directorio raíz del proyecto:


```bash
    python3.8 executer.py
```

### Ejemplos
Este ejemplo demuestra el uso de arreglos, ciclos y expresiones. ¡Encuentra más ejemplos en la carpeta test!

```cpp
program sort;
var int: arr[6];

main()
    var int: i, j, min, temp;
{
    arr[0] = 16;
    arr[1] = 12;
    arr[2] = 8;
    arr[3] = 9;
    arr[4] = 1;
    arr[5] = 9;

    from i = 0 to 5 do {
        min = i;
        from j = i + 1 to 6 do {
            if (arr[j] < arr[min]) then {
                min = j;
            }
        }
        temp = arr[min];
        arr[min] = arr[i];
        arr[i] = temp;
    }

    from i = 0 to 6 do {
        write(arr[i]);
    }
}
```

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)