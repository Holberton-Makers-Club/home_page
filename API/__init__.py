from flask import Blueprint, render_template, jsonify, request


api_v1 = Blueprint("api", __name__, url_prefix="/api")
