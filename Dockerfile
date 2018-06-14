FROM python:3.6

RUN apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev

RUN pip install numpy telepot flask opencv-python gunicorn

RUN git clone https://github.com/jasperproject/jasper-client.git jasper \
        && chmod +x jasper/jasper.py \
        && pip install --upgrade setuptools \
        && pip install -r jasper/client/requirements.txt

ADD const.py /

ADD config.py /

ADD app.py /

RUN python config.py

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]