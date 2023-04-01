from flask import Flask
from threading import Thread

import os

import discord

def start_server():
    app = Flask('')

    @app.route('/')
    def main():
        return "Your Bot Is Ready"

    def run():
        app.run(host="0.0.0.0", port=8000)

    def keep_alive():
        server = Thread(target=run)
        server.start()

    keep_alive()
