from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select

from database.connection import get_session
from models.events import Event, EventUpdate

event_router = APIRouter(
    tags=['Events']
)

events = []


@event_router.get('/', response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    all_events = session.exec(statement).all()
    return all_events


@event_router.get('/{id}', response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:

    event = session.get(Event, id)
    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Event with supplied ID {id} does not exist'
    )


@event_router.post('/new')
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {
        "message": f'Event {new_event.id} created successfully'
    }


@event_router.put('/{id}', response_model=Event)
async def update_event(id: int, modified_event: EventUpdate, session=Depends(get_session)) -> dict:

    event = session.get(Event, id)
    if event:
        event_data = modified_event.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Event with supplied ID {id} does not exist'
        )


@event_router.delete('/{id}')
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()

        return {
            'message': f'Event {id} delete successfully'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Event supplied id {id} does not exist'
        )


@event_router.delete('/')
async def delete_all_events() -> dict:
    events.clear()
    return {
        'message': 'Events deleted successfully'
    }
