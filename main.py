import json
import socket
import signal
import sys
import threading
import re


# Function to handle Ctrl+C and other signals
def signal_handler(sig, frame):
    print('\nShutting down the server...')
    server_socket.close()
    sys.exit(0)


def handle_request(client_socket):
    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f'Received request: \n{request_data}')

    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]

    # Init the response content and status code
    response_content = ''
    status_code = 200

    # Define a simple routing mechanism
    if path == '/':
        response_content = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Contact information</title>
                </head>
                <body>
                    <div style="display: flex; height: 500px; align-items: center; justify-content: center;">
                        <div align=center>
                            <font>
                                Hello, World!
                                <br>
                                Landing page.
                            </font>
                        </div>
                    </div>
                </body>
            </html>
        """
    elif path == '/about':
        response_content = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Contact information</title>
                </head>
                <body>
                    <div style="display: flex; height: 500px; align-items: center; justify-content: center;">
                        <div align=center>
                            <font>
                                PR Laboratory #4
                                <br>
                                About page.
                            </font>
                        </div>
                    </div>
                </body>
            </html>
        """
    elif path == '/contacts':
        response_content = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Contact information</title>
                </head>
                <body>
                    <div style="display: flex; height: 500px; align-items: center; justify-content: center;">
                        <div align=center>
                            <font>
                                FAF-213
                                <br>
                                Bardier Andrei
                                <br>
                                andrei.bardier@isa.utm.md
                            </font>
                        </div>
                    </div>
                </body>
            </html>
        """
    elif path == '/products':
        html_response = ''
        for item in products:
            product_info = item['make'] + ' ' + item['model']
            html_response += f'<a href="product/{products.index(item) + 1}">{product_info}</a> <br>'
        response_content = f"""
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Products</title>
                </head>
                <body>
                    <div style="display: flex; height: 500px; align-items: center; justify-content: center;">
                        <div align=center>
                            <font size=5px>
                                Products:
                                <br>
                                {html_response}
                            </font>
                        </div>
                    </div>
                </body>
            </html>
        """
    elif re.match(r'^/product/(\d+)$', path) and 0 < int(path.split('/')[-1]) <= len(products):
        product_info = ''

        for key, value in products[int(path.split('/')[-1]) - 1].items():
            product_info += str(key) + ': ' + str(value) + '<br>'
        response_content = f"""
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Product {path.split('/')[-1]} information</title>
                </head>
                <body>
                    <div style="display: flex; height: 500px; align-items: center; justify-content: center;">
                        <div align=center>
                            <font size=5px>
                                {product_info}
                            </font>
                        </div>
                    </div>
                </body>
            </html>
        """
    else:
        response_content = f"""
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Error</title>
                </head>
                <body>
                    <div style="display: flex; height: 500px; align-items: center; justify-content: center;">
                        <div align=center>
                            <font color='red' size=20px>
                                Error 404
                            </font>
                            <br>
                            Not found
                        </div>
                    </div>
                </body>
            </html>
        """
        status_code = 404

    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


# Open json file
# Open the file with the correct encoding
with open('products.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

products = []
for product in data:
    products.append(
        {
            'make': product.get('make'),
            'model': product.get('model'),
            'year': product.get('year'),
            'description': product.get('description')
        }
    )


print(products)

# Define the server's IP address and port
# IP address to bind to (localhost)
HOST = '127.0.0.1'

# Port to listen on
PORT = 8080

# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
# Backlog for multiple simultaneous connections
server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")
client_socket, client_address = server_socket.accept()
print(client_address)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

    try:
        # Create a thread to handle the client's request
        client_handler = threading.Thread(target=handle_request, args=(client_socket,))
        client_handler.start()
    except KeyboardInterrupt:
        # Handle Ctrl+C interruption here (if needed)
        pass
