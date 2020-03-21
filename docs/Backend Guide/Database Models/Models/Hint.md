# Hint

Created: Jan 31, 2020 9:44 PM

**Note: All hints will be created through a CMS**

Hint model

- Hints are used to give students advice if a student is stuck on a card.
- Hints are nested. A hint can own hints.

Hint fields

- name - name of the Hint
- contentful_id - the contentful id from cotentful
- card_id - the foreign key used to reference a card.
- card - keeps track of the card that a hint belongs to. **One to many with Card model.**
- parent_hint_id - the foreign key used to reference a hint.
- hint_children - keeps track of all the hints that belong to a hint. **One to many with Hint models.**
- steps - keeps track of the steps that belong to a hint. **One to many with Step model.**
- activity_progresses - keeps track of the hints that belong to an ActivityProgresses. **Many to many with ActivityProgress model.**