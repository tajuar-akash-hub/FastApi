# 1. #Base image 
FROM python:3.11

# 2. #Work directory 
WORKDIR /app

# 3. #copy rest of the appliction code 

COPY . .

# 4. #run
RUN pip install --no-cache-dir -r requirements.text

# 5. #port expose
EXPOSE 8500

# 6. #commnad

# CMD ["python","./app.py"]

# CMD ["streamlit", "run", "app.py"]

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]