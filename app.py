import os
import pandas as pd

from flask import request, flash, url_for
from flask_login import login_required
from flask_migrate import Migrate
from flask_script import Manager
from flask_admin import Admin

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from werkzeug.utils import redirect

from flask_app_init import app, db

MIGRATION_DIR = os.path.join('admin', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and '.xlsx' in file.filename:
            try:
                df = pd.read_excel(file.filename, sheetname=0)
                for row in df['column name'].tolist():
                    invoice = Invoice(number=row[0], email=row[1])

                db.session.add(invoice)
                db.session.commit()

            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка чтения файла", "error")

    return redirect(url_for('admin/invoice'))


# FLASK-ADMIN
from models import User, Role, Invoice
from views import HomeAdminView, InvoiceView, LogoutView

admin = Admin(app, 'DME Parser', url='/admin', index_view=HomeAdminView(name='Load XLSX'))
admin.add_view(InvoiceView(Invoice, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='admin/logout_redirect'))

# FLASK-SECURITY
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
