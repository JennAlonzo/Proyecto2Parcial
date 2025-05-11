import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

class DecisionNode:
    def __init__(self, attribute=None, threshold=None, left=None, right=None, result=None):
        self.attribute = attribute  # Atributo para dividir (ej. "Edad")
        self.threshold = threshold  # Valor umbral para la división
        self.left = left            # Nodo izquierdo (valores <= threshold)
        self.right = right          # Nodo derecho (valores > threshold)
        self.result = result        # Resultado si es nodo hoja

class LoveAdvisorApp(tk.Tk):
    def __init__(self):
        self.preferences = {}
        super().__init__()
        self.title("LoveAdvisor 💘 (Árbol de Decisión)")
        self.geometry("800x600")
        self.configure(bg="#ffe6f0")

        self.container = tk.Frame(self, bg="#ffe6f0")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (StartPage, PreferencesPage, AddCandidatesPage, QuestionsPage, ResultPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(StartPage)
        
        # Construir el árbol de decisión
        self.decision_tree = self.build_decision_tree(self.preferences)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_frame(self, cont):
        return self.frames[cont]
    
    def build_decision_tree(self, preferences=None):
        prefs = preferences or {}
        prioridades = prefs.get("Prioridades", []) #lista de strings
        
        # Crea posibles nodos
        nodos_disponibles = {
            "Edad": lambda: DecisionNode(attribute="Edad", threshold=30,
                                     left=DecisionNode(result="Puntaje medio"),
                                     right=None),  # right se conecta después
            "Nivel educativo": lambda: DecisionNode(attribute="Nivel educativo", threshold="Universidad",
                                     left=DecisionNode(result="Bajo puntaje"),
                                     right=None),
            "Altura": lambda: DecisionNode(attribute="Altura", threshold=170,
                                     left=DecisionNode(result="Puntaje medio"),
                                     right=None),
            "Nivel económico": lambda: DecisionNode(attribute="Nivel económico", threshold="Medio",
                                     left=DecisionNode(result="Bajo puntaje"),
                                     right=None),
            "Personalidad": lambda: DecisionNode(attribute="Personalidad", threshold=prefs.get("Personalidad ideal", "Indiferente"),
                                     left=DecisionNode(result="Bajo puntaje"),
                                     right=None)
        }

    # Si tiene una personalidad ideal clara, puede ser nodo raíz
        if prefs.get("Personalidad ideal") and prefs["Personalidad ideal"] != "Indiferente":
            root = nodos_disponibles["Personalidad"]()
            prioridades = [p for p in prioridades if p != "Personalidad"]
        else:
            root = None

    # Construir árbol según prioridades
        current = root
        if not prioridades and (prefs.get("Personalidad ideal") in [None, "", "Indiferente"]):
    # No hay prioridades ni personalidad, usar árbol por defecto
            return DecisionNode(attribute="Género", threshold="Masculino",
                        left=DecisionNode(result="Puntaje bajo"),
                        right=DecisionNode(result="Puntaje medio"))

        for p in prioridades:
            node = nodos_disponibles[p]()
            if current is None:
                current = node
                root = current
            else:
            # Encuentra la hoja derecha más profunda y conéctala
                cursor = current
                while cursor.right is not None and cursor.result is None:
                    cursor = cursor.right
                cursor.right = node
                current = node

    # Si quedan nodos no prioritarios, agrégalos al final
        for p, gen_node in nodos_disponibles.items():
            if p not in prioridades and (p != "Personalidad" or prefs.get("Personalidad ideal") == "Indiferente"):
                node = gen_node()
                cursor = current
                while cursor.right is not None and cursor.result is None:
                    cursor = cursor.right
                cursor.right = node
                current = node

    # Asegura una hoja final
        if current.right is None:
            current.right = DecisionNode(result="Alto puntaje")
            
        if root is None:
            #arbol por defecto
            root = DecisionNode(attribute="Género", threshold="Masculino",
                                left=DecisionNode(result="Puntaje bajo"),
                                right=DecisionNode(result="Puntaje medio"))

        return root 

    def evaluate_candidate(self, candidate, responses):
        # Evaluar un candidato usando el árbol de decisión y las respuestas del usuario
        node = self.decision_tree
        score = 0
        
        while node.result is None:
            attr = node.attribute
            threshold = node.threshold
            
            # Manejar diferentes tipos de atributos
            if attr in ["Edad", "Altura"]:
                try:
                    value = int(candidate[attr])
                except:
                    value = 0
                if value <= threshold:
                    node = node.left
                else:
                    node = node.right
            else:
                if candidate[attr] == threshold:
                    node = node.left
                else:
                    node = node.right
        razones = []
        # Asignar puntaje basado en el resultado del nodo hoja
        if node.result == "Alto puntaje":
            score = 3
            razones.append("Cumple con todos los atributos clave del árbol de decisión")
        elif node.result == "Puntaje medio":
            score = 2
            razones.append("Cumple parcialmente con los atributos clave del árbol de decisión")
        elif node.result == "Puntaje bajo":
            score = 1
            razones.append("Cumple mínimamente con los atributos clave del árbol de decisión")
        else:
            score = 0
            razones.append("No cumple con los atributos clave del árbol de decisión")
        
        # Ajustar puntaje basado en respuestas del usuario
        #Profesión definida
        if responses[0] == "Sí" and candidate["Profesión/carrera"].strip() != "":
            score += 1
            razones.append("Tiene una profesión o carrera")
        #Personalidad
        if responses[1] != "Indiferente" and candidate.get("Personalidad") == responses[1]:
            score += 1
            razones.append(f"Tiene la personalidad deseada: {responses[1]}")
        #Intereses compartidos
        if responses[2] == "Sí" and "anime" in candidate.get("Intereses", "").lower():
            score += 1
            razones.append("Comparte intereses")
        #No tener hijos
        if responses[3] == "Sí" and candidate["Es madre/padre solterx"] == "No":
            score += 1
            razones.append("No tiene hijos, como se prefiere")
        #Nivel educativo mínimo
        niveles = ["Primaria", "Secundaria", "Preparatoria", "Universidad", "Maestría"]
        nivel_requerido = responses[4]
        nivel_candidato = candidate.get("Nivel educativo", "")
        if nivel_candidato in niveles and niveles.index(nivel_candidato) >= niveles.index(nivel_requerido):
            score += 1
            razones.append(f"Cumple con el nivel educativo mínimo ({nivel_requerido})")
        #Altura mínima
        try:
            altura_min = int(responses[5])
            altura_candidato = int(candidate.get("Altura", "0"))
            if altura_candidato >= altura_min:
                score += 1
                razones.append(f"Cumple con la altura mínima deseada ({altura_min})")
        except:
            pass #si alguna conversión falla, no suma puntaje
        
        return score, razones

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffe6f0")

        title = tk.Label(self, text="💖 LoveAdvisor con Árbol de Decisión 💖", 
                        font=("Comic Sans MS", 22, "bold"), bg="#ffe6f0", fg="#cc3366")
        title.pack(pady=60)

        subtitle = tk.Label(self, text="¡Encuentra tu match ideal con inteligencia artificial!", 
                          font=("Comic Sans MS", 14), bg="#ffe6f0", fg="#cc3366")
        subtitle.pack(pady=10)
        
        prefs_btn = tk.Button(self, text="Preferencias 💡", command=lambda: controller.show_frame(PreferencesPage),
                      font=("Comic Sans MS", 14), bg="#ccccff", fg="black", width=20)
        prefs_btn.pack(pady=10)

        start_btn = tk.Button(self, text="Comenzar 💘", command=lambda: controller.show_frame(AddCandidatesPage),
                            font=("Comic Sans MS", 14), bg="#ff99cc", fg="white", width=20)
        start_btn.pack(pady=50)

class AddCandidatesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fff0f5")
        self.controller = controller
        self.candidates = []

        title = tk.Label(self, text="❤ Agrega a tus pretendientes ❤", 
                    font=("Comic Sans MS", 20, "bold"), bg="#fff0f5", fg="#cc3366")
        title.pack(pady=20)

        form_frame = tk.Frame(self, bg="#fff0f5")
        form_frame.pack(pady=10)

        self.entries = {}

        fields = [
            ("Apodo", "entry"),
            ("Edad", "entry"),
            ("Género", ["Femenino", "Masculino", "No binario"]),
            ("Personalidad", ["Romántic@", "Aventurer@", "Intelectual", "Divertid@", "Reservad@"]),
            ("Color de piel", ["Clara", "Morena", "Oscura"]),
            ("Nivel económico", ["Bajo", "Medio", "Alto"]),
            ("Nivel educativo", ["Primaria", "Secundaria", "Universidad", "Maestría"]),
            ("Altura", "entry"),
            ("Profesión/carrera", "entry"),
            ("Es madre/padre solterx", ["Sí", "No"]),
            ("Intereses", "entry")
        ]

        for i, (label_text, input_type) in enumerate(fields):
            label = tk.Label(form_frame, text=label_text + ":", 
                       font=("Comic Sans MS", 12), bg="#fff0f5", anchor="w")
            label.grid(row=i, column=0, sticky="w", pady=4)

            if input_type == "entry":
                entry = tk.Entry(form_frame, font=("Comic Sans MS", 12), width=30)
                entry.grid(row=i, column=1, pady=4)
            else:
                entry = ttk.Combobox(form_frame, values=input_type, 
                               font=("Comic Sans MS", 12), state="readonly", width=28)
                entry.grid(row=i, column=1, pady=4)
                entry.set(input_type[0])

            self.entries[label_text] = entry

        add_btn = tk.Button(self, text="Agregar pretendiente ❤️", command=self.add_candidate,
                       font=("Comic Sans MS", 12), bg="#ff6699", fg="white")
        add_btn.pack(pady=10)

        self.candidate_list = tk.Label(self, text="", font=("Comic Sans MS", 12), 
                                 bg="#fff0f5", fg="#660033")
        self.candidate_list.pack()

        next_btn = tk.Button(self, text="Continuar a preguntas 💋", command=self.go_to_questions,
                       font=("Comic Sans MS", 12), bg="#cc3366", fg="white")
        next_btn.pack(pady=15)

    def add_candidate(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        if not data["Apodo"]:
            messagebox.showwarning("Advertencia", "Debes ingresar al menos un apodo")
            return
        self.candidates.append(data)
        self.update_list()
        # Limpiar campos después de agregar
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set(entry.cget("values")[0])
            else:
                entry.delete(0, tk.END)

    def update_list(self):
        names = [c["Apodo"] for c in self.candidates]
        self.candidate_list.config(text=f"Pretendientes agregados ({len(names)}): " + ", ".join(names))

    def go_to_questions(self):
        if len(self.candidates) < 2:
            messagebox.showwarning("Advertencia", "Debes agregar al menos 2 pretendientes")
            return
        questions_page = self.controller.get_frame(QuestionsPage)
        questions_page.set_candidates(self.candidates)
        self.controller.show_frame(QuestionsPage)

class QuestionsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffeaf4")
        self.controller = controller
        self.candidates = []
        self.responses = []
        self.current_q = 0

        self.questions = [
            "¿Debe tener una profesión o carrera actualmente?",
            "¿Qué tipo de personalidad prefieres en una pareja",
            "¿Te gustaria que comparta intereses contigo (como anime, videojuegos, libros, etc.)?",
            "¿Prefieres que no tenga hij@s?",
            "¿Cuál es el nivel educativo minimo que prefieres en una pareja?",
            "¿Qué altura mínima te gustaría que tuviera tu pareja?"
        ]
        
        self.options = [
            ["Sí", "No", "Indiferente"],
            ["Romántic@", "Aventurer@", "Intelectual", "Divertid@", "Reservad@"],
            ["Sí", "No", "Indiferente"],
            ["Sí", "No", "No me importa"],
            ["Primaria", "Secundaria", "Preparatoria", "Universidad", "Maestría"],
            ["160", "170", "180", "190"]
        ]

        self.label = tk.Label(self, text="", font=("Comic Sans MS", 18), 
                            wraplength=600, bg="#ffeaf4", fg="#cc3366")
        self.label.pack(pady=40)

        self.selected = tk.StringVar()
        self.radio_buttons = []
        
        self.radio_frame = tk.Frame(self, bg="#ffeaf4")
        self.radio_frame.pack()

        self.next_btn = tk.Button(self, text="Siguiente 💌", command=self.next_question,
                                font=("Comic Sans MS", 12), bg="#cc3366", fg="white")
        self.next_btn.pack(pady=20)

    def set_candidates(self, candidates):
        self.candidates = candidates
        self.responses = []
        self.current_q = 0
        self.show_question()

    def show_question(self):
        # Limpiar radio buttons anteriores
        for widget in self.radio_frame.winfo_children():
            widget.destroy()
        
        if self.current_q < len(self.questions):
            self.label.config(text=self.questions[self.current_q])
            self.selected.set("")
            
            # Crear nuevos radio buttons para la pregunta actual
            for opt in self.options[self.current_q]:
                btn = tk.Radiobutton(self.radio_frame, text=opt, variable=self.selected, 
                                    value=opt, font=("Comic Sans MS", 14), 
                                    bg="#ffeaf4", fg="#99004d", anchor="w")
                btn.pack(pady=4, anchor="w")
        else:
            self.evaluate_matches()

    def next_question(self):
        answer = self.selected.get()
        if not answer:
            messagebox.showwarning("Advertencia", "Debes seleccionar una respuesta")
            return
        self.responses.append(answer)
        self.current_q += 1
        self.show_question()

    def evaluate_matches(self):
        # Evaluar cada candidato usando el árbol de decisión
        scored_candidates = []
        for candidate in self.candidates:
            score, razones = self.controller.evaluate_candidate(candidate, self.responses)
            scored_candidates.append((score, candidate, razones))
        
        # Ordenar por puntaje descendente
        scored_candidates.sort(reverse=True, key=lambda x: x[0])
        
        # Mostrar resultados
        result_page = self.controller.get_frame(ResultPage)
        result_page.show_results(scored_candidates)
        self.controller.show_frame(ResultPage)

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fff0f5")
        self.controller = controller

        self.title_label = tk.Label(self, text="💘 Tus Matches Ideales 💘", 
                                  font=("Comic Sans MS", 24, "bold"), 
                                  bg="#fff0f5", fg="#cc3366")
        self.title_label.pack(pady=30)

        #self.results_frame = tk.Frame(self, bg="#fff0f5")
        #self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # Contenedor con scroll
        canvas = tk.Canvas(self, bg="#fff0f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#fff0f5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")


        restart_btn = tk.Button(self, text="Comenzar de nuevo", command=self.restart,
                              font=("Comic Sans MS", 14), bg="#cc3366", fg="white", width=20)
        restart_btn.pack(pady=40)

    def show_results(self, scored_candidates):
        # Limpiar resultados anteriores
        #for widget in self.results_frame.winfo_children():
            #widget.destroy()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not scored_candidates:
            tk.Label(self.scrollable_frame, text="No hay suficientes datos para mostrar resultados",
                    font=("Comic Sans MS", 14), bg="#fff0f5").pack()
            return
        
        # Mostrar el top 3 de matches
        top_label = tk.Label(self.scrollable_frame, 
                           text="✨ Tus mejores matches basados en el árbol de decisión ✨",
                           font=("Comic Sans MS", 16, "bold"), bg="#fff0f5", fg="#660033")
        top_label.pack(pady=10)
        
        for i, (score, candidate, razones) in enumerate(scored_candidates[:3]):
            #frame = tk.Frame(self.results_frame, bg="#ffd9eb", bd=2, relief="ridge", padx=10, pady=10)
            frame = tk.Frame(self.scrollable_frame, bg="#ffd9eb", bd=2, relief="ridge", padx=10, pady=10)
            frame.pack(fill="x", pady=5, padx=20)

            pos_color = "#cc0066" if i == 0 else "#ff3399" if i == 1 else "#ff66b3"
            pos_text = "🥇 1er lugar" if i == 0 else "🥈 2do lugar" if i == 1 else "🥉 3er lugar"

            tk.Label(frame, text=pos_text, font=("Comic Sans MS", 14, "bold"),
             bg="#ffd9eb", fg=pos_color).grid(row=0, column=0, sticky="w")
    
            tk.Label(frame, text=f"👤 {candidate['Apodo']}",
             font=("Comic Sans MS", 14), bg="#ffd9eb").grid(row=1, column=0, sticky="w")

            tk.Label(frame, text=f"⭐ Puntaje: {score}/9",  # puede llegar a 9 ahora
             font=("Comic Sans MS", 12), bg="#ffd9eb").grid(row=2, column=0, sticky="w")

            details = f"Edad: {candidate['Edad']} | Altura: {candidate['Altura']} cm\n"
            details += f"Educación: {candidate['Nivel educativo']} | Profesión: {candidate['Profesión/carrera']}"
            tk.Label(frame, text=details, font=("Comic Sans MS", 11), bg="#ffd9eb",
             justify="left").grid(row=3, column=0, sticky="w", pady=(5, 0))

    # Mostrar razones de selección 
            if i == 0:
                razones_text = "\n".join([f"• {r}" for r in razones])
                tk.Label(frame, text=f"📝 ¿Por qué fue elegido?:\n{razones_text}",
                    font=("Comic Sans MS", 11), bg="#ffe6f0", justify="left", wraplength=700,
                    relief="groove", bd=1, padx=10, pady=6).grid(row=4, column=0, sticky="w", pady=(10, 0))


    def restart(self):
        # Limpiar todo y volver al inicio
        add_page = self.controller.get_frame(AddCandidatesPage)
        add_page.candidates = []
        add_page.update_list()
        
        questions_page = self.controller.get_frame(QuestionsPage)
        questions_page.responses = []
        questions_page.current_q = 0
        
        self.controller.show_frame(StartPage)
        
class PreferencesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f0ff")
        self.controller = controller

        title = tk.Label(self, text="📝 Define tus preferencias", 
                     font=("Comic Sans MS", 20, "bold"), bg="#f5f0ff", fg="#663399")
        title.pack(pady=20)

        self.entries = {}
        labels = [
            "Edad mínima", "Edad máxima",
            "Altura mínima", "Nivel educativo mínimo",
            "¿Debe tener hijos?", "Personalidad ideal"
        ]

        form_frame = tk.Frame(self, bg="#f5f0ff")
        form_frame.pack(pady=10)

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#f5f0ff", font=("Comic Sans MS", 12)).grid(row=i, column=0, sticky="w", pady=5, padx=10)

            if "educativo" in label:
                entry = ttk.Combobox(form_frame, values=["Primaria", "Secundaria", "Universidad", "Maestría"], state="readonly")
                entry.set("Secundaria")
            elif "hijos" in label:
                entry = ttk.Combobox(form_frame, values=["Sí", "No", "Indiferente"], state="readonly")
                entry.set("Indiferente")
            elif "Personalidad" in label:
                entry = ttk.Combobox(form_frame, values=["Romántic@", "Aventurer@", "Intelectual", "Divertid@", "Reservad@", "Indiferente"], state="readonly")
                entry.set("Indiferente")
            else:
                entry = tk.Entry(form_frame)

            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[label] = entry
            
        tk.Label(self, text="¿Qué aspectos valoras más en una pareja?", bg="#f5f0ff", font=("Comic Sans MS", 12, "bold")).pack(pady=(20, 5))
        prioridades_frame = tk.Frame(self, bg="#f5f0ff")
        prioridades_frame.pack()
        
        self.prioridad_vars = {
            "Edad": tk.BooleanVar(),
            "Nivel educativo": tk.BooleanVar(),
            "Altura": tk.BooleanVar(),
            "Profesión": tk.BooleanVar(),
            "Personalidad": tk.BooleanVar(),
            "Tener hij@s": tk.BooleanVar()
        }

        for i, (nombre, var) in enumerate(self.prioridad_vars.items()):
            cb = tk.Checkbutton(prioridades_frame, text=nombre, variable=var,
                        font=("Comic Sans MS", 11), bg="#f5f0ff", anchor="w")
            cb.grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=2)

        btn_frame = tk.Frame(self, bg="#f5f0ff")
        btn_frame.pack(pady=20)

        save_btn = tk.Button(btn_frame, text="Guardar preferencias 💾", bg="#9966cc", fg="white", font=("Comic Sans MS", 12),
                         command=self.save_preferences)
        save_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(btn_frame, text="Regresar ↩️", bg="#cccccc", fg="black", font=("Comic Sans MS", 12),
                         command=lambda: controller.show_frame(StartPage))
        back_btn.grid(row=0, column=1, padx=10)

    def save_preferences(self):
        self.controller.preferences = {key: entry.get() for key, entry in self.entries.items()}
        messagebox.showinfo("Preferencias guardadas", "Tus preferencias fueron guardadas 💖")
        prioridades_seleccionadas = [key for key, var in self.prioridad_vars.items() if var.get()]
        self.controller.preferences["Prioridades"] = prioridades_seleccionadas
        self.controller.show_frame(StartPage)

if __name__ == "__main__":
    app = LoveAdvisorApp()
    app.mainloop()