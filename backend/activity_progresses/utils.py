from backend.checkpoints.utils import create_checkpoint_progresses
from backend.models import Activity, ActivityProgress, CheckpointProgress, HintStatus


# Function to create an ActivityProgress
def create_progress(activity_id, current_user_id):
    activity_prog = ActivityProgress(student_id=current_user_id,
                                     activity_id=activity_id)

    activity = Activity.query.get(activity_id)
    activity_prog.checkpoints = create_checkpoint_progresses(activity.checkpoints, current_user_id)
    activity.cards.sort(key=lambda x: x.order)
    next_card = activity.cards[0]
    activity_prog.cards_locked = activity.cards
    activity_prog.cards_locked.pop(0)
    activity_prog.cards_unlocked.append(next_card)
    activity_prog.last_card_completed = next_card.id

    return activity_prog


# Function to check if the ActivityProgress is completed by checking if all the checkpoints are completed
def is_activity_completed(activity_progress_id, student_id):
    activity_progress = ActivityProgress.query.get(activity_progress_id)
    incomplete_checkpoint_progresses = CheckpointProgress.query.filter_by(activity_progress_id=activity_progress_id,
                                                                          is_completed=False,
                                                                          student_id=student_id).all()
    # If there are any incomplete progresses, then return immediately, else mark activity_progress as completed
    if incomplete_checkpoint_progresses:
        activity_progress.is_completed = False
        return

    activity_progress.is_completed = True
    activity_progress.is_graded = False

    return


# Function to unlock a card
def unlock_card(student_activity_prog, next_card):
    locked_cards = student_activity_prog.cards_locked
    locked_cards.sort(key=lambda x: x.order)
    locked_cards.remove(next_card)
    student_activity_prog.cards_unlocked.append(next_card)

    return


# Function to unlock a hint
def unlock_hint(student_activity_prog, hint):
    hint_status = HintStatus.query.filter_by(hint_id=hint.id, activity_progress_id=student_activity_prog.id).first()

    if hint_status.is_unlocked:
        return "Hint already unlocked"

    hint_status.is_unlocked = True

    return "Hint unlocked!"
