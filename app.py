import os
import pandas as pd

from flask import request, flash, url_for, redirect
from flask_login import login_required
from flask_migrate import Migrate
# from flask_script import Manager
from flask_admin import Admin

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

from flask_app_init import app, db

MIGRATION_DIR = os.path.join('admin', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)


# manager = Manager(app)


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and '.xlsx' in file.filename:
            file.save(file.filename)
            try:
                df = pd.read_excel(file.filename)
                df.to_csv("table.csv", index=None, header=True, sep=';', na_rep='-')
                with open('table.csv', 'r', encoding='utf-8') as f:
                    for row in f:
                        print(row)
                        row = row.split(';')
                        invoice = Invoice.query.filter_by(number=row[0]).first()
                        if invoice:
                            invoice.email += f' {row[1]}'
                            invoice.place += f' {row[2].replace(".0", "")}'
                            invoice.weight += f' {row[3]}'
                        else:
                            if len(row) < 3 or 'unnamed' in invoice.place.lower():
                                invoice = Invoice(
                                    number=row[0],
                                    email=row[1]
                                )
                            else:
                                invoice = Invoice(
                                    number=row[0],
                                    email=row[1],
                                    place=row[2].replace(".0", ""),
                                    weight=row[3]
                                )

                            db.session.add(invoice)
                        db.session.commit()
                flash("Файл загружен")

                os.remove(file.filename)
                os.remove('table.csv')

            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка чтения файла", "error")

    return redirect(url_for('admin.index'))


# FLASK-ADMIN
from models import User, Role, Invoice
from views import HomeAdminView, InvoiceView, LogoutView

admin = Admin(app, 'DME Parser', url='/admin', index_view=HomeAdminView(name='Load XLSX'))
admin.add_view(InvoiceView(Invoice, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='admin/logout_redirect'))

# FLASK-SECURITY
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
