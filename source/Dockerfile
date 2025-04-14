FROM ubuntu:22.04

ENV TZ=Europe/Rome
ENV DEBIAN_FRONTEND=noninteractive

# Imposta il timezone
RUN ln -fs /usr/share/zoneinfo/Europe/Rome /etc/localtime && \
    apt update -y && \
    apt upgrade -y && \
    apt install -y \
        python3.10 \
        python3-pip \
        python-is-python3 \
        python3-venv \
        vim \
        git && \
    pip install --no-cache-dir \
        torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && \
    pip install --no-cache-dir \
        numpy==1.26.4 \
        matplotlib==3.8.2 \
        pandas==2.2.0 \
        PyYAML==6.0.1 \
        scipy==1.12.0 \
        pctk==0.2.2

# Copia tutto il contenuto nella cartella di lavoro
WORKDIR /app
COPY . .

# Comando di default (equivalente al %runscript)
ENTRYPOINT ["bash", "-c", "\
if [ -z \"$1\" ]; then \
    echo 'Error: output folder missing'; \
    echo 'usage: docker run image_name /path/to/your/output/folder'; \
    exit 1; \
fi && \
output_folder=$(realpath \"$1\") && \
cd ../test && \
python utility_test.py \"$output_folder\" && \
python quantitative_test.py \"$output_folder\" && \
python utility_test_second.py \"$output_folder\" && \
python quantitative_test_second.py \"$output_folder\" && \
cd ../helpers/plots && \
python time_plot.py \"$output_folder/quantitative_test.json\" \"$output_folder/quantitative_test_second.json\" \"$output_folder\" \
"]
