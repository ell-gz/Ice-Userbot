#Ice-Userbot @UsersBanned
FROM kenkannih/ice-userbot:buster

RUN git clone -b Ice-Userbot https://github.com/ell-gz/Ice-Userbot /home/iceuserbot/ \
    && chmod 777 /home/iceuserbot \
    && mkdir /home/iceuserbot/bin/

WORKDIR /home/iceuserbot/

CMD [ "bash", "start" ]
