from fastapi import FastAPI, HTTPException, Path


app = FastAPI()

# our database
students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 25"
    },
    2: {
        "name": "Paul",
        "age": 16,
        "class": "year 26"
    },
    3: {
        "name": "George",
        "age": 15,
        "class": "year 27"
    },
    4: {
        "name": "Ringo",
        "age": 19,
        "class": "year 23"
    }
}

@app.get("/")
def index():
    return {"message": "Hello World!!"}

@app.get("/students/")
def get_students(name: str | None = None):
    """
    Get all students or get a student by name by passing the name as a query parameter, 
    i.e., /students/?name=student_name
    """

    if name: # name was passed as a query parameter
        for student_id in students.keys():
            if students[student_id]["name"] == name.capitalize(): # all names in the database are capitalized
                return students[student_id]
        
        raise HTTPException(status_code=404, detail=f"Student with name {name} not found.")

    return students # return all students

@app.get("/students/{student_id}")
def get_student_by_id(student_id: int = Path(description="Id of student", gt=0)):
    """
    Get student by id.
    """

    try:
        return students[student_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found.")
