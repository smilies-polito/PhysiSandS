FROM ubuntu:22.04

ENV TZ=Europe/Rome
ENV DEBIAN_FRONTEND=noninteractive

# Installazioni
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

WORKDIR /workspace

# ENTRYPOINT corretto con gestione di argomento $0
ENTRYPOINT ["bash", "-c", "\
if [ -z \"$1\" ]; then \
  echo 'Error: output folder missing'; \
  echo 'Usage: docker run image_name /path/to/output'; \
  exit 1; \
fi && \
output_folder=\"$1\" && \
cd /workspace/test && \
python utility_test.py \"$output_folder\" && \
python quantitative_test.py \"$output_folder\" && \
python utility_test_second.py \"$output_folder\" && \
python quantitative_test_second.py \"$output_folder\" && \
cd /workspace/helpers/plots && \
python time_plot.py \"$output_folder/quantitative_test.json\" \"$output_folder/quantitative_test_second.json\" \"$output_folder\" \
", "bash"]
