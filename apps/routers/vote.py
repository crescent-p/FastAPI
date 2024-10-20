

from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, database, oauth, models
from sqlalchemy.orm import Session

router = APIRouter(tags=["Votes"])

@router.post('/votes', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth.get_current_user)):

    first_porst = db.query(models.Post).where(models.Post.id == vote.post_id).first()
    if not first_porst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The said post was not found")


    query = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.posts_id == vote.post_id)
    found_post = query.first()   
    if(vote.dir == 1):
        if found_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already voted for this post")
        else:
            new_vote = models.Votes(user_id=current_user.id, posts_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            
            return {"message": "Successfully added vote."}
    elif(vote.dir == 0):
        if not found_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You didn't like this post. Like before you unlilke")
        else:
            query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Successfully deleted vote."}
