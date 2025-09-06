# utils/db.py
from django.db import connection

def execute_query(query, params=None):
    """Execute a raw SQL query and return the cursor"""
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        return cursor