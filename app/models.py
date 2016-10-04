# coding:utf-8
from . import db


class ClothesType(db.Model):
    __tablename__ = 'clothesType'
    id = db.Column(db.Integer, primary_key=True)
    typeName = db.Column(db.String(64), unique=True, index=True)
    remark = db.Column(db.Text())

    clothes = db.relationship('Clothes', backref='clothesType')

    def __repr__(self):
        return '<ClothesType %r>' % self.typeName


class Clothes(db.Model):
    __tablename__ = 'clothes'
    id = db.Column(db.Integer, primary_key=True)
    clothesName = db.Column(db.String(64), unique=True, index=True)
    remark = db.Column(db.Text())
    clothesTypeId = db.Column(db.Integer, db.ForeignKey('clothesType.id'))
    tags = db.relationship('Tag', secondary=clothesTag,
                           backref=db.backref("clothes", lazy='dynamic'),
                           lazy='dynamic')


clothesTag = db.Table('clothesTag',
                      db.Column('clothesId', db.Integer, db.ForeignKey('clothes.id')),
                      db.Column('tagId', db.Integer, db.ForeignKey('tag.id')), )


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tagName = db.Column(db.String(64), unique=True, index=True)
