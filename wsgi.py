#!/usr/bin/env python3.8
from dotenv import load_dotenv
load_dotenv()
from os import getenv

from app import app

if __name__ == "__main__":
    app.run(host=getenv('HOST'), port=getenv('PORT'))