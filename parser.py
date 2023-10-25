import socket
import re
from bs4 import BeautifulSoup


def get_data(path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    request = f'GET {path} HTTP/1.1\r\nHost: 127.0.0.1:8080\r\n\r\n'
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return response


def extract_simple_page(html):
    data = ''

    soup = BeautifulSoup(html, 'html.parser')

    # Extract text within the <font> tag
    content = soup.find('font')
    for line in content:
        if line.get_text():
            data += line.get_text().strip() + '\n'

    return data.split('\n')


def extract_product_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extract text within the <font> tag
    content = soup.find('font')

    product_info = {}
    product_data = ''
    for line in content:
        if line.get_text():
            product_data += line.get_text().strip() + '\n'

    product_data = product_data.split('\n')
    for item in product_data:
        if item:
            key, value = item.split(': ')
            product_info[key.strip().lower()] = value.strip()

    return product_info


def get_products_paths(html):
    product_paths = []

    soup = BeautifulSoup(html, 'html.parser')

    # Extract 'hrefs' within the <a> tag
    content = soup.findAll('a')
    for line in content:
        product_paths.append('/' + line.get('href'))

    return product_paths


if __name__ == '__main__':
    product_paths = get_products_paths(get_data('/products'))
    simple_paths = ['/', '/about', '/contacts']

    products_info = [extract_product_info(get_data(item)) for item in product_paths]
    simple_pages_info = [extract_simple_page(get_data(item)) for item in simple_paths]

    print('Products parse result:')
    for item in products_info:
        print(f'from \'{product_paths[products_info.index(item)]}\':\t\t', item)

    print('\nSimple pages parse result:')
    for item in simple_pages_info:
        print(f'from \'{simple_paths[simple_pages_info.index(item)]}\':\t\t', item)
