from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# SQL get all
# @router.get("/posts")
# def get_posts():
#     posts=cursor.execute("""SELECT * FROM posts""")
#     posts=cursor.fetchall()
#     return {'data':posts} 

# ORM get all
@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""):

    #Filter by id
    # posts=db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # All posts
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results=db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    print(results)

    return posts

#SQL create
# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
#     new_post=cursor.fetchone()
#     conn.commit()
#     return {'data':new_post}

#ORM create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post=models.Post(owner_id = current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#SQL get one
# @router.get("/posts/{id}")
# def get_post(id: int):
#     post=cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
#     post=cursor.fetchone()
#     print(post)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     return {"post_detail":post}

#ORM get one
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # Filter by id (if not, delete)
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")

    return post

# SQL delete
# @router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
#     deleted_post=cursor.fetchone()
#     conn.commit()
#     if deleted_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

#ORM delete
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# SQL delete
# @router.put("/posts/{id}")
# def update_post(id: int, post:Post):
#     cursor.execute("""UPDATE posts SET title= %s, content= %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,id))
#     updated_post=cursor.fetchone()
#     conn.commit()
#     if updated_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found") 
#     return{"message":updated_post}

# ORM update
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()