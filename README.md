# COVID19p

COVID19p es un lenguaje de programación bajo el fundamento de Little Languages con el fin de proveer herramientas de cálculo sencillas y funciones estadísticas y gráficas básicas para auxiliar en el procesamiento de datos.

## Instalación

Clona el repositorio y extrae el directorio principal a tu computadora.
Además, para utilizarlo necesitas:
* Python3+
* pip
* Las librerías [plotly](https://plotly.com/python/) y [numpy](https://numpy.org/). Puedes instalarlas a través de pip

```bash
pip install [inserte nombre de paquete plotly]
pip install numpy
```

## Uso
[TBD: Manual de referencia rápida](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
[TBD: Video tutorial < 1 min](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
```c++
program prueba;
var int: a, xyz[20], b;
bool: t, f;

function int hello (float x, float y, int re, int be) {
    a = 1;
    b = 2;
    t = true;
    f = false;
}

function void there (int a, int b) {
    a = 1;
    b = a + 10;
}

main ()
var int: x, c, d, y, ren, col, dev[10][2], ted[19];
    float: xx, yy;
    dataFrame: myData, frame;
{
    x = 30;
    d = 10;
    c = 14;
    y = 400;
    b = 30;

    t = true;
    f = false;

    a = d + c;
    x = (a + c) * d / d;
    if (b > c) then {
        t = f && f;
        t = true;
    } else {
        t = f || f;
    }


    load(myData, "miRuta", ren, col);


    while (x > c) do {
        t = b + a;
        x = x - 1;
    }

    xx = 42.1;
    yy = 12.3;
    hello(xx,yy, x + c, c + x);

    from a = a to b do {
        b = x + c;
    }

    dev[1][1] = 18;
    dev[3][0] = 10;

    write(xx, yy, x);

    load(frame, "i", x, y);

    return (a);
}
```
## Autores
Este proyecto fue trabajado por Nissim Betesh y Alejandro Longoria, estudiantes del Tecnológico de Monterrey.

## Contribuciones
Pull requests son bienvenidas. Para mayores cambios, por favor inicia un issue para discutir lo que te gustaría cambiar del lenguaje.

Asegúrate de actualizar los casos de prueba según cambie la funcionalidad.

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)