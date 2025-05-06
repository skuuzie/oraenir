from flask import Flask, jsonify, request, redirect, abort
from flask_cors import CORS

from config import *

from db.dynamodb import OraenirDDB
from logic.shorty import ShortyCore
from util.middleware import *
from util.exception import *

from traceback import format_exc

ddb = OraenirDDB()
shorty = ShortyCore(ddb.ddb)

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})
    
    logger.info('Flask is configured')

    @app.route('/')
    def index():
        """Health check"""

        return jsonify({"message": "OK"})

    @app.route('/shorty', methods=['POST'])
    @require_json_fields(['url'])
    def shorten():
        """Shorten input URL and return the ID"""

        data: dict = request.get_json()
        
        url_id = shorty.shorten_link(data['url'], data.get('custom_id'))

        return jsonify({'shorty': f'/{url_id}'})
    
    @app.route('/<netloc>/<path:path>')
    def unshort(netloc, path):
        """Extract the URL ID and redirect it to the target URL"""

        if netloc != 's':
            abort(404)

        return redirect(shorty.open_shortened_link(path), 302)
    
    @app.errorhandler(404)
    def handle_404(error):
        """Handle non-existant page or route"""
        
        return "Not found.", 404
    
    @app.errorhandler(OraenirException)
    def handle_custom_exception(error: OraenirException):
        """Handle critical exception caused by user"""

        response = jsonify({'message': error.message})
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(Exception)
    def handle_uncaught_exception(error: Exception):
        """Uncaught error that breaks the flow of the system"""

        logger.critical(format_exc())
        return "Server error.", 503

    return app