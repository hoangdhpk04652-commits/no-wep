from app import db

class User(db.Model):
    __tablename__ = 'nhanvien' # Tên bảng thực tế trong PostgreSQL của bạn
    
    manv = db.Column(db.Integer, primary_key=True)
    tennv = db.Column(db.String(50), nullable=False)
    luong = db.Column(db.Integer,  nullable=False)