FROM redis:7
COPY sentinel.conf /etc/redis/sentinel.conf
EXPOSE 26379
CMD ["redis-sentinel", "/etc/redis/sentinel.conf"]
