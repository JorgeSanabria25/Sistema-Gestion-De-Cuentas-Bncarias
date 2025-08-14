Autor
-----
- Nombre: Jorge Andrés Sanabria
- Contacto: jorgeasanabria25@gmail.com

Descripción
-----------
Aplicación de consola en Python para la gestión de cuentas bancarias usando estructuras en memoria (diccionarios y listas). El sistema exige un inicio de sesión básico (nombre y cédula) y expone un menú de 7 opciones:
1) Crear cuenta: registra cédula, nombre, email, edad, teléfono móvil y ubicación (país, departamento, ciudad y dirección).
2) Depositar dinero: permite depósitos a cuenta de ahorros, cuenta corriente o CDT.
3) Solicitar crédito: crea productos de crédito (libre inversión, vivienda, compra de automóvil), asigna número de producto y guarda fecha de inicio.
4) Retirar dinero: valida saldo disponible en ahorros o corriente y confirma la transacción.
5) Pago cuenta crédito: recibe número de producto, muestra fecha de inicio y estado (activo, inactivo, cancelado, pagado) y permite registrar pagos.
6) Cancelar cuenta: elimina la cuenta del cliente y todos sus datos.
7) Salir: muestra saldos actuales e historial de transacciones, luego finaliza.

Stack Tecnologico
-----------------
- Lenguaje: Python 3.x
- Tipo de aplicación: CLI (línea de comandos)
- Estructuras: diccionarios, listas, funciones
- Biblioteca estándar usada: datetime

Requerimientos
--------------
- Python 3.8 o superior (recomendado 3.10+)
- No requiere librerías externas

Ejecución : Como se ejecuta su proyecto
---------------------------------------

Linux
-----
```bash
python3 sistema_gestion_bancaria.py
```

Windows
-------
```powershell
py sistema_gestion_bancaria.py
```
o
```powershell
python sistema_gestion_bancaria.py
```

Estructura de Archivos
----------------------
```
.
├── sistema_gestion_bancaria.py
└── README.md
```

Librerias Externas
------------------
No utiliza librerías externas; todo corresponde a la biblioteca estándar de Python.
