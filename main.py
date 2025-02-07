from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel


app = FastAPI()


class Student(BaseModel):
    """
    Schema of Student model.
    """

    name: str
    age: int
    class_: str

# the database is a dictionary of Student objects
students = {
    1: Student(name="John", age=17, class_="year 25"),
    2: Student(name="Paul", age=17, class_="year 26"),
    3: Student(name="George", age="15", class_="year 27"),
    4: Student(name="Ringo", age=19, class_="year 23")
}

@app.get("/")
def index():
    return {"message": "Hello World!!"}

@app.get("/students/")
def get_students(name: str | None = None) -> dict[int, Student] | Student: 
    """
    Get all students or get a student by name by passing the name as a query parameter, 
    i.e., /students/?name=student_name
    """

    if name: # name was passed as a query parameter
        for student_id in students.keys():
            if students[student_id].name == name.capitalize(): # all names in the database are capitalized
                return students[student_id]
        
        raise HTTPException(status_code=404, detail=f"Student with name {name} not found.")

    return students # return all students

@app.get("/students/{student_id}")
def get_student_by_id(student_id: int = Path(description="Id of student", gt=0)) -> Student:
    """
    Get student by id.
    """

    try:
        return students[student_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found.")


@app.post("/students/")
def create_student(student_info: Student) -> Student:
    """
    Store student info in database.
    """

    student_id = max(students.keys()) + 1 # calculate student id
    student_info.name = student_info.name.capitalize() # names in the database must be capitalized

    students[student_id] = student_info # store student info in database

    return students[student_id]
