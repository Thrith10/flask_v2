FROM node:alpine

RUN apk add --no-cache tini git \
    && npm install -g git-http-server \
    && adduser -D -g git git

USER git
WORKDIR /home/git

RUN which git-http-server

RUN git init --bare repository.git \
    && git config --global user.name "Reness Ravichandran" \
    && git config --global user.email "2201427@sit.singaporetech.edu.sg"


ENTRYPOINT ["tini", "--", "git-http-server", "-p", "3000", "/home/git"]

CMD ["git-http-server", "/home/git/repository.git"]