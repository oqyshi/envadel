# Этап 1: Сборка
FROM node:20-alpine as build
WORKDIR /app

# Объявляем аргументы сборки
ARG VITE_CORE_API_URL
ARG VITE_SEARCH_API_URL
# Делаем их доступными для процесса npm run build
ENV VITE_CORE_API_URL=$VITE_CORE_API_URL
ENV VITE_SEARCH_API_URL=$VITE_SEARCH_API_URL

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап 2: Nginx
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]