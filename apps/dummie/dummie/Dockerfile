FROM docker.io/node:lts-alpine

WORKDIR /app

RUN addgroup --system dummie-dummie && \
          adduser --system -G dummie-dummie dummie-dummie

COPY dist/apps/dummie/dummie dist
RUN chown -R dummie-dummie:dummie-dummie .

CMD [ "node", "dist" ]