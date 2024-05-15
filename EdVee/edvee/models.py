from datetime import datetime
from edvee import db, login_manager, app
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serialiser
import jwt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_profile.png')
    password = db.Column(db.String(50), nullable=False)
    projects = db.relationship('Project', backref='creator')
    project_accesses = db.relationship('Access', foreign_keys='Access.user_id', backref='access_user')
    collections = db.relationship('Collection', backref='creator')

    def get_reset_token(self):
        # s = Serialiser(app.config['SECRET_KEY'], expires_sec)
        # return s.dumps({'user_id': self.id}).decode('utf-8')
        encoded = jwt.encode({"user_id": self.id}, "secret", algorithm="HS256")
        return encoded

    @staticmethod
    def verify_reset_token(token):
        # s = Serialiser(app.config['SECRET_KEY'])
        # try:
        #     user_id = s.loads(token)['user_id']
        # except:
        #     return None
        user_id = jwt.decode(token, "secret", algorithms="HS256")['user_id']
        # print("user_id:", user_id)
        # return User.query.get(user_id['user_id'])
        return db.session.get(User, user_id['user_id'])

    def __repr__(self):
        return f"User({self.id}, '{self.name}', '{self.email}')"
    

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), default="Untitled Project", nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    elements = db.relationship('Element', foreign_keys='Element.project_id', backref='parent_project')
    connections = db.relationship('Connection', foreign_keys='Connection.project_id', backref='parent_project')
    project_accesses = db.relationship('Access', foreign_keys='Access.project_id', backref='access_project')

    def __repr__(self):
        return f"Project('{self.id}', '{self.name}', '{self.creator_id}')"


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    desc = db.Column(db.String(1000))
    # position = db.Column(db.Integer, nullable=False)
    element_type = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    connections1 = db.relationship('Connection', foreign_keys='Connection.element1', backref="parent_element1")
    connections2 = db.relationship('Connection', foreign_keys='Connection.element2', backref="parent_element2")

    def __repr__(self):
        # return f"Element('{self.id}', '{self.name}', '{self.element_type}', '{self.project_id}')"
        return f"\n(PROJECT-{self.project_id}, ID-{self.id}, {self.name}, TYPE{self.element_type})"


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    element1 = db.Column(db.Integer, db.ForeignKey('element.id'), nullable=False)
    element2 = db.Column(db.Integer, db.ForeignKey('element.id'), nullable=False)

    def __repr__(self):
        # return f"Connection('{self.id}', '{self.project_id}', '{self.element1}', '{self.element2}')"
        return f"\n(PROJECT{self.project_id}, {self.element1} -> {self.element2})"


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    elements_of_type = db.relationship('Element', foreign_keys='Element.element_type', backref='type_of_element')

    def __repr__(self):
        return f"ElementType('{self.id}', '{self.name}')"


class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    access_level = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"\n(PROJECT-{self.project_id}, USER-{self.user_id}, ACCESS LEVEL-{self.access_level})"


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    projects = db.relationship('Project', foreign_keys='Project.collection_id', backref='collection')

    def __repr__(self):
        return f"ElementType('{self.id}', '{self.name}', '{self.creator_id}')"
