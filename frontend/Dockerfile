# Stage 1: Build Vue app
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package.json and install dependencies
COPY web/package.json ./
RUN npm install

# Copy source code and build
COPY web/ ./
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
