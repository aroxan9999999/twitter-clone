FROM archlinux:latest

RUN pacman -Sy --noconfirm python base-devel python-pip expat openssl ca-certificates postgresql && rm -rf /var/cache/pacman/pkg/*

WORKDIR /server

COPY /server /server

COPY .env .env

RUN python -m venv venv
RUN . venv/bin/activate

RUN ./venv/bin/pip install -r /server/requirements.txt

CMD ["./venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
