import datetime

clientes = {}
creditos = {}
seq_credito = 5000

TIPOS_CUENTA = ["AHORROS", "CORRIENTE", "CDT"]
TIPOS_CREDITO = ["LIBRE_INVERSION", "VIVIENDA", "COMPRA_AUTO"]

def hoy():
    return datetime.date.today().isoformat()

def norm(opcion: str) -> str:
    if not opcion:
        return ""
    t = opcion.strip().upper().replace("  ", " ")
    t = t.replace("CUENTA DE ", "").replace("CUENTA ", "")
    t = t.replace("LIBRE INVERSIÓN", "LIBRE_INVERSION").replace("LIBRE INVERSION", "LIBRE_INVERSION")
    t = t.replace("COMPRA DE AUTOMOVIL", "COMPRA_AUTO").replace("COMPRA DE AUTOMÓVIL", "COMPRA_AUTO")
    t = t.replace("COMPRA AUTOMOVIL", "COMPRA_AUTO").replace("COMPRA AUTOMÓVIL", "COMPRA_AUTO")
    t = t.replace("AUTOMOVIL", "AUTO").replace("AUTOMÓVIL", "AUTO")
    return t

def input_no_vacio(msg):
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("El valor no puede estar vacío.")

def input_int(msg):
    while True:
        try:
            v = int(input(msg).strip())
            return v
        except ValueError:
            print("Valor inválido. Intente de nuevo.")

def input_float(msg):
    while True:
        try:
            v = float(input(msg).strip())
            return v
        except ValueError:
            print("Valor inválido. Intente de nuevo.")

def validar_email_simple(correo: str) -> bool:
    return "@" in correo and "." in correo.split("@")[-1]

def login_basico():
    nombre = input_no_vacio("Nombre: ")
    cc = input_no_vacio("Cédula: ")
    return nombre, cc

def existe_cliente(cc):
    return cc in clientes

def validar_sesion_para_operar(nombre, cc) -> bool:
    if not existe_cliente(cc):
        print("No existe registro de cliente. Debe crear su cuenta primero.")
        return False
    if clientes[cc]["nombre"].strip().upper() != nombre.strip().upper():
        print("Los datos de login no coinciden con el registro.")
        return False
    return True

def apuntar_mov_cliente(cc, tipo, detalle, monto=None):
    mov = {"fecha": hoy(), "tipo": tipo, "detalle": detalle}
    if monto is not None:
        mov["monto"] = monto
    clientes[cc]["historial"].append(mov)

def apuntar_mov_producto(cc, producto, tipo, monto):
    mov = {"fecha": hoy(), "tipo": tipo, "monto": monto}
    clientes[cc]["productos"][producto]["historial"].append(mov)

def crear_cuenta():
    print("\n== Crear cuenta ==")
    cc = input_no_vacio("Cédula de ciudadanía: ")
    if existe_cliente(cc):
        print("Ya existe una cuenta registrada para esta cédula.")
        return
    nombre = input_no_vacio("Nombre completo: ")
    while True:
        email = input_no_vacio("Email: ")
        if validar_email_simple(email):
            break
        print("Email inválido.")
    edad = input_int("Edad: ")
    movil = input_no_vacio("Contacto teléfono móvil: ")
    ubicacion_label = input_no_vacio("Ubicación (descripción breve, por ejemplo 'Residencia principal'): ")
    pais = input_no_vacio("País: ")
    dpto = input_no_vacio("Departamento: ")
    ciudad = input_no_vacio("Ciudad: ")
    direccion = input_no_vacio("Dirección: ")
    clientes[cc] = {
        "nombre": nombre,
        "email": email,
        "edad": edad,
        "contacto": {"movil": movil},
        "ubicacion": {
            "descripcion": ubicacion_label,
            "pais": pais,
            "departamento": dpto,
            "ciudad": ciudad,
            "direccion": direccion
        },
        "productos": {
            "AHORROS": {"saldo": 0.0, "historial": []},
            "CORRIENTE": {"saldo": 0.0, "historial": []},
            "CDT": {"saldo": 0.0, "historial": []}
        },
        "historial": []
    }
    apuntar_mov_cliente(cc, "ALTA_CLIENTE", "Registro de cliente")
    print("Cuenta creada correctamente.")

