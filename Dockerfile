FROM python:3.12-slim

WORKDIR /app

# 1) requirements.txt está en la raíz del repo
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 2) Copiamos SOLO la carpeta backend dentro del contenedor
COPY backend /app/backend

# 3) Asegurar que Python vea /app como raíz de módulos
ENV PYTHONPATH=/app
EXPOSE 8000
# 4) IMPORTANTE: levantar uvicorn apuntando a backend.app.main:app
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
