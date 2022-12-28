import sqlite3
import bcrypt
from os.path import isfile


class WorksDB:
    def __init__(self, name='works.db'):
        self.name = name
        self.dbCreation()

    def addWork(self, workname, workform, worktype, images, rightansw, filepath):
        try:
            workid = self.cur.execute('SELECT workid FROM info ORDER BY workid DESC LIMIT 1').fetchone()[0]
            self.cur.execute(f'''CREATE TABLE IF NOT EXISTS "{workid + 1}" (
                imagepath TEXT UNIQUE NOT NULL,
                rightansw TEXT NOT NULL,
                filepath TEXT);''')
            while len(filepath) < len(images):
                filepath.append([])
            for i in range(len(images)):
                self.cur.execute(f'INSERT INTO "{workid + 1}" VALUES (?, ?, ?)', (images[i], rightansw[i], ';'.join(filepath[i])))
            self.cur.execute(f'INSERT INTO info VALUES (?, ?, ?, ?)', (workid + 1, workname, worktype, workform))
            self.db.commit()
            print(f'Work {workid + 1}:{workname} | Created successfully')
        except Exception as error:
            print(f'Work {workid + 1}:{workname} | Returned an error {error}')
    
    def delWork(self, workid):
        try:
            workname = self.cur.execute(f'SELECT workname FROM info WHERE workid="{workid}"').fetchone()[0]
            self.cur.execute(f'DELETE FROM info WHERE workid="{workid}"')
            self.cur.execute(f'DROP TABLE IF EXISTS "{workid}"')
            self.db.commit()

            users = DataDB().cur.execute('SELECT userid FROM students WHERE userid!="teacher"').fetchall()
            for x in users:
                DataDB().cur.execute(f'DROP TABLE IF EXISTS "{x[0]}-{workid}"')
            DataDB().delNewWorks(workid)
            DataDB().delDoneWorks(workid)
            DataDB().delInWorks(workid)
            
            print(f'Work {workid}:{workname} | Deleted successfully')
        except Exception as error:
            print(f'Work {workid} | Returned an error {error}')

    def getFormById(self, workid):
        return self.cur.execute(f'SELECT workform FROM info WHERE workid="{workid}"').fetchone()[0]

    def getTasks(self, workid):
        return [[x[0], x[1], x[2].split(';')] for x in self.cur.execute(f'SELECT imagepath,rightansw,filepath FROM "{workid}"').fetchall()]

    def getFormWorks(self, form):
        return self.cur.execute(f'SELECT workid,workname,worktype FROM info WHERE workform="{form}"').fetchall()

    def getWorks(self):
        return list(map(list, self.cur.execute('SELECT * FROM info').fetchall()[1:]))

    def dbCreation(self):
        self.db = sqlite3.connect(self.name, check_same_thread=False)
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS info (
            workid INT UNIQUE NOT NULL,
            workname TEXT NOT NULL,
            worktype TEXT NOT NULL,
            workform SMALLINT NOT NULL);''')
        if not self.cur.execute('SELECT workid FROM info').fetchone():
            self.cur.execute(f'INSERT INTO info VALUES (?, ?, ?, ?)', (0, 'NONE', 'NONE', 'NONE'))
        self.db.commit()


class DataDB:
    def __init__(self, name='data.db'):
        self.name = name
        self.dbCreation()

    def addStudent(self, userid, name, surname, form, password, newworks='', doneworks='', inprogress=''):
        try:
            password = passHashing(password)
            self.cur.execute(f'''INSERT INTO students VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?)''', (userid, name, surname, form, newworks, doneworks, inprogress, password))
            if not self.cur.execute(f'SELECT number,letter FROM forms WHERE number="{form[:-1]}" AND letter="{form[-1]}"').fetchone():
                self.cur.execute(f'INSERT INTO forms VALUES (?, ?, ?)', (form[:-1], form[-1], userid))
            else:
                stud = self.cur.execute(f'SELECT list FROM forms WHERE number="{form[:-1]}" AND letter="{form[-1]}"').fetchone()[0]
                self.cur.execute(f'UPDATE forms SET list="{stud},{userid}" WHERE number="{form[:-1]}" AND letter="{form[-1]}"')
            self.db.commit()
            print(f'Student {userid}:{name}-{surname} | Student created successfully')
        except Exception as error:
            print(f'Student {userid}:{name}-{surname} | Returned an error while student creation')

    def checkStudent(self, userid):
        return str(userid) in [x[0] for x in self.cur.execute('SELECT userid FROM students')]

    def delStudent(self, userid):
        if userid == 'teacher' or userid not in [x[0] for x in self.cur.execute('SELECT userid FROM students').fetchall()]:
            return
        form = self.cur.execute(f'SELECT form FROM students WHERE userid="{userid}"').fetchone()[0]
        self.cur.execute(f'DELETE FROM students WHERE userid="{userid}"')
        lst = self.cur.execute(f'SELECT list FROM forms WHERE list LIKE "%{userid}%"').fetchone()
        self.cur.execute(f'UPDATE forms SET list="{",".join([x for x in lst[0].split(",") if x != userid])}" WHERE number="{form[:-1]}" AND letter="{form[-1]}"')
        for workid in [x[0] for x in WorksDB().cur.execute('SELECT workid FROM info').fetchall() if x]:
            self.cur.execute(f'DROP TABLE IF EXISTS "{userid}-{workid}"')
        self.db.commit()

    def getStudents(self):
        return self.cur.execute('SELECT userid,name,surname,form FROM students WHERE userid != "teacher"').fetchall()

    def delNewWorks(self, workid):
        newworks = self.cur.execute('SELECT userid,newworks FROM students').fetchall()
        for x in newworks:
            newset = ",".join(list(filter(lambda y: y != str(workid), x[1].split(","))))
            self.cur.execute(f'UPDATE students SET newworks="{newset}" WHERE userid="{x[0]}"')
            self.db.commit()
    
    def delDoneWorks(self, workid):
        doneworks = self.cur.execute('SELECT userid,doneworks FROM students').fetchall()
        for x in doneworks:
            newset = ",".join(list(filter(lambda y: y.split(':')[0] != str(workid), x[1].split(","))))
            self.cur.execute(f'UPDATE students SET doneworks="{newset}" WHERE userid="{x[0]}"')
            self.db.commit()
    
    def delInWorks(self, workid):
        inworks = self.cur.execute('SELECT userid,inprogress FROM students').fetchall()
        for x in inworks:
            newset = ",".join(list(filter(lambda y: y.split(':')[0] != str(workid), x[1].split(","))))
            self.cur.execute(f'UPDATE students SET inprogress="{newset}" WHERE userid="{x[0]}"')
            self.db.commit()


    def getFullFormStudents(self, form):
        number, letter = form[:-1], form[-1]
        students = self.cur.execute(f'SELECT list FROM forms WHERE number="{number}" AND letter="{letter}"').fetchone()
        if not students:
            print(f'Students of {form} form | 0 students')
            return (None, [None])
        try:
            students = (form, students[0].split(','))
            print(f'Students of {form} form | Returned successfully')
            return students
        except Exception as error:
            print(f'Students of {form} form | Returned an error {error}')
            return
    
    def getNumFormStudents(self, form):
        return self.cur.execute(f'SELECT userid,name,surname,form FROM students WHERE FORM LIKE {form}_').fetchall()
    
    def addStudTaskTable(self, userid, workid):
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS "{userid}-{workid}" (
            taskid INT UNIQUE NOT NULL,
            answer TEXT NOT NULL,
            status SMALLINT NOT NULL);''')
        self.db.commit()
    
    def getInWorksTasks(self, userid, workid):
        return [list(x) for x in self.cur.execute(f'SELECT answer,status FROM "{userid}-{workid}"').fetchall()]

    def changeInAnsw(self, userid, workid, taskid, answer, status):
        self.cur.execute(f'UPDATE "{userid}-{workid}" SET answer="{answer}",status="{status}" WHERE taskid="{taskid}"')
        self.db.commit()

    def addInAnsw(self, userid, workid, taskid, answer, status):
        try:
            self.cur.execute(f'INSERT INTO "{userid}-{workid}" VALUES (?, ?, ?)', (taskid, answer, status))
            self.db.commit()
            print(f'User {userid} saved answer on {workid}:{taskid} successfully')
        except Exception as error:
            print(f'User {userid} returned an error while saving answer on {workid}:{taskid}')

    def getNumFormStudents(self, number):
        students = self.cur.execute('SELECT userid,name,surname,form FROM students').fetchall()
        return list(filter(lambda x: str(number) == x[3][:-1], students))

    def addNewWork(self, workid, studentsid):
        try:
            for userid in studentsid:
                self.addStudTaskTable(userid, workid)
                for x in range(len(WorksDB().cur.execute(f'SELECT * from "{workid}"').fetchall())):
                    self.addInAnsw(userid, workid, x, '', 0)
                newworks = self.cur.execute(f'SELECT newworks FROM students where userid="{userid}"').fetchone()[0]
                if not newworks:
                    self.cur.execute(f'UPDATE students SET newworks="{workid}" WHERE userid="{userid}"')
                else:
                    self.cur.execute(f'UPDATE students SET newworks="{newworks},{workid}" WHERE userid="{userid}"')
            self.db.commit()
            workname = WorksDB().cur.execute(f'SELECT workname FROM info WHERE workid="{workid}"').fetchone()[0]
            print(f'Work {workid}:{workname} | Distributed successfully')
        except Exception as error:
            print(f'Work {workid}:{workname} | Returned an error {error} while distribution')

    def fromNewToIn(self, userid, workid, result=0):
        try:
            inprogress = self.cur.execute(f'SELECT inprogress FROM students where userid="{userid}"').fetchone()[0]
            if not inprogress:
                self.cur.execute(f'UPDATE students SET inprogress="{workid}:{result}," WHERE userid="{userid}"')
            else:
                self.cur.execute(f'UPDATE students SET inprogress="{inprogress}{workid}:{result}," WHERE userid="{userid}"')
            self.db.commit()
            workname = WorksDB().cur.execute(f'SELECT workname FROM info WHERE workid="{workid}"').fetchone()[0]
            user = self.cur.execute(f'SELECT name,surname FROM students WHERE userid="{userid}"').fetchone()
            self.delNewWork(userid, workid)
            self.addStudTaskTable(userid, workid)
            print(f'Work {workid}:{workname} | Started by {userid}:{user[0]}-{user[1]}')
        except Exception as error:
            print(f'Work {workid}:{workname} | Returned an error {error} when {userid}:{user[0]}-{user[1]} start it')

    def delNewWork(self, userid, workid):
        newworks = self.cur.execute(f'SELECT newworks FROM students WHERE userid="{userid}"').fetchone()[0]
        if newworks:
            newworks = newworks.split(',')
            newworks.remove(str(workid))
            newworks = ','.join(newworks)
        self.cur.execute(f'UPDATE students SET newworks="{newworks}" WHERE userid="{userid}"')
        self.db.commit()
    
    def changeInProgress(self, userid, workid, progress):
        inprogress = self.cur.execute(f'SELECT inprogress FROM students WHERE userid="{userid}"').fetchone()[0].split(',')
        for x in range(len(inprogress)):
            if inprogress[x].split(':')[0] == str(workid):
                inprogress[x] = f'{inprogress[x].split(":")[0]}:{progress}'
        self.cur.execute(f'UPDATE students SET inprogress="{",".join(inprogress)}" WHERE userid="{userid}"')
        self.db.commit()

    def fromInToDone(self, userid, workid):
        try:
            if not self.getInWorks(userid):
                return
            result = [x[1] for x in self.getInWorks(userid) if x[0] == int(workid)][0]
            doneworks = self.cur.execute(f'SELECT doneworks FROM students where userid="{userid}"').fetchone()[0]
            if not doneworks:
                self.cur.execute(f'UPDATE students SET doneworks="{workid}:{result}," WHERE userid="{userid}"')
            else:
                self.cur.execute(f'UPDATE students SET doneworks="{doneworks}{workid}:{result}," WHERE userid="{userid}"')
            self.db.commit()
            workname = WorksDB().cur.execute(f'SELECT workname FROM info WHERE workid="{workid}"').fetchone()[0]
            user = self.cur.execute(f'SELECT name,surname FROM students WHERE userid="{userid}"').fetchone()
            self.delInWork(workid, userid)
            print(f'Work {workid}:{workname} | Done by {userid}:{user[0]}-{user[1]}')
        except Exception as error:
            print(f'Work {workid}:{workname} | Returned an error {error} when {userid}:{user[0]}-{user[1]} start it')

    def delInWork(self, workid, userid):
        inprogress = self.cur.execute(f'SELECT inprogress FROM students WHERE userid="{userid}"').fetchone()[0]    
        if inprogress:
            inprogress = inprogress.split(',')
            for x in inprogress:
                if f'{str(workid)}:' in x:
                    inprogress.remove(x)
            inprogress = ','.join(inprogress)
        self.cur.execute(f'UPDATE students SET inprogress="{inprogress}" WHERE userid="{userid}"')
        self.db.commit()

    def getNewWorks(self, userid):
        newworks = self.cur.execute(f'SELECT newworks FROM students WHERE userid="{userid}"').fetchone()
        out = []
        if newworks:
            for i in filter(lambda x: x, set(newworks[0].split(','))):
                out.append([int(i)] + list(WorksDB().cur.execute(f'SELECT worktype,workname FROM info WHERE workid="{i}"').fetchone()))
        return out

    def getDoneWorks(self, userid):
        doneworks = self.cur.execute(f'SELECT doneworks FROM students WHERE userid="{userid}"').fetchone()
        if doneworks:
            return [[int(i) for i in x.split(':')]  + list(WorksDB().cur.execute(f'SELECT worktype,workname FROM info WHERE workid="{x.split(":")[0]}"').fetchone()) for x in set(doneworks[0].split(',')) if x]
        return

    def getInWorks(self, userid):
        inworks = self.cur.execute(f'SELECT inprogress FROM students WHERE userid="{userid}"').fetchone()
        if inworks:
            return [[int(i) for i in x.split(':')] + list(WorksDB().cur.execute(f'SELECT worktype,workname FROM info WHERE workid="{x.split(":")[0]}"').fetchone()) for x in set(inworks[0].split(',')) if x]
        return

    def getDoneStud(self, workid):
        output = []
        students = self.cur.execute('SELECT userid,name,surname,form,doneworks FROM students').fetchall()
        students = map(list, filter(lambda x: str(workid) in map(lambda y: y.split(':')[0], x[4].split(',')), students))
        for student in students:
            for work in student[4].split(','):
                if work.split(':')[0] == str(workid):
                    output.append(student[0:4] + [work.split(':')])
                    break
        return output
    
    def getInStud(self, workid):
        output = []
        students = self.cur.execute('SELECT userid,name,surname,form,inprogress FROM students').fetchall()
        students = map(list, filter(lambda x: str(workid) in map(lambda y: y.split(':')[0], x[4].split(',')), students))
        for student in students:
            for work in student[4].split(','):
                if work.split(':')[0] == str(workid):
                    output.append(student[:4] + [work.split(':')])
                    break
        return [list(x) for x in output]
    
    def getNewStud(self, workid):
        output = []
        students = self.cur.execute('SELECT userid,name,surname,form,newworks FROM students').fetchall()
        for student in students:
            if student[4] == str(workid):
                output.append(student[:4])
        return [list(x) for x in output]
    
    def getStudentsOfWork(self, workid):
        return [self.getNewStud(workid), self.getDoneStud(workid), self.getInStud(workid)]

    def getHashedPass(self, userid):
        return self.cur.execute(f'SELECT password FROM students WHERE userid="{userid}"').fetchone()[0]
    
    def checkPass(self, userid, password):
        return checkPassword(password, self.getHashedPass(userid))
    
    def dbCreation(self):
        self.db = sqlite3.connect(self.name, check_same_thread=False)
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS students (
            userid TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            form TEXT NOT NULL,
            newworks TEXT,
            doneworks TEXT,
            inprogress TEXT,
            password TEXT);''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS forms (
            number SMALLINT,
            letter VARCHAR(1),
            list TEXT);''')
        self.db.commit()

def passHashing(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def checkPassword(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)


if __name__ == '__main__':
    a = WorksDB()
    b = DataDB()
    # a.delWork(1)
    # print(a.getTasks(3))
    # print(b.getStudents())
    # b.addStudent('teacher', 'Учитель', 'Учительский', '99卐', 'Fox')
    # a.addWork('Тест 1', 10, 'ТЕСТ', ['/STATIC/Tasks/t0e0.jpg', '/STATIC/Tasks/t0e1.jpg', '/STATIC/Tasks/t0e2.jpg'], [1, 2, 3])
    # a.addWork('Контрольная 1', 10, 'КОНТРОЛЬНАЯ', ['/STATIC/Tasks/t0e0.jpg', '/STATIC/Tasks/t0e1.jpg', '/STATIC/Tasks/t0e2.jpg'], [1, 2, 3], [['path1', 'path2'], [], ['path3']])
    # b.addStudent('deniskairiska', 'Дмитрий', 'Суперский', '10И', 'kek')
    # b.addStudent('supernagibatel', 'Кирилл', 'Мефодьевич', '10И', 'kek1')
    # b.addNewWork(3, ['deniskairiska', 'supernagibatel'])
    # b.fromInToDone('deniskairiska', 1)
    # b.fromInToDone('supernagibatel', 1)
    # b.addNewWork(2, ['supernagibatel'])
    # b.fromNewToIn('deniskairiska', 1)
    # b.delInWork(1, 'deniskairiska')
    # b.addInAnsw('deniskairiska', 1, 1, 1, 2)
    # b.fromInToDone('deniskairiska', '1')
    # print(b.getNewWorks('supernagibatel'))
    # print(b.getStudentsOfWork(2))
    # b.addNewWork(1, ['supernagibatel'])
    # print(b.getDoneStud(1))
    # <id>:<progress>:[39820卐0卍25493卐1卍3523452卐2]
    # b.delStudent('supernagibatel')