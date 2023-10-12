# Build stage
FROM node:18 AS build-stage
WORKDIR /frontend-ts
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Nginx stage
FROM nginx:latest
COPY --from=build-stage /frontend-ts/dist/ /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]