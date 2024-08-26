# Use an official Ubuntu as a parent image
FROM ubuntu:24.04

# Set environment variables to avoid user interaction during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    libopencv-dev \
    libssl-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Compile the C++ program
RUN g++ -o server main.cpp -I/usr/include/opencv4 -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -lssl -lcrypto -lpthread

# Make port 8080 available to the world outside this container
EXPOSE 80

# Run the server when the container launches
CMD ["./server"]
