from app import render_template, flash
from app.models import User, Tag, Company, Position, Application, insert_position
from flask import session, request,redirect,url_for


class Companies:

	@staticmethod
	def homepage():
		return render_template('company/homepage.html', positions=Position.query.filter(Position.company_id == session['company_id']).filter(Position.available	== True).order_by(Position.id.desc()).limit(5))

	@staticmethod
	def create_offer():
		id = insert_position('', session['company_id'], '', True, 0, 0, '', 1)
		return redirect(url_for('v1pre_routes.position_view', positionId=id))

	@staticmethod
	def browse_students():
		page = int(request.args.get('page', default='0'))
		offers_per_page = 10
		position = -2

		if request.form.get('position'):
			position = int(request.form.get('position')) - 1

		if position == -2:
			return render_template('company/browse_students.html',
									positions=Position.query.filter(Position.company_id == int(session['company_id'])),
									students=Application.query.filter(Application.company_id == int(session['company_id'])))
		else:
			return render_template('company/browse_students.html',
									positions=Position.query.filter(Position.company_id == int(session['company_id'])),
									students=Application.query.filter(Application.company_id == int(session['company_id']) and
																	  Application.position_id == position))

	@staticmethod
	def my_offers():
		return render_template('company/my_offers.html',
							   positions=Position.query.filter(Position.company_id == int(session['company_id'])))

	@staticmethod
	def application_view(applicationId):
		application = Application.query.filter(Application.id==applicationId).one()
		if application.company_id != session['company_id']:
			flash('Тази кандидатура не е по обява на Вашата фирма.', 'danger')
			return render_template('template.html')
		return render_template('company/application.html', application=application)

	@staticmethod
	def company_view(companyId):
		company = Company.query.filter(Company.id == companyId)[0]
		if companyId == session['company_id']:
			return render_template('company/company.html', company=company)
		else:
			return render_template('students/company.html', company=company)

	@staticmethod
	def sector_view(sectorId):
		return render_template('students/sector.html', sector=Sector.query.filter(Sector.id == sectorId)[0], companies=Company.query.filter(Company.sector_id == sectorId).all())

	@staticmethod
	def position_view(positionId):
		position = Position.query.filter(Position.id == positionId)[0]
		if position.company_id == session['company_id']:
			return render_template('company/position.html', position=position, tags=Tag.query.all())
		else:
			return render_template('students/position.html', position=position, tags=Tag.query.all())

	@staticmethod
	def profile():
		company = Company.query.filter(Company.id == session['company_id'])[0]
		return render_template('company/profile.html', company=company)
