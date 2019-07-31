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
        feeder = Feeder.query.filter_by(secret_key = form.secret_key.data).first()
        if feeder is None:
            feeder = Feeder.query.filter_by(name = form.name.data).first()
            if feeder is None:
                new_feeder = Feeder(name =form.name.data, secret_key= form.secret_key.data)
                db.session.add(new_feeder)
                current_user.feeders.append(new_feeder)
                flash('new feeder created')
                db.session.commit()
                return redirect(url_for('petfeeder_index'))
            else:
                form.name.errors.append(ValidationError('name unavailable'))
        elif current_user.feeders.filter_by(name= form.name.data).first() is not None:
            form.name.errors.append(ValidationError('feeder already linked to your account'))
            return render_template('add_petfeeder.html', title="add feeder", form=form)
        else:
            if not feeder.name == form.name.data:
                form.name.errors.append(ValidationError("feeder in use with different name"))
            else:
                current_user.feeders.append(feeder)
                flash("existing feeder added to your account")
                db.session.commit()
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
    #TODO: in order to make the system work: at removal next moment's update time must be set to removal time!
    moment = FeedMoment.query.filter_by(feedmoment_id = moment_id).first()
    if moment.Feeder.users.filter_by(id = current_user.id).first() is not None:
        print (moment)
        FeedMoment.query.filter_by(feedmoment_id = moment_id).delete()
        db.session.commit()
        flash ('removed')
        return redirect(url_for('petfeeder', id =id))

@app.route('/petfeeder/api<hash>')
def api(hash):
    feeder = Feeder.get_feeder_from_hash(hash)
    if not feeder is None:
        time = request.args.get('last_update')
        feedmoment = feeder.get_next_moment()
        moment_time = feedmoment.last_updated
        if moment_time > time:
            #TODO: return encrypted feedmoments with last updated between last updated of next feedmoment and "update-moment" of request
            pass
        else:
            #TODO: return encrypted "up to date" signal
            pass

