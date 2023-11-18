# Build stage
FROM node:18 AS build-stage
WORKDIR /frontend-ts
COPY package*.json ./
ENV VITE_DJANGO_SERVER_HTTP_URL=https://192.168.1.77:8443
ENV VITE_DJANGO_SERVER_WEBSOCKET_URL=wss://192.168.1.77:8443
RUN npm install
COPY . .
RUN npm run build

# Nginx stage
FROM nginx:latest
COPY --from=build-stage /frontend-ts/dist/ /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]