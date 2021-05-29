import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Admin(Base):
    __tablename__ = "administrators"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String(128))

    clients = relationship("Client", back_populates="owner")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)

    owner_id = Column(Integer, ForeignKey(Admin.id), index=True)
    owner = relationship(Admin, back_populates="clients")
