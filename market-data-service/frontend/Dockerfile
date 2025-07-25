FROM node:lts
# Set working directory
WORKDIR /market-data-service/frontend

# install node modules
COPY ./package*.json ./
RUN npm install

# Copy all files from current directory to working dir in image
COPY . .

EXPOSE 3000

ENV HOST 0.0.0.0


ENTRYPOINT [ "npm", "start"]