from app import app, babel, db, migrate, render_template
from app.router import session
from app.models import User, Sector, Company, Position
from flask import g, request, Blueprint, flash, url_for
from app.v1pre.config import *

from app.v1pre.visitors import Visitors
from app.v1pre.students import Students
from app.v1pre.companies import Companies

mapped_routes = {
    'Visitor': Visitors,
    'Student': Students,
    'Company': Companies
}

routes = Blueprint('v1pre_routes', __name__, template_folder=template_f, static_folder=static_f)


@routes.route('/')
def homepage():
    try:
        return mapped_routes[session['type']].homepage()
    except AttributeError:
        return mapped_routes['Visitor'].homepage()


@routes.route('/profile')
def profile():
    try:
        return mapped_routes[session['type']].profile()
    except AttributeError:
        return mapped_routes['Visitor'].profile()
    except:
        flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
        flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
        session['redirect'] = url_for('v1pre_routes.profile')
        return render_template('template.html')


@routes.route('/company/<companyId>', methods=['GET', 'POST'])
def company_view(companyId):
    try:
        return mapped_routes[session['type']].company_view(companyId)
    except AttributeError:
        mapped_routes['Visitor'].company_view(companyId)
    except:
        flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
        flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
        session['redirect'] = url_for('v1pre_routes.company_view')
        return render_template('template.html')


@routes.route('/sector/<sectorId>', methods=['GET', 'POST'])
def sector_view(sectorId):
    try:
        return mapped_routes[session['type']].sector_view(sectorId)
    except AttributeError:
        return mapped_routes['Visitor'].sector_view(sectorId)
    except:
        flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
        flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
        session['redirect'] = url_for('v1pre_routes.sector_view')
        return render_template('template.html')


@routes.route('/position/<positionId>', methods=['GET', 'POST'])
def position_view(positionId):
    try:
        return mapped_routes[session['type']].position_view(positionId)
    except AttributeError:
        return mapped_routes['Visitor'].position_view(positionId)
    except:
        flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
        flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
        session['redirect'] = url_for('v1pre_routes.position_view', positionId=positionId)
        return render_template('template.html')


@routes.route('/update', methods=['POST'])
def update_data():
    from flask import jsonify

    data = request.form['code']
    name = request.form['name']
    id = request.form['id']

    if name == 'company.name':
        if int(session['company_id']) == int(id):
            Company.query.filter(Company.id == id).update({'name': data})
            db.session.commit()
            session['company'] = data
            return jsonify({'value': data}), 200
        else:
            return jsonify({'position_id': Position.query.filter(Position.id == id).one().company_id, 'company_id': session['company_id'], 'status': 'You are not part of this company'}), 200
    elif name == 'company.description':
            if int(session['company_id']) == int(id):
                Company.query.filter(Company.id == id).update({'description': data})
                db.session.commit()
                return jsonify({'value': data}), 200
            else:
                return jsonify({'position_id': id, 'company_id': session['company_id'],
                                'status': 'You are not part of this company'}), 403

    elif name == 'company.contacts':
            if int(session['company_id']) == int(id):
                Company.query.filter(Company.id == id).update({'contacts': data})
                db.session.commit()
                return jsonify({'value': data}), 200
            else:
                return jsonify({'position_id': id, 'company_id': session['company_id'],
                                'status': 'You are not part of this company'}), 403

    elif name == 'position.name':
        if int(session['company_id']) == Position.query.filter(Position.id == id).one().company_id:
            Position.query.filter(Position.id == id).update({'name': data})
            db.session.commit()
            return jsonify({'value': data}), 200
        else:
            return jsonify({'position_id': id, 'company_id': session['company_id'], 'status': 'This position is not your company\'s'}), 403

    elif name == 'position.description':
        if int(session['company_id']) == Position.query.filter(Position.id == id).one().company_id:
            Position.query.filter(Position.id == id).update({'description': data})
            db.session.commit()
            return jsonify({'value': data}), 200
        else:
            return jsonify({'position_id': Position.query.filter(Position.id == id).one().company_id, 'company_id': session['company_id'], 'status': 'This position is not your company\'s'}), 403
    else:
        return jsonify({'status': 'data-name is not recognized'}), 400
