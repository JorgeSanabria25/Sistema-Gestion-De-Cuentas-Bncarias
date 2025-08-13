
def menu(): 
    cuentas = {}
    while True:
        print("\n--- Sistema Gestión de Cuentas Bancarias ---")
        print("1. Crear Cuenta")
        print("2. Depositar Dinero")
        print("3. Solicitar Crédito")
        print("4. Retirar Dinero")
        print("5. Pago Cuota Crédito")
        print("6. Cancelar Cuenta")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cc = input("Ingrese CC del cliente: ")
            nombre = input("Ingrese nombre: ")
            cuentas[cc] = {
                "nombre": nombre,
                "saldo": 0,
                "credito": 0,
                "estado": "Activo"
            }
            print("Cuenta creada con éxito.")
        elif opcion == "2":
            cc = input("Ingrese CC: ")
            if cc in cuentas:
                monto = float(input("Ingrese monto a depositar: "))
                cuentas[cc]["saldo"] += monto
                print("Depósito realizado.")
            else:
                print("Cuenta no encontrada.")
        elif opcion == "3":
            cc = input("Ingrese CC: ")
            if cc in cuentas:
                monto = float(input("Ingrese monto de crédito: "))
                cuentas[cc]["credito"] += monto
                cuentas[cc]["saldo"] += monto
                print("Crédito otorgado.")
            else:
                print("Cuenta no encontrada.")
        elif opcion == "4":
            cc = input("Ingrese CC: ")
            if cc in cuentas:
                monto = float(input("Ingrese monto a retirar: "))
                if cuentas[cc]["saldo"] >= monto:
                    cuentas[cc]["saldo"] -= monto
                    print("Retiro exitoso.")
                else:
                    print("Fondos insuficientes.")
            else:
                print("Cuenta no encontrada.")
        elif opcion == "5":
            cc = input("Ingrese CC: ")
            if cc in cuentas:
                monto = float(input("Ingrese monto de pago: "))
                if cuentas[cc]["saldo"] >= monto and cuentas[cc]["credito"] > 0:
                    cuentas[cc]["saldo"] -= monto
                    cuentas[cc]["credito"] -= monto
                    print("Pago realizado.")
                else:
                    print("Fondos insuficientes o no hay crédito.")
            else:
                print("Cuenta no encontrada.")
        elif opcion == "6":
            cc = input("Ingrese CC: ")
            if cc in cuentas:
                cuentas[cc]["estado"] = "Cancelada"
                print("Cuenta cancelada.")
            else:
                print("Cuenta no encontrada.")
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
