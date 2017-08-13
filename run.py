from flask import Flask, request, jsonify
import os

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()