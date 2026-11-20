import tkinter as tk
from tkinter import ttk, messagebox


class LoginView(ttk.Frame):
    def __init__(self, padre, login_controller, al_entrar):
        super().__init__(padre, padding=30)
        self.login_controller = login_controller
        self.al_entrar = al_entrar

        ttk.Label(self, text="Sistema de Gestión y Predicción\nde Reservas Hídricas",
                  font=("Arial", 16, "bold"), justify="center").pack(pady=(10, 25))

        ttk.Label(self, text="Usuario").pack(anchor="w")
        self.entrada_usuario = ttk.Entry(self, width=30)
        self.entrada_usuario.pack(pady=(0, 10))

        ttk.Label(self, text="Contraseña").pack(anchor="w")
        self.entrada_clave = ttk.Entry(self, width=30, show="*")
        self.entrada_clave.pack(pady=(0, 15))
        self.entrada_clave.bind("<Return>", lambda evento: self.entrar())

        ttk.Button(self, text="Ingresar", command=self.entrar).pack()
        self.entrada_usuario.focus()

    def entrar(self):
        usuario = self.entrada_usuario.get().strip()
        clave = self.entrada_clave.get()
        try:
            correcto = self.login_controller.iniciar_sesion(usuario, clave)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo consultar la base de datos:\n{error}")
            return
        if correcto:
            self.al_entrar()
        else:
            messagebox.showwarning("Acceso denegado", "Usuario o contraseña incorrectos")
