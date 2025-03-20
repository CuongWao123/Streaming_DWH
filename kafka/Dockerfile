FROM bitnami/kafka:latest

# Làm việc trong thư mục an toàn
WORKDIR /opt/bitnami/kafka/scripts/


COPY create-topics.sh .


USER root


RUN chmod +x create-topics.sh


USER 1001


CMD [ "/opt/bitnami/kafka/scripts/create-topics.sh" ]
