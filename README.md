# PR_Lab_4

Welcome to the PR Laboratory #4 project repository. This project is an exploration into creating a basic HTTP server and a parser to extract data from it. The server serves different web pages based on the requested path, and the parser is designed to extract specific data from these pages.

## Overview

The main goal of this project is to understand the workings of an HTTP server and how to extract data from web pages. The server is written in Python and uses basic socket programming to handle incoming requests. The parser, on the other hand, uses the BeautifulSoup library to parse the HTML content and extract relevant information.

## Files and Descriptions

1. **[main.py](https://github.com/Ricigeroi/PR_Lab_4/blob/master/main.py)**: The heart of the server. It sets up the HTTP server, listens for incoming connections, and serves web pages based on the requested path.

2. **[parser.py](https://github.com/Ricigeroi/PR_Lab_4/blob/master/parser.py)**: This script contains functions to extract data from the server. It connects to the server, sends HTTP requests, and parses the received HTML content.

3. **[products.json](https://github.com/Ricigeroi/PR_Lab_4/blob/master/products.json)**: A JSON file containing a list of products. Each product has details like make, model, year, and description.

## Setup and Installation

1. Clone the repository to your local machine.
2. Ensure you have Python installed.
3. Install the Beatiful Soup library using `pip install beautifulsoup4`.

## Usage

1. Start the server by running `main.py`.
2. Use a web browser to navigate to `http://127.0.0.1:8080/` to view the served pages.
3. To extract data from the server, run `parser.py`.

## Routes

- `/`: Home page with a welcoming message.
- `/about`: Provides information about the PR Laboratory #4 project.
- `/contacts`: Displays contact information.
- `/products`: Lists all products links to their individual details.
- `/product/<product_id>`: Shows detailed information about a specific product.
