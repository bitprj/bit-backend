# Card

Created: Jan 31, 2020 5:02 PM

**Note: All cards will be created through a CMS**

Card model

- This model is used to display the steps of an activity
- Cards are owned by an activity
- Card own Concepts and Hints

Card fields

- name - name of the Card
- contentful_id - the contentful id from cotentful
- order - the order in which the card is displayed
- activity_id - the foreign key used to reference an activity
- activity - the activity that the card belongs to. **One to many with Activity model.**
- checkpoint_id -the foreign key used to reference a checkpoint
- checkpoint - the checkpoint that belongs to a Card. **One to one with Checkpoint model.**
- concepts - keeps track of the concepts that belongs to a card. **Many to many with Concept model.**
- hints - keeps track of the hints that belongs to a card. **Many to many with Hint model.**
- activity_locked_cards - keeps track of the locked cards in the ActivityProgress model. **Many to many with ActivityProgress.**
- activity_unlocked_cards - keeps track of the unlocked cards in the ActivityProgress model. **Many to many with ActivityProgress.**