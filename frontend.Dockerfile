FROM node:16-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the frontend code
COPY frontend/ ./

# Expose the port the app runs on
EXPOSE 9080

# Command to run the application
CMD ["npm", "start"]