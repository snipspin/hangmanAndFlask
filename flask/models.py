from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gamedb'
db = SQLAlchemy(app)

class Publisher(db.Model):
  __tablename__ = 'publishers'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)

  games = db.relationship('Game', backref='creator', lazy=True)

  def __repr__(self):
    return f'Player(id={self.id}, name="{self.name}")'
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
  

game_genres = db.Table('game_genres',
  db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
  db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)

# from models import Publisher
# publisherer = [Publisher(name='Ubisoft')]
# publisherer.append(Publisher(name='Nintendo'))
# publisherer.append(Publisher(name='Activision'))
# publisherer.append(Publisher(name='Valve'))

class Game(db.Model):
  __tablename__ = 'games'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150), unique=True, nullable=False)
  publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id', ondelete='SET NULL'))

  genres = db.relationship('Genre',
    secondary=game_genres,
    lazy='subquery',
    backref=db.backref('games', lazy=True)
  )

  def __repr__(self):
    return f'Game(id={self.id}, name="{self.name}", publisher_id={self.publisher_id})'

  def as_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'creator': self.creator.as_dict()['name'],
    }

# db.session.add(Game(name='Watch Dogs', publisher_id=Publisher.query.filter_by(name="Ubisoft").one().id))
# db.session.add(Game(name='Animal Crossing: New Horizons', publisher_id=Publisher.query.filter_by(name="Nintendo").one().id))
# db.session.add(Game(name='Call of Duty: Modern Warfare', publisher_id=Publisher.query.filter_by(name="Activision").one().id))
# db.session.add(Game(name='Half-Life: Alyx', publisher_id=Publisher.query.filter_by(name="Valve").one().id))

class Genre(db.Model):
  __tablename__ = 'genres'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)

  def __repr__(self):
    return f'Tag(id={self.id}, name="{self.name}")'
  
  def as_dict(self):
    return {'id': self.id, 'name': self.name}

# from models import Genre
# games = Game.query.all()
# games[0].genres += [Genre(name='Action-Adventure')]
# games[1].genres += [Genre(name='Soziale Simulation')]
# games[2].genres += [Genre(name='Ego-Shooter')]
# games[3].genres += [Genre(name='Virtual-Reality'), Genre(name='Ego-Shooter')]

def get_or_create(model, defaults=None, **kwargs):
  instance = db.session.query(model).filter_by(**kwargs).first()
  if instance:
    return instance, False
  else:
    params = dict((k, v) for k, v in kwargs.items())
    params.update(defaults or {})
    instance = model(**params)
    db.session.add(instance)
    db.session.commit()
    return instance, True


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gamedb'
# db = SQLAlchemy(app)



# class Player(db.Model):
    
#     __tablename__ = 'players'
    
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String, unique=True, nullable=False)
#     name = db.Column(db.String,unique=True, nullable=False)

#     def __repr__(self):
#         return f'💸💸💸Player(id={self.id}, email="{self.email}", name="{self.name}")'

#     def as_dict(self):
#         return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# game_genres = db.Table('game_genres',
# db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
# db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True))


# # from models import Player
# # players = [Player(name='Mausschubser', email='mausschubser@example.com')]
# # players.append = [Player(name='Konsolero', email='konsolero@example.com')]
# # players.append = [Player(name='Joystickkiller', email='joystickkiller@example.com')]
# # players.append = [Player(name='Mauskiller', email='mauskiller@example.com')]


# class Game(db.Model):
    
#     __tablename__ = 'games'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String,unique=True, nullable=False)
#     publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id', ondelete='SET NULL'))
    
#     genres = db.relationship('Genre', 
#     secondary=game_genres, 
#     lazy='subquery',
#     backref=db.backref('games', lazy=True))

#     def __repr__(self):
#         return f'🎲🎮🕹Game(id={self.id}, name="{self.name}", publisher="{self.publisher_id}")'

#     def as_dict(self):
#         return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# class Publisher(db.Model):
#     __tablename__ = 'publishers'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)

#     games = db.relationship('Game',
#     backref=db.backref('publisher', lazy=True)
#     lazy=True)
    
#     def __repr__(self):
#         return f'💰💰💰Publisher(id={self.id}, name="{self.name}")'
    
#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# class Genre(db.Model):
#     __tablename__ = 'genres'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
    
#     def __repr__(self):
#         return f'🤪🤪🤪Genre(id={self.id}, name="{self.name}")'
    
#     def as_dict(self):
#         return {'id': self.id, 'name': self.name}

# def get_or_create(model, defaults=None, **kwargs):
#   instance = db.session.query(model).filter_by(**kwargs).first()
#   if instance:
#     return instance, False
#   else:
#     params = dict((k, v) for k, v in kwargs.items())
#     params.update(defaults or {})
#     instance = model(**params)
#     db.session.add(instance)
#     db.session.commit()
#     return instance, True