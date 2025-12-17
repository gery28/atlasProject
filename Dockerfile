FROM python:3.11
WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/gery28/atlasProject .


# RUN python -m venv /venv

# Install deps into venv
# ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN pip install uvicorn
RUN pip install gunicorn


EXPOSE 8080
# CMD ["waitress-serve", "--threads=8", "--host=0.0.0.0", "--port=5000", "main:app"]
# CMD ["ls"]
# CMD ["uvicorn", "atlas:asgi_app", "--host", "0.0.0.0", "--port", "5000"]
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
CMD ["python","main.py"]