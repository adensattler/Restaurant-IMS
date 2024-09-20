from app import create_app
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = create_app()

if __name__ == "__main__":
    port = int(getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)