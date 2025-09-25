FROM node:18

WORKDIR /app

# copy package.json
COPY package.json ./

# ติดตั้ง dependencies
RUN npm install

# copy โค้ดทั้งหมด (src, public ฯลฯ)
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
