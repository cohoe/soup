#!/usr/bin/env python

from flask import Flask

soup = Flask(__name__)
from soup import views
