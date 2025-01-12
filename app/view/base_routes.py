from flask import Blueprint, render_template, request, redirect, url_for
from ..model.car_model import Car
from app.extensions import db

bp = Blueprint('base', __name__, url_prefix='/')

@bp.route('/')
def base():
    return render_template('base_template.html')