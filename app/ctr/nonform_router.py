from flask import render_template
from .__init__ import ctr
from ..models import Material

@ctr.route('/')
@ctr.route('/welcome', method=['get', ])
def welcome_user():
    return 'welcome user'
    # return render_template('welcome.html')

@ctr.route('/materials')
def show(materials):
    return render_template('material_table.html',materials=Material.query())