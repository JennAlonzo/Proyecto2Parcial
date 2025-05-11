# Proyecto2Parcial

 💘 LoveAdvisor: Tu Asistente Amoroso con Árbol de Decisión

LoveAdvisor es una aplicación de escritorio construida con Python y Tkinter que te ayuda a encontrar tu pareja ideal evaluando pretendientes según tus preferencias personales. Utiliza un árbol de decisión dinámico para puntuar y clasificar a tus candidatos en función de los criterios que más valoras.

---

# 🧾 ¿Qué hace esta app?

- Permite agregar pretendientes con características como edad, personalidad, intereses, etc.
- Te hace preguntas clave sobre lo que buscas en una pareja.
- Usa un árbol de decisión personalizado para puntuar a cada pretendiente.
- Muestra un ranking de compatibilidad con las razones por las que fueron elegidos.

---

#Flujo de Uso Paso a Paso

# 1. Inicio
Al ejecutar `FoolAdvisor.py`, se abre una interfaz gráfica con dos botones:

- Preferencias: Define los aspectos más importantes en una pareja.
- Comenzar : Inicia directamente el proceso de evaluación de pretendientes.

---

# 2. Preferencias 
Aquí defines:

- Edad mínima y máxima
- Altura mínima
- Nivel educativo mínimo
- Si debe o no tener hij@s
- Personalidad ideal
- Y lo más importante: ¿Qué aspectos valoras más? (edad, personalidad, profesión, etc.)

Esto se usa para construir el árbol de decisión que filtrará a tus pretendientes.

---

# 3. Agregar Pretendientes
Debes ingresar al menos 2 pretendientes. Para cada uno se solicita:

- Apodo
- Edad
- Género
- Personalidad
- Nivel económico y educativo
- Altura
- Profesión/carrera
- Si tiene hij@s
- Intereses

Después de agregarlos, presiona "Continuar a preguntas 💋".

---

# 4. Responde Preguntas Personales
Responde 6 preguntas clave, como:

- ¿Debe tener una carrera?
- ¿Qué personalidad prefieres?
- ¿Debe compartir intereses contigo?
- ¿Preferencias respecto a hij@s?
- ¿Nivel educativo mínimo?
- ¿Altura mínima?

Las respuestas se usan para ajustar el puntaje de cada pretendiente.

---

# 5. Resultados Finales
La app muestra los **3 pretendientes más compatibles** con:

- Su apodo, edad, altura, nivel educativo y profesión.
- Puntaje total (hasta 9 puntos).
- Razones detalladas por las que fueron seleccionados.


# 6. Reiniciar
Desde la pantalla de resultados puedes presionar **"Comenzar de nuevo"** para borrar datos y empezar desde cero.

---

# Requisitos

- Python 3.7 o superior
- No requiere instalación de librerías externas (usa solo módulos estándar)