def depositar_dinero():
    print("\n== Depositar dinero ==")
    nombre, cc = login_basico()
    if not validar_sesion_para_operar(nombre, cc):
        return
    print("Portafolio de depósito: AHORROS, CORRIENTE, CDT")
    destino = norm(input_no_vacio("Producto destino: "))
    if destino not in TIPOS_CUENTA:
        print("Producto no válido.")
        return
    valor = input_float("Valor a depositar: ")
    if valor <= 0:
        print("El valor debe ser positivo.")
        return
    clientes[cc]["productos"][destino]["saldo"] += valor
    apuntar_mov_producto(cc, destino, "DEPOSITO", valor)
    apuntar_mov_cliente(cc, "DEPOSITO", f"Depósito a {destino}", valor)
    print(f"Depósito realizado. Saldo {destino}: {clientes[cc]['productos'][destino]['saldo']:.2f}")

def solicitar_credito():
    global seq_credito
    print("\n== Solicitar crédito ==")
    nombre, cc = login_basico()
    if not validar_sesion_para_operar(nombre, cc):
        return
    print("Portafolio de crédito: LIBRE_INVERSION, VIVIENDA, COMPRA_AUTO")
    tipo = norm(input_no_vacio("Tipo de crédito: "))
    if tipo not in TIPOS_CREDITO:
        print("Tipo de crédito no válido.")
        return
    monto = input_float("Valor a solicitar: ")
    if monto <= 0:
        print("El monto debe ser positivo.")
        return
    seq_credito += 1
    id_prod = seq_credito
    creditos[id_prod] = {
        "cc": cc,
        "tipo": tipo,
        "fecha_inicio": hoy(),
        "estado": "ACTIVO",
        "monto": monto,
        "saldo_pendiente": monto,
        "historial": [{"fecha": hoy(), "evento": "APROBACION", "monto": monto}]
    }
    apuntar_mov_cliente(cc, "ALTA_CREDITO", f"Crédito {tipo} aprobado ID {id_prod}", monto)
    print(f"Crédito aprobado. Número de producto: {id_prod}. Fecha de inicio: {creditos[id_prod]['fecha_inicio']}")

def retirar_dinero():
    print("\n== Retirar dinero ==")
    nombre, cc = login_basico()
    if not validar_sesion_para_operar(nombre, cc):
        return
    print("Origen del retiro (solo AHORROS o CORRIENTE):")
    origen = norm(input_no_vacio("Producto origen: "))
    if origen not in ["AHORROS", "CORRIENTE"]:
        print("Solo se permite retirar de AHORROS o CORRIENTE.")
        return
    valor = input_float("Valor a retirar: ")
    if valor <= 0:
        print("El valor debe ser positivo.")
        return
    saldo = clientes[cc]["productos"][origen]["saldo"]
    if valor <= saldo:
        clientes[cc]["productos"][origen]["saldo"] -= valor
        apuntar_mov_producto(cc, origen, "RETIRO", -valor)
        apuntar_mov_cliente(cc, "RETIRO", f"Retiro desde {origen}", -valor)
        print("Transacción confirmada.")
        print(f"Saldo {origen}: {clientes[cc]['productos'][origen]['saldo']:.2f}")
    else:
        print("Fondos insuficientes.")

def pagar_cuenta_credito():
    print("\n== Pago cuenta crédito ==")
    nombre, cc = login_basico()
    if not validar_sesion_para_operar(nombre, cc):
        return
    try:
        id_prod = int(input_no_vacio("Número de producto del crédito: "))
    except ValueError:
        print("Número de producto inválido.")
        return
    if id_prod not in creditos or creditos[id_prod]["cc"] != cc:
        print("No existe ese crédito para el cliente.")
        return
    cr = creditos[id_prod]
    print(f"Fecha de inicio: {cr['fecha_inicio']}")
    print(f"Estado actual: {cr['estado']}")
    print(f"Saldo pendiente: {cr['saldo_pendiente']:.2f}")
    if cr["estado"] in ["CANCELADO", "PAGADO", "INACTIVO"]:
        print("El crédito no admite pagos en su estado actual.")
        return
    print("Seleccione cuenta para debitar (AHORROS o CORRIENTE):")
    origen = norm(input_no_vacio("Cuenta origen: "))
    if origen not in ["AHORROS", "CORRIENTE"]:
        print("Cuenta no válida para pago.")
        return
    pago = input_float("Valor a pagar: ")
    if pago <= 0:
        print("El pago debe ser positivo.")
        return
    if clientes[cc]["productos"][origen]["saldo"] < pago:
        print("Saldo insuficiente en la cuenta seleccionada.")
        return
    clientes[cc]["productos"][origen]["saldo"] -= pago
    cr["saldo_pendiente"] -= pago
    cr["historial"].append({"fecha": hoy(), "evento": "PAGO", "monto": pago})
    apuntar_mov_producto(cc, origen, "PAGO_CREDITO", -pago)
    apuntar_mov_cliente(cc, "PAGO_CREDITO", f"Pago al crédito {id_prod} desde {origen}", -pago)
    if cr["saldo_pendiente"] <= 0.01:
        cr["saldo_pendiente"] = 0.0
        cr["estado"] = "PAGADO"
        print("Pago aplicado. El crédito ha quedado PAGADO.")
    else:
        print(f"Pago aplicado. Saldo pendiente actual: {cr['saldo_pendiente']:.2f}")

def cancelar_cuenta():
    print("\n== Cancelar cuenta (borrar todos los datos) ==")
    nombre, cc = login_basico()
    if not validar_sesion_para_operar(nombre, cc):
        return
    for cid in list(creditos.keys()):
        if creditos[cid]["cc"] == cc:
            del creditos[cid]
    del clientes[cc]
    print("La cuenta y todos los datos del cliente han sido eliminados.")

def mostrar_saldos_y_historial_y_salir():
    print("\n== Salir y mostrar resumen ==")
    nombre, cc = login_basico()
    if not existe_cliente(cc) or clientes[cc]["nombre"].strip().upper() != nombre.strip().upper():
        print("No hay datos para el usuario indicado.")
        print(f"Este bien, vuelva pronto, {nombre}.")
        return
    ah = clientes[cc]["productos"]["AHORROS"]["saldo"]
    co = clientes[cc]["productos"]["CORRIENTE"]["saldo"]
    cd = clientes[cc]["productos"]["CDT"]["saldo"]
    print(f"Saldo AHORROS: {ah:.2f}")
    print(f"Saldo CORRIENTE: {co:.2f}")
    print(f"Saldo CDT: {cd:.2f}")
    print("\nHistorial de transacciones del cliente:")
    for i, mov in enumerate(clientes[cc]["historial"], start=1):
        linea = f"{i}. {mov['fecha']} | {mov['tipo']} | {mov['detalle']}"
        if "monto" in mov:
            linea += f" | {mov['monto']:.2f}"
        print(linea)
    print(f"\nEste bien, vuelva pronto, {clientes[cc]['nombre']}.")

def menu():
    while True:
        print("\n=== Sistema de Gestión de Cuentas Bancarias ===")
        print("1. Crear cuenta")
        print("2. Depositar dinero")
        print("3. Solicitar crédito")
        print("4. Retirar dinero")
        print("5. Pago cuenta crédito")
        print("6. Cancelar cuenta")
        print("7. Salir (mostrar saldos e historial)")
        op = input("Seleccione una opción: ").strip()
        if op == "1":
            crear_cuenta()
        elif op == "2":
            depositar_dinero()
        elif op == "3":
            solicitar_credito()
        elif op == "4":
            retirar_dinero()
        elif op == "5":
            pagar_cuenta_credito()
        elif op == "6":
            cancelar_cuenta()
        elif op == "7":
            mostrar_saldos_y_historial_y_salir()
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
