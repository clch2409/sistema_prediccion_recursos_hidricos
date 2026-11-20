import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

COLOR_FONDO_TITULO = "#1d3f66"
COLOR_BOTON = "#1d3a5c"
COLOR_BOTON_ACTIVO = "#059669"
COLOR_PANEL = "#667790"
COLOR_OK = "#059669"
COLOR_MALO = "#dc2626"
COLOR_ALERTA_FONDO = "#2a1a1a"


def crear_tabla(padre, columnas, anchos):
    marco = ttk.Frame(padre)
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=12,
                         selectmode="browse")
    for columna, ancho in zip(columnas, anchos):
        tabla.heading(columna, text=columna)
        tabla.column(columna, width=ancho, anchor="center")
    barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    tabla.tag_configure("ok", foreground=COLOR_OK)
    tabla.tag_configure("malo", foreground=COLOR_MALO)
    return marco, tabla


def llenar_tabla(tabla, filas):
    """filas: lista de (valores, etiqueta) o (valores, etiqueta, iid). Conserva la selección."""
    seleccion = tabla.selection()
    for item in tabla.get_children():
        tabla.delete(item)
    for fila in filas:
        valores, etiqueta = fila[0], fila[1]
        iid = str(fila[2]) if len(fila) > 2 else None
        tabla.insert("", "end", iid=iid, values=valores, tags=(etiqueta,))
    vigentes = [i for i in seleccion if tabla.exists(i)]
    if vigentes:
        tabla.selection_set(vigentes)


def formatear_fecha(fecha):
    if fecha is None:
        return "-"
    return fecha.strftime("%d/%m/%Y %H:%M")


def formatear_fecha_corta(fecha):
    if fecha is None:
        return "-"
    return fecha.strftime("%d/%m/%Y")


def crear_barra_crud(padre, al_nuevo, al_editar, al_eliminar):
    barra = ttk.Frame(padre)
    ttk.Button(barra, text="Nuevo", command=al_nuevo).pack(side="left", padx=(0, 6))
    ttk.Button(barra, text="Editar", command=al_editar).pack(side="left", padx=6)
    ttk.Button(barra, text="Eliminar", command=al_eliminar).pack(side="left", padx=6)
    return barra


def id_seleccionado(tabla, texto="un registro"):
    """Devuelve el iid de la fila seleccionada (str) o avisa y devuelve None."""
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showinfo("Seleccione un registro", f"Seleccione {texto} de la tabla primero.")
        return None
    return seleccion[0]


def confirmar_eliminar(descripcion):
    return messagebox.askyesno(
        "Confirmar eliminación", f"¿Eliminar {descripcion}?\nEsta acción no se puede deshacer.",
        icon="warning")


def ejecutar_con_aviso(accion, parent=None):
    """Ejecuta accion(); True si salió bien. Muestra el error si falla (ValueError = validación)."""
    try:
        accion()
        return True
    except ValueError as error:
        messagebox.showwarning("No se pudo completar", str(error), parent=parent)
    except Exception as error:
        messagebox.showerror("Error", f"Error con la base de datos:\n{error}", parent=parent)
    return False


def consultar_con_aviso(consulta, parent=None):
    """Devuelve el resultado de consulta(), o None si falló (mostrando el error)."""
    resultado = []
    if ejecutar_con_aviso(lambda: resultado.append(consulta()), parent=parent):
        return resultado[0]
    return None


def _a_numero(texto, etiqueta):
    texto = texto.strip().replace(",", ".")
    if not texto:
        return None
    try:
        return float(texto)
    except ValueError:
        raise ValueError(f"{etiqueta} debe ser un número")


def _a_fecha(texto, etiqueta):
    texto = texto.strip()
    if not texto:
        return None
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            pass
    raise ValueError(f"{etiqueta} debe tener el formato AAAA-MM-DD (o DD/MM/AAAA)")


class FormularioDialogo(tk.Toplevel):
    """Ventana modal con campos. Al guardar llama a al_guardar(valores: dict).

    Cada campo es un dict: clave, etiqueta, tipo, y opcionalmente valor, opciones, editable.
    tipo: texto | numero | fecha | combo | clave | bool | texto_largo
    opciones (combo): lista de (id, texto). El valor de un combo es el id.
    """

    def __init__(self, padre, titulo, campos, al_guardar):
        super().__init__(padre)
        self.title(titulo)
        self.resizable(False, False)
        self.transient(padre.winfo_toplevel())
        self.campos = campos
        self.al_guardar = al_guardar
        self.widgets = {}

        cuerpo = ttk.Frame(self, padding=16)
        cuerpo.pack(fill="both", expand=True)
        for fila, campo in enumerate(campos):
            ttk.Label(cuerpo, text=campo["etiqueta"]).grid(row=fila, column=0, sticky="nw",
                                                          padx=(0, 10), pady=5)
            self.widgets[campo["clave"]] = self._crear_widget(cuerpo, campo)
            self.widgets[campo["clave"]][0].grid(row=fila, column=1, sticky="we", pady=5)

        botones = ttk.Frame(cuerpo)
        botones.grid(row=len(campos), column=0, columnspan=2, pady=(14, 0), sticky="e")
        ttk.Button(botones, text="Guardar", command=self._guardar).pack(side="left", padx=4)
        ttk.Button(botones, text="Cancelar", command=self.destroy).pack(side="left", padx=4)

        self.bind("<Escape>", lambda evento: self.destroy())
        self.update_idletasks()
        raiz = padre.winfo_toplevel()
        x = raiz.winfo_rootx() + (raiz.winfo_width() - self.winfo_width()) // 2
        y = raiz.winfo_rooty() + (raiz.winfo_height() - self.winfo_height()) // 3
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        self.wait_visibility()
        self.grab_set()
        self.focus_set()

    def _crear_widget(self, padre, campo):
        tipo = campo["tipo"]
        valor = campo.get("valor")
        editable = campo.get("editable", True)
        if tipo == "bool":
            variable = tk.BooleanVar(value=bool(valor))
            widget = ttk.Checkbutton(padre, variable=variable,
                                     state="normal" if editable else "disabled")
            return widget, variable
        if tipo == "combo":
            textos = [texto for _, texto in campo["opciones"]]
            variable = tk.StringVar()
            for id_opcion, texto in campo["opciones"]:
                if valor is not None and id_opcion == valor:
                    variable.set(texto)
            widget = ttk.Combobox(padre, textvariable=variable, values=textos, width=38,
                                  state="readonly" if editable else "disabled")
            return widget, variable
        if tipo == "texto_largo":
            widget = tk.Text(padre, width=40, height=5, wrap="word")
            widget.insert("1.0", "" if valor is None else str(valor))
            return widget, widget
        variable = tk.StringVar(value="" if valor is None else str(valor))
        widget = ttk.Entry(padre, textvariable=variable, width=40,
                           show="*" if tipo == "clave" else "",
                           state="normal" if editable else "disabled")
        return widget, variable

    def _leer(self, campo):
        tipo, etiqueta = campo["tipo"], campo["etiqueta"].rstrip(": ")
        _, variable = self.widgets[campo["clave"]]
        if tipo == "bool":
            return variable.get()
        if tipo == "texto_largo":
            return variable.get("1.0", "end").strip()
        if tipo == "combo":
            for id_opcion, texto in campo["opciones"]:
                if texto == variable.get():
                    return id_opcion
            raise ValueError(f"Seleccione: {etiqueta}")
        texto = variable.get()
        if tipo == "numero":
            return _a_numero(texto, etiqueta)
        if tipo == "fecha":
            return _a_fecha(texto, etiqueta)
        if tipo == "clave":
            return texto  # sin strip: los espacios cuentan como parte de la contraseña
        return texto.strip()

    def _guardar(self):
        try:
            valores = {campo["clave"]: self._leer(campo) for campo in self.campos}
        except ValueError as error:
            messagebox.showwarning("Datos inválidos", str(error), parent=self)
            return
        if ejecutar_con_aviso(lambda: self.al_guardar(valores), parent=self):
            self.destroy()
