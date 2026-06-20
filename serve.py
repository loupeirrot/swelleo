#!/usr/bin/env python3
"""Mini serveur local pour prévisualiser le dashboard SurfAlert.
Sert le dossier du projet sur http://localhost:8000
Usage : python3 serve.py
"""
import functools
import http.server
import os
import socketserver

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8000"))

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"SurfAlert servi sur http://localhost:{PORT}")
    httpd.serve_forever()
