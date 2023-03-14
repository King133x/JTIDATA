from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class FilterForm(FlaskForm):
    id = StringField('ID')
    AN = StringField('AN')
    Model = StringField('Model')
    SN = StringField('SN')
    NOM = StringField('NOM')
    LOC = StringField('LOC')
    CAL_DATE = StringField('CAL DATE')
    DUE = StringField('DUE')
    CYCLE = StringField('CYCLE')
    MANUFACTURE = StringField('MANUFACTURE')
    PROC = StringField('PROC')
    SPECIAL_CAL = StringField('SPECIAL CAL')
    NOTE = StringField('NOTE')
    COST = StringField('COST')
    STANDARD = StringField('STANDARD')
    Facility = StringField('Facility')
    submit = SubmitField('Search')

class EditRecordForm(FlaskForm):
    AN = StringField('AN')
    Model = StringField('Model')
    SN = StringField('SN')
    NOM = StringField('NOM')
    LOC = StringField('LOC')
    CAL_DATE = StringField('CAL DATE')
    DUE = StringField('DUE')
    CYCLE = StringField('CYCLE')
    MANUFACTURE = StringField('MANUFACTURE')
    PROC = StringField('PROC')
    SPECIAL_CAL = StringField('SPECIAL CAL')
    NOTE = StringField('NOTE')
    COST = StringField('COST')
    STANDARD = StringField('STANDARD')
    Facility = StringField('Facility')
    submit = SubmitField('Update')