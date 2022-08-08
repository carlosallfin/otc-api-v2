# uvicorn main:app --reload
# venv\scripts\activate.bat

from fastapi import FastAPI
import models
from database import engine
from routers import post,user,auth,vote, currency,accounts,banks
from config import settings

# Creates all of our models
models.Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(currency.router)
app.include_router(accounts.router)
app.include_router(banks.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     return {'status':'success'}

# # SQL get all
# # @app.get("/posts")
# # def get_posts():
# #     posts=cursor.execute("""SELECT * FROM posts""")
# #     posts=cursor.fetchall()
# #     return {'data':posts} 

# # ORM get all
# @app.get("/posts",response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return posts

# #SQL create
# # @app.post("/posts", status_code=status.HTTP_201_CREATED)
# # def create_post(post: Post):
# #     cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
# #     new_post=cursor.fetchone()
# #     conn.commit()
# #     return {'data':new_post}

# #ORM create
# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(post: schemas.PostCreate,db: Session = Depends(get_db)):
#     new_post=models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# #SQL get one
# # @app.get("/posts/{id}")
# # def get_post(id: int):
# #     post=cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
# #     post=cursor.fetchone()
# #     print(post)
# #     if not post:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
# #     return {"post_detail":post}

# #ORM get one
# @app.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id: int,db: Session = Depends(get_db)):
#     post=db.query(models.Post).filter(models.Post.id==id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     return post

# # SQL delete
# # @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# # def delete_post(id: int):
# #     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
# #     deleted_post=cursor.fetchone()
# #     conn.commit()
# #     if deleted_post==None:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
# #     return Response(status_code=status.HTTP_204_NO_CONTENT)

# #ORM delete
# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int,db: Session = Depends(get_db)):
#     post=db.query(models.Post).filter(models.Post.id==id)
#     if post.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# # SQL delete
# # @app.put("/posts/{id}")
# # def update_post(id: int, post:Post):
# #     cursor.execute("""UPDATE posts SET title= %s, content= %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,id))
# #     updated_post=cursor.fetchone()
# #     conn.commit()
# #     if updated_post==None:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found") 
# #     return{"message":updated_post}

# # ORM update
# @app.put("/posts/{id}",response_model=schemas.Post)
# def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
#     post_query=db.query(models.Post).filter(models.Post.id==id)
#     post=post_query.first()
#     if post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     post_query.update(updated_post.dict(),synchronize_session=False)
#     db.commit()
#     return post_query.first()

# #ORM create user
# @app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):

#     #hash password - user.password
#     hashed_pwd = utils.hash(user.password)
#     user.password = hashed_pwd
#     new_user=models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

# #ORM get user
# @app.get("/users/{id}", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def get_user(id: int ,db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')
    
#     return user

