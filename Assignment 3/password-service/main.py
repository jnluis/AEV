from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import LargeBinary
from sqlmodel import Field, Session, SQLModel, create_engine, select
from hashlib import md5
from base64 import b64encode, b64decode

class Password(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    pass_hash: bytes

class PasswordNew(SQLModel):
    password: str

class PasswordOut(SQLModel):
    id: int | None
    pass_hash: str # Base64 encoded in UTF-8

def encode_pass(password: Password) -> PasswordOut:
    public_hash = b64encode(password.pass_hash).decode("utf-8")
    return PasswordOut(id=password.id, pass_hash=public_hash)

# Surely this generic CRUD-like design couldn't be unsafe, right?!

# TODO: Refer lack of proper security requirements specification in design.

sqlite_fname = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_fname}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def clear_db():
    SQLModel.metadata.drop_all(engine)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield
    # clear_db()

# VULNERABLE!
def md5_hash(password: str) -> bytes:
    m = md5()
    m.update(password.encode("utf-8"))
    return m.digest()

app = FastAPI(lifespan=lifespan)

@app.post("/", response_model=PasswordOut)
async def create_pass(password: PasswordNew, session: SessionDep):
    hashed_password = md5_hash(password.password)
    db_password = Password(pass_hash=hashed_password)

    session.add(db_password)
    session.commit()
    session.refresh(db_password)

    return encode_pass(db_password)

@app.get("/", response_model=list[PasswordOut])
async def get_passwords(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    passwords = session.exec(select(Password).offset(offset).limit(limit)).all()
    return [encode_pass(password) for password in passwords]

@app.get("/{pass_id}", response_model=PasswordOut)
async def get_password(pass_id: int, session: SessionDep):
    password = session.get(Password, pass_id)
    if not password:
        raise HTTPException(status_code=404, detail="Password not found")
    return encode_pass(password)

@app.delete("/{pass_id}")
async def delete_password(pass_id: int, session: SessionDep):
    password = session.get(Password, pass_id)
    if not password:
        raise HTTPException(status_code=404, detail="Password not found")
    session.delete(password)
    session.commit()
    return {"ok": True}

@app.put("/{pass_id}", response_model=PasswordOut)
async def update_password(pass_id: int, password: PasswordNew, session: SessionDep):
    curr_password = session.get(Password, pass_id)
    if not curr_password:
        raise HTTPException(status_code=404, detail="Password not found")
    
    hashed_password = md5_hash(password.password)
    db_password = Password(id=pass_id, pass_hash=hashed_password)

    session.add(db_password)
    session.commit()
    session.refresh(db_password)

    return encode_pass(db_password)