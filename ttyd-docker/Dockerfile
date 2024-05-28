FROM alpine:3.14

RUN adduser -D  admin

# install git
RUN apk update
RUN  apk add git
RUN  apk add ttyd
RUN apk add curl

RUN apk add zsh 

RUN apk add python3 py3-pip

# volume 
RUN mkdir /home/files
RUN chown -R  admin:admin /home
RUN chmod  755 /home/files

COPY entrypoint.sh /home/entrypoint.sh
RUN chmod +x /home/entrypoint.sh

RUN python3 -m venv /venv  
ENV PATH=/venv/bin:$PATH

RUN chown -R  admin:admin /venv 
RUN chmod 755 /venv 

RUN pip3 install typer

USER admin
#oh my zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" -y



EXPOSE 7681
WORKDIR /home/files
CMD ["ttyd", "-W"]

# docker run --rm  -p 7681:7681 -v aforismi:/home/files frachecco86/aforismi_terminal

# puh to docker
# docker image push frachecco86/aforismi_terminal