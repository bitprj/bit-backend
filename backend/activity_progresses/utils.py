from backend import db
from backend.cards.utils import get_cards_hints
from backend.models import Activity, ActivityProgress


# Function to create an ActivityProgress
def create_progress(activity_id, current_user_id):
    activity_prog = ActivityProgress(student_id=current_user_id,
                                     activity_id=activity_id)

    activity = Activity.query.get(activity_id)
    activity.cards.sort(key=lambda x: x.order)
    # Fills in the hints and cards as locked in the activity progress
    activity_prog.hints_locked = get_cards_hints(activity.cards)
    next_card = activity.cards[0]
    activity_prog.cards_locked = activity.cards
    activity_prog.cards_locked.pop(0)
    activity_prog.cards_unlocked.append(next_card)
    activity_prog.last_card_completed = next_card.id

    return activity_prog


# Function to get the hint data based on a card
def get_hint_data(student_activity_prog, target_card):
    card_hints = set(target_card.hints)
    locked_card_hints = set(student_activity_prog.hints_locked).intersection(card_hints)
    unlocked_card_hints = set(student_activity_prog.hints_unlocked).intersection(card_hints)
    db.session.commit()

    hints = {
        "hints_locked": locked_card_hints,
        "hints_unlocked": unlocked_card_hints
    }

    return hints


# Function to unlock a card
def unlock_card(student_activity_prog):
    locked_cards = student_activity_prog.cards_locked
    locked_cards.sort(key=lambda x: x.order)

    target_card = locked_cards.pop(0)
    student_activity_prog.cards_unlocked.append(target_card)
    student_activity_prog.last_card_completed = target_card.order

    return target_card
