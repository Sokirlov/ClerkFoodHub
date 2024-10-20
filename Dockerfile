FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Налаштовуємо українську локаль
RUN sed -i '/uk_UA.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen uk_UA.UTF-8

# Встановлюємо системну локаль за замовчуванням
ENV LANG=uk_UA.UTF-8 \
    LANGUAGE=uk_UA:uk \
    LC_ALL=uk_UA.UTF-8

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD ["python", "start.py"]
#EXPOSE 8002
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]