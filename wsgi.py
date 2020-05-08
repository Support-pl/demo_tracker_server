#!/usr/bin/env python3.8
from os import getenv
from app import app

from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    app.run(host=getenv('HOST'), port=getenv('PORT'))