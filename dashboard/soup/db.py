#!/usr/bin/env python

from sqlalchemy import create_engine
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

connect = "postgresql+psycopg2://"+DB_USER+":"+DB_PASS+"@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME
engine = create_engine(connect)
dbconn = engine.connect()


