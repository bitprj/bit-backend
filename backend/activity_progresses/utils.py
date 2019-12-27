from backend.models import ActivityProgress


# Function to unlock a card
def unlock_card(activity_id, current_user_id):
    student_activity_prog = ActivityProgress.query.filter_by(student_id=current_user_id,
                                                             activity_id=activity_id).first()
    for card in student_activity_prog.cards_locked:
        print(card.order)
    locked_cards = student_activity_prog.cards_locked
    locked_cards.sort(key=lambda x: x.order)

    target_card = locked_cards[0]
    print(target_card)
    student_activity_prog.cards_unlocked.append(target_card)
    student_activity_prog.cards_locked.remove(target_card)
    # print(target_card.order)
    student_activity_prog.last_card_completed = target_card.order
    print(student_activity_prog.last_card_completed)
    print(student_activity_prog.cards_locked)
    print(student_activity_prog.cards_unlocked)
    return
