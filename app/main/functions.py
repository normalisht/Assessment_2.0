from app import db
from app.models import User, Expert, Viewer, Admin, Parameter
from sqlalchemy import create_engine


def users_in_json(users):
    string = '['
    for user in users:

        if user.birthday:
            birthday = user.birthday.strftime('%d.%m.%Y')
        else:
            birthday = '-'
        string += '{' + '"id":{0},"username":"{1}","birthday":"{2}","team":"{3}",' \
                        '"project_number":{4}, "project_id":{5},' \
            .format(str(user.id),
                    str(user.username),
                    str(birthday),
                    str(user.team),
                    str(user.project_number),
                    str(user.project_id))

        for i in range(5):
            string += '"sum_grade_{0}":"{1}",' \
                .format(i, str(user.__dict__['sum_grade_{}'.format(i)]))

        string += '"sum_grade_all":"{0}"'.format(str(user.sum_grade_all)) + '},'
    string = string[:len(string) - 1] + ']'
    return string


def experts_in_json(experts):
    string = '['

    for expert in experts:
        string += '{' + '"id":{0},"username":"{1}","weight":"{2}","quantity":"{3}},' \
                        '"project_number":{4}, "project_id":{5},'.format(str(expert.id),
                                                                         str(expert.username),
                                                                         str(expert.weight),
                                                                         str(expert.quantity),
                                                                         str(expert.project_number),
                                                                         str(expert.project_id)) + '},'

    string = string[:len(string) - 1] + ']'

    return string


def grades_in_json(grades):
    string = '['
    for grade in grades:
        string += '{' + '"id":{0},"date":"{1}","expert_id":"{2}","user_id":"{3}",' \
                        '"comment":"{4}"'.format(str(grade.id),
                                                 str(grade.date.strftime('%H:%M %d.%m.%y')),
                                                 str(grade.expert_id),
                                                 str(grade.user_id),
                                                 str(grade.comment))

        for i in range(5):
            string += ',"parameter_{0}":"{1}"' \
                .format(i, str(grade.__dict__['parameter_{}'.format(i)]))

        string += '},'

    string = string[:len(string) - 1] + ']'

    return string

def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


def delete(Model):
    try:
        x = db.session.query(Model).delete()
        db.session.commit()
    except:
        db.session.rollback()


def excel(filename):
    df = pd.read_excel(filename)
    engine = create_engine("sqlite:///T_park.db")
    df.head
    if filename == 'user':
        delete(User)
        df.columns = ['id', 'username', 'email', 'avatar', 'password_hash', 'birth_date', 'team']
        df.to_sql(filename, con=engine, if_exists='append', index=False)
    elif filename == 'admin':
        delete(Admin)
        df.columns = ['admin_id', 'username', 'email']
        df.to_sql(filename, con=engine, if_exists='append', index=False)
    elif filename == 'expert':
        delete(Expert)
        df.columns = ['id', 'username', 'email', 'weight', 'quantity']
        df.to_sql(filename, con=engine, if_exists='append', index=False)
    elif filename == 'viewer':
        delete(Viewer)
        df.columns = ['id', 'username', 'email']
        df.to_sql(filename, con=engine, if_exists='append', index=False)
    else:
        print('123')