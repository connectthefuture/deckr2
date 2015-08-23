"""
Run the simple client. Run this interactivily with python -i ./bin/run_simple_client.py
"""

from tests.test_integration.simple_client import SimpleClient

if __name__ == "__main__":
    connection = SimpleClient()
    connection.initalize()
