### Development Environment Setup

1. Setup VS Code with all the related extensions.
    - Python
    - Pylance
    - Django
    - Docker
    - Docker Compose

2. Docker Compose setup. If we want this to be a webapp,
   I'd do a simple docker compose setup with a Django container and a Database.

### System Architecture

**Card Data Model**

* Face Value (Integer)
* Picture Value (Enum) (A, K, Q, J, Joker)
* Suit (Enum) (Hearts, Spades, Clubs, Diamonds)
* Deck (Foreign Key Reference)
* Position in Deck (Non-Nullable, Unique Within Deck)
* Constraint: One, and only one, of "Face Value" and "Picture Value" are populated, the other is NULL.
* Constraint: Suit must be populated, unless the card is a Joker, in which case suit is NULL.

**Deck Data Model**

* Doesn't have any fields, just holds cards via a reference.
* Has a "shuffle" function, which randomly sets all the card positions, then does a single big write to the database, both for performance and also to avoid the Card Position Unique constraint.

**Assumptions**

I deliberately did not constrain decks to have 52 cards, or constrain that cards must be unique within a deck. Some games (like 500) take cards out. Other may or may not use Jokers. Others (like Canasta) use two decks meaning cards aren't unique. My philosophy is to be cautious with assumptions, having them broken later causes bigger problems than the time you saved up front.

I did assume every card needs a face or picture value. To account for jokers, I included that as a face value option and added a database constaint that a Joker has no suit.

I made it so face value can be any number as opposed to just more enum values, for two reasons. Firstly, it makes sorting the cards easier and more maintainable. Also, some games (like 6-player 500) have special cards like 11, 12, 13.

I assumed I needed to store the data in a database, hence the relationship between Deck and Card being represented as a Foreign Key from the card to the deck. If it was all just within Python, I would've made Cards a List inside Deck, which would've been easier to maintain.

### Development Plan

1. Write tests first, TDD is a great way to make your development goals contained and objective.
2. **Implement database models.**
3. **Implement code:** Deck.shuffle() function.

### CI/CD Pipeline

We could use GitHub actions or GitLab for a CI/CD pipeline. Ideally we'd have these steps, with the pipeline being stopped if any of them fail:

1. Static Analysis (Static Analysis comes first since it's quick, we don't want to run a big test suite only to fail lint and have to run all the tests again).
    * Lint. (e.g. flake8)
    * Type Checking. (e.g. MyPy)
    * Security (e.g. Bandit)

2. Unit Tests. (Come next, because they're also fast)

3. Integration Tests. (Complex tests involving the database, run last because we don't want to spend time on them until every quick check has been done first)

4. Deployment. (Automatically deploy to a testing or staging environment, to be double checked by a tester before being rolled out to Production).

### Important Architectural Decision

An important decision I made was to keep the "Card" database table relatively unconstrained. For example, it can have face values other than 2 through 10, there can be duplicates within a deck, there can be cards missing from the deck, etc.

The requirements don't specify what card game is being played, so I needed to keep it fluid to avoid broken assumptions later. If I knew what game we were playing, I would've constrained the database more to make things more maintainable.
