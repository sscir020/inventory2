from flask import Blueprint

ctr = Blueprint('ctr', __name__)

from app.ctr import form_routers,forms,nonform_router
