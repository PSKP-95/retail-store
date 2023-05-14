FROM nginx

COPY dist/retail-ui /usr/share/nginx/html

# this is optional: COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-site.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf


EXPOSE 4200

#COPY ./entryPoint.sh /
#RUN chmod +x entryPoint.sh

#ENTRYPOINT ["/entryPoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

