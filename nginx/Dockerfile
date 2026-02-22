FROM nginx:stable-alpine

# Remove built-in default config
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy our config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Clear default html
RUN rm -rf /usr/share/nginx/html/*

# Copy WebUI files
COPY webui /usr/share/nginx/html