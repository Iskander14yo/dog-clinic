from enum import Enum
from fastapi import FastAPI, Query, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root() -> Dict[str, str]:
    return {"message": "Welcome to the Dog API!"}


@app.post('/post', response_model=Timestamp)
def create_post(timestamp: Timestamp) -> Timestamp:
    post_db.append(timestamp)
    return timestamp


@app.get('/dog', response_model=List[Dog])
def get_dogs(kind: Optional[DogType] = Query(None)):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())


@app.post('/dog', response_model=Dog)
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=400, detail="Dog with this PK already exists")
    dogs_db[dog.pk] = dog
    return dog


@app.get('/dog/{pk}', response_model=Dog)
def get_dog_by_pk(pk: int):
    dog = dogs_db.get(pk)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog


@app.patch('/dog/{pk}', response_model=Dog)
def update_dog(pk: int, dog_update: Dog = Body(...)):
    existing_dog = dogs_db.get(pk)
    if existing_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    dog_update.pk = pk  # Ensure the pk doesn't change
    dogs_db[pk] = dog_update
    return dog_update

