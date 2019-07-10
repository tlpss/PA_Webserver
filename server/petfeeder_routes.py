from server import app, login, db
from flask_login import current_user, login_user, logout_user, login_required

from server.models import FeedMoment, FeederUsers, Feeder
from server.forms import PetFeederRegistrationForm, ValidationError, FeedMomentRegistrationForm
from flask import render_template, redirect, url_for, request, flash
from werkzeug.urls import url_parse


@app.route('/petfeeder')
@login_required
def petfeeder_index():
    return render_template('petfeeder_index.html',title= "petfeeder", feeders = current_user.feeders.all())


#TODO : this registration is for development purposes only!

@app.route('/petfeeder/new', methods = ["GET", "POST"])
@login_required
def add_petfeeder():
    form = PetFeederRegistrationForm()
    if form.validate_on_submit():
        feeder = Feeder.query.filter_by(name=form.name.data).first()
        if feeder is None:
            feeder = Feeder(name = form.name.data)
        elif current_user.feeders.filter_by(name= form.name.data).first() is not None:
            form.name.errors.append(ValidationError('feeder already linked'))
            return render_template('add_petfeeder.html', title="add feeder", form=form)
        current_user.feeders.append(feeder)
        db.session.commit()
        flash("registration finished")
        return redirect(url_for('petfeeder_index'))
    return render_template('add_petfeeder.html', title= "add feeder", form = form)


@app.route('/petfeeder/<id>')
@login_required
def petfeeder(id):
    feeder = Feeder.query.filter_by(id=id).first()
    if feeder is None:
        flash('feeder does not exist')
        return redirect(url_for('petfeeder_index',feeders = current_user.feeders.all() ))
    return render_template('petfeeder.html',feedmoments = feeder.feed_moments.order_by(FeedMoment.feed_time).all(), feeder = feeder )

@app.route('/petfeeder/<id>/add', methods = ["GET", "POST"])
@login_required
def add_feedmoment(id):
    feeder = Feeder.query.filter_by(id=id).first()

    form = FeedMomentRegistrationForm()
    if form.validate_on_submit():
        moment = FeedMoment(amount = form.amount.data)
        moment.setFeedTime(form.hour.data, form.minute.data)
        feeder.feed_moments.append(moment)
        db.session.commit()
        flash('moment added')
        return redirect( url_for('petfeeder', id = id))
    return render_template('add_feedmoment.html', form = form)

@app.route('/petfeeder/<id>/delete/<moment_id>')
@login_required
def delete_feedmoment(id , moment_id):
    moment = FeedMoment.query.filter_by(feedmoment_id = moment_id).first()
    if moment.Feeder.users.filter_by(id = current_user.id).first() is not None:
        print (moment)
        FeedMoment.query.filter_by(feedmoment_id = moment_id).delete()
        db.session.commit()
        flash ('removed')
        return redirect(url_for('petfeeder', id =id))
