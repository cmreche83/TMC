# -*- coding: utf-8 -*-
from datetime import date
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

#from sqlalchemy import Computed
from sqlalchemy import create_engine
from sqlalchemy import select
#from sqlalchemy.orm import column_property
#from sqlalchemy.orm import deferred

from sqlalchemy import String as sql_string
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker


def calculateAge(birthDate:str = "")->int:
    """
    Calculates the age of a person from his date of birth passed as a string dd-mm-yyyy
    """
    if len(birthDate) >= 10:
        age = date.today().year - int(birthDate[-4:])
        extra = int(birthDate[:2]+birthDate[3:5]) - int(f"{date.today().day:02}{date.today().month:02}")
        if extra > 0:
            age = age - 1
        return age
    else:
        return 0

class Base(DeclarativeBase):
    pass

# this is the User dataclass
class User(Base):
     __tablename__ = "user"
    
    # Left ugly comments here to show that I looked into the path of having age computed by the DB itself (generated column)
    # that idea does not work since we can only do it with immutable functions while time is anything but immutable
    
     id: Mapped[int] = mapped_column(primary_key=True)
     firstname: Mapped[str] = mapped_column(sql_string(30))
     lastname: Mapped[str] = mapped_column(sql_string(30))
     #age:Mapped[int] = mapped_column(sql_integer, init=False) #Computed("id*id"),
     date_of_birth: Mapped[str] = mapped_column(sql_string(10))
     #-----date_of_birth: Mapped[date] = mapped_column(sql_date)
     #age: Mapped[int] = mapped_column(Computed("floor(datediff(day,@date_of_birth,@today) / 365.2425)"))
     ##### --- age: Mapped[int] = mapped_column(Computed("FLOOR(date_of_birth - CURRENT_DATE) / 365.2425"))
     #age:int = calculateAge(date_of_birth)
     #age: Mapped[int] = deferred(calculateAge(date_of_birth))
     #age: column_property(calculateAge(str(date_of_birth)))
     #age: column_property(floor(datediff(day,@birthdate,@today) / 365.2425))
     

     def __repr__(self) -> str:
         usr = f"User\nid={self.id!r}\n firstname={self.firstname!r}\n lastname={self.lastname!r}\nage={self.age!r}\ndate_of_birth={self.date_of_birth!r}"
         return usr

# this is the user response dataclass ( used only so that pydantic can validate )
class UserResponse(BaseModel):
    firstname: str
    lastname: str
    date_of_birth: str
    
# initialisation of the connection with the database here
user = "admin"
password = "password"
hostname = "db"
database_name = "TestDB"
service_port = 5432
sql_engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{hostname}:{service_port}/{database_name}', echo=False)
Session = sessionmaker(sql_engine)
Base.metadata.create_all(sql_engine)

# initialisation of FastAPI ( we will need its descriptors beyond this point )
app = FastAPI(debug=False)
origins = ["*"]
# to mitigate CORS issue ... added this middleware
# however after extended testing CORS is still not handled as well as I wish
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

# List Users ( to display the table in the web interface )
@app.get(path="/users")
def get_users():
    results = []
    with Session.begin() as session:
        try:
            for row in session.execute(select(User).order_by(User.id)):
                results.append({"id":row.User.id, 
                                "firstname":row.User.firstname, 
                                "lastname":row.User.lastname, 
                                "date_of_birth":row.User.date_of_birth, 
                                "age":calculateAge(row.User.date_of_birth)
                                })
        except Exception as e:
            session.rollback()
            print(f"Failed to query Users: {e}")
        else:
            session.commit()
            session.close()
    return results
            
# Create new users
@app.post(path="/users/create")
def add_user(new_user: UserResponse):
    #with Session(sql_engine) as session, session.begin():
    with Session.begin() as session:
        #        #stmt = session.scalars(insert(User).values(firstname=new_user.firstname, lastname=new_user.lastname, date_of_birth=new_user.date_of_birth)).returning(User)
        #        #print(dir(session))
        #        #return stmt
        try:
            session.add(User(firstname=new_user.firstname, lastname=new_user.lastname, date_of_birth=new_user.date_of_birth))
        except Exception as e:
            session.rollback()
            print(f"Failed to add this User: {e}")
        else:
            session.commit()
            session.close()
    return new_user

# Delete Users ( - ) Button in the table in the web interface
@app.delete(path="/user/{user_id}")
def delete_user(user_id: int):
    print(f"DEL user {user_id}")
    #with Session(sql_engine) as session, session.begin():
    with Session.begin() as session:
        try:
            ghost = session.query(User).filter(User.id == user_id).one()
            session.delete(ghost)
        except Exception as e:
            session.rollback()
            session.close()
            return {"message": f"Failed to remove User with id {user_id}: {e}"}
        else:
            session.commit()
            session.close()
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)