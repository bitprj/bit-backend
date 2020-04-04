from backend import db
from backend.cards.utils import get_cards_hints
from backend.checkpoint_progresses.utils import create_checkpoint_progresses
from backend.hints.utils import create_hint_status
from backend.models import Activity, ActivityProgress, CheckpointProgress, HintStatus, ModuleProgress


# Function to create an ActivityProgress
def create_progress(activity_id, current_user_id):
    activity_prog = ActivityProgress(student_id=current_user_id,
                                     activity_id=activity_id,
                                     accumulated_gems=0)
    activity = Activity.query.get(activity_id)
    # Create checkpoint progresses
    activity_prog.checkpoints = create_checkpoint_progresses(activity.cards, current_user_id)
    # Sets the first card of the activity as the last card unlocked
    activity.cards.sort(key=lambda x: x.order)
    next_card = activity.cards[0]
    activity_prog.cards_locked = activity.cards
    activity_prog.cards_locked.pop(0)
    activity_prog.cards_unlocked.append(next_card)
    activity_prog.last_card_unlocked = next_card.id
    activity_prog.accumulated_gems += next_card.gems
    db.session.add(activity_prog)
    db.session.commit()

    return activity_prog


# Function to fill in the activity_progress' relationships
def fill_in_rels(student_activity_prog, student):
    if student_activity_prog.activity in student.incomplete_activities:
        student.incomplete_activities.remove(student_activity_prog.activity)

    # Fills in the hints and cards as locked in the activity progress
    hints = get_cards_hints(student_activity_prog.activity.cards)
    create_hint_status(student_activity_prog, hints)

    return


# Function to check if the ActivityProgress is completed by checking if all the checkpoints are completed
def is_activity_completed(activity_progress_id, student_id):
    activity_progress = ActivityProgress.query.get(activity_progress_id)
    incomplete_checkpoint_progresses = CheckpointProgress.query.filter_by(activity_progress_id=activity_progress_id,
                                                                          is_completed=False,
                                                                          student_id=student_id).all()
    # If there are any incomplete progresses, then return immediately, else mark activity_progress as completed
    if incomplete_checkpoint_progresses and not activity_progress.cards_locked:
        activity_progress.is_completed = False
        return

    if not activity_progress.cards_locked:
        activity_progress.is_completed = True
        activity_progress.is_graded = False

        for module in activity_progress.activity.modules:
            module_prog = ModuleProgress.query.filter_by(module_id=module.id, student_id=student_id).first()

            if activity_progress.activity in module_prog.inprogress_activities:
                module_prog.inprogress_activities.remove(activity_progress.activity)
                module_prog.completed_activities.append(activity_progress.activity)

    return


# Function to unlock a card
def unlock_card(student_activity_prog, next_card):
    locked_cards = student_activity_prog.cards_locked
    locked_cards.sort(key=lambda x: x.order)
    locked_cards.remove(next_card)
    student_activity_prog.cards_unlocked.append(next_card)
    student_activity_prog.accumulated_gems += next_card.gems

    return


# Function to unlock a hint
def unlock_hint(student_activity_prog, hint):
    hint_status = HintStatus.query.filter_by(hint_id=hint.id, activity_progress_id=student_activity_prog.id).first()

    if hint_status.is_unlocked:
        return "Hint already unlocked"

    hint_status.is_unlocked = True
    student_activity_prog.accumulated_gems -= hint.gems

    return "Hint unlocked!"
