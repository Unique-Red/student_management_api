from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"{self.name} has email {self.email}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_all(cls):
        return cls.query.all()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    matric_number = db.Column(db.String(120), nullable=False)
    gpa = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('students', lazy=True))
    

    def __repr__(self):
        return f"{self.first_name} has email {self.email}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_all(cls):
        return cls.query.all()

class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(80), nullable=False)
    course_title = db.Column(db.String(120), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    lecturer = db.Column(db.String(120), nullable=False)
    students = db.relationship('Student', secondary='courses_registered', backref=db.backref('courses', lazy='dynamic'))
    courses_registered = db.relationship('CourseRegistered', backref='courses', lazy=True)
    registered_students = db.relationship('Student', secondary='courses_registered', backref=db.backref('registered_courses', lazy='dynamic'))

    def __repr__(self):
        return f"{self.course_code} is taken by {self.lecturer}"

class CourseRegistered(db.Model):
    __tablename__ = 'courses_registered'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    def __repr__(self):
        return f"{self.student_id} has course {self.course_id}"


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('admin', lazy=True))

    def __repr__(self):
        return f"{self.first_name} has email {self.email}"

