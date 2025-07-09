# --- Fase 1: Base e Dipendenze ---
# Usiamo una versione specifica e un'immagine "slim" per ridurre le dimensioni
FROM python:3.11-slim as base

# Imposta le variabili d'ambiente per Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Imposta la directory di lavoro
WORKDIR /app

# Installa le dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# --- Fase 2: Builder ---
# Questa fase installa le dipendenze Python
FROM base as builder

# Aggiorna pip e installa le dipendenze
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# --- Fase 3: Runtime ---
# Questa è l'immagine finale che verrà eseguita
FROM base as runtime

# Copia le dipendenze installate dalla fase "builder"
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Crea un utente non-root per motivi di sicurezza
RUN addgroup --system app && adduser --system --group app

# Copia il codice dell'applicazione
COPY . .

# Raccogli i file statici di Django
# --noinput evita che il comando chieda conferme
# RUN python manage.py collectstatic --noinput

# Cambia il proprietario dei file all'utente "app"
RUN chown -R app:app /app

# Passa all'utente non-root
USER app

# Esponi la porta su cui Gunicorn sarà in ascolto
EXPOSE 8000

# Comando per avviare l'applicazione in produzione con Gunicorn
# Assumendo che il tuo progetto Django si chiami "django-store"
# Se il file wsgi.py si trova in una cartella con un altro nome, modificalo
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "django_store.wsgi:application"]