from flask import Flask
from api import adService
from api import userService

app = Flask(__name__)
app.register_blueprint(adService.ads)
app.register_blueprint(userService.user)
app.run(debug=True)