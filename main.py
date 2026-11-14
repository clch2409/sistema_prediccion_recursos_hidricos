"""
main.py - Punto de entrada. Ejecutar con:  python main.py

Aquí solo se "arma" el sistema:
   MQTT  ->  MensajeController  ->  Base de datos  ->  Controladores  ->  Vistas
"""
import tkinter as tk

from controllers.bombeo_controller import BombeoController
from controllers.dashboard_controller import DashboardController
from controllers.login_controller import LoginController
from controllers.mensaje_controller import MensajeController
from controllers.prediccion_controller import PrediccionController
from controllers.reservorio_controller import ReservorioController
from services.mqtt_service import MqttService
from views.login_view import LoginView
from views.main_window import VentanaPrincipal


def main():
    raiz = tk.Tk()
    raiz.title("Gestión y Predicción de Reservas Hídricas")
    raiz.geometry("1150x650")

    # ---- Ingesta de datos (MQTT) ----
    mensajes = MensajeController()
    mqtt = MqttService(mensajes.procesar_mensaje)
    mensajes.set_publicador(mqtt.publicar_comando)
    try:
        mqtt.iniciar()
    except Exception as error:
        print(f"No se pudo conectar al broker MQTT: {error}")

    controladores = {
        "mensajes": mensajes,
        "dashboard": DashboardController(),
        "reservorio": ReservorioController(),
        "prediccion": PrediccionController(),
        "bombeo": BombeoController(),
    }

    # ---- Login y luego ventana principal ----
    login_controller = LoginController()
    vista_login = LoginView(raiz, login_controller, al_entrar=lambda: abrir_principal())
    vista_login.pack(expand=True)

    def abrir_principal():
        vista_login.destroy()
        VentanaPrincipal(raiz, controladores).pack(fill="both", expand=True)

    def al_cerrar():
        mqtt.detener()
        raiz.destroy()

    raiz.protocol("WM_DELETE_WINDOW", al_cerrar)
    raiz.mainloop()


if __name__ == "__main__":
    main()
