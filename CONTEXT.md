


# Pokémon AI Battle

Turn-based Pokémon battles, in the style of the original games, fought between AI agents from different LLM vendors and overseen by a Referee.

## Language

### Battle

**Battle**:
A single turn-based match between two Trainers, each controlled by a different Vendor, played under simplified Pokémon rules. A Trainer wins when all of its opponent's Pokémon have fainted.
_Avoid_: Match, game, fight

**Turn Event**:
A single fact about what happened in a Turn (e.g. a Switch, an Item used, a move and its damage, a faint, an Illegal Action, the Battle ending). The UI plays back the Turn Events, and the Referee's commentary goes alongside them.
_Avoid_: Log entry, message, animation

**Turn**:
One round of a Battle in which each Trainer takes exactly one action and the Referee resolves them.
_Avoid_: Round, move (a move is something a Pokémon uses, not a unit of time)

**Referee**:
The AI agent that oversees a Battle: it judges whether each Trainer's action is legal, ensures each takes only one action per Turn, and reports the outcome. It never decides the outcome itself.
_Avoid_: Judge, arbiter, game master

**Illegal Action**:
An action a Trainer submits that the rules do not allow (e.g. a move its Pokémon doesn't know, or more than one action in a Turn).
_Avoid_: Invalid move, bad move

**Lost Turn**:
A Turn in which a Trainer takes no action because it submitted two Illegal Actions in a row.
_Avoid_: Skipped turn, forfeit (a forfeit would end the whole Battle)

**Trainer Action**:
An action the Trainer takes itself: a Switch or using an Item. Trainer Actions always resolve before Pokémon Actions.
_Avoid_: Command

**Pokémon Action**:
An action the active Pokémon takes: using one of its moves. Pokémon Actions resolve in order of speed, with a coin toss for ties.
_Avoid_: Attack (not every move needs to be an attack in future)

**Switch**:
A Trainer Action that swaps the active Pokémon for another from the Team, using up the Trainer's action for that Turn.
_Avoid_: Swap, withdraw

**Item**:
A healing potion (Super Potion or Hyper Potion) that a Trainer uses on one of its Pokémon as a Trainer Action. Every Trainer starts a Battle with 2 Super Potions and 1 Hyper Potion.
_Avoid_: Consumable, bag item, potion (when meaning any Item)

**Replacement**:
Sending in a new Pokémon after the active one faints. It happens outside of any Turn and costs no action.
_Avoid_: Switch (a Switch costs an action; a Replacement does not)

**Score**:
Points awarded to the winning Trainer of a Battle: 7 minus the number of Pokémon it brought, so a win with one Pokémon scores 6. Scores add up to a running total for each Model, which can be summed per Vendor.
_Avoid_: Reward, points, prize

**Forfeit**:
Losing a Battle outright, with no Score, because a Trainer submitted two illegal Teams in a row during Team Selection.
_Avoid_: Disqualification, Lost Turn (a Lost Turn only costs one Turn)

**Abandoned**:
A Battle that ended with no winner and no Score for either Trainer because a Vendor failed. Unlike a Forfeit, it is not the Model's fault.
_Avoid_: Cancelled, errored, draw

### Information

**Trainer View**:
The part of the Battle a Trainer is allowed to see: its own Team in full, plus only its opponent's Revealed Pokémon.
_Avoid_: Battle state, game state (the full state is only seen by the Referee)

**Battle Log**:
The record of every Turn so far, including actions, Illegal Actions and results. Each Trainer receives the Battle Log filtered by the same rules as its Trainer View.
_Avoid_: History, transcript

### Trainers and teams

**Vendor**:
An LLM provider. Every Battle is Anthropic vs OpenAI, and DeepSeek runs the Referee.
_Avoid_: Provider, model company

**Model**:
The specific LLM from a Vendor that controls a Trainer, chosen for each Battle.
_Avoid_: Engine, bot

**Team Selection**:
The phase before Turn 1 in which each Trainer, without seeing its opponent's choices, picks a name, an Archetype, a Team and a lead Pokémon.
_Avoid_: Draft, team building

**Trainer**:
The persona an AI agent plays in a Battle: a name it chooses, plus an Archetype, controlling one Team.
_Avoid_: Player, agent, competitor

**Archetype**:
A trainer class from the original games (e.g. Bug Catcher, Hiker) that a Trainer adopts, which limits its Team to Pokémon of certain types. Gym Leaders and the Elite Four are named people, not Archetypes.
_Avoid_: Class, role, persona

**Team**:
The one to six Rental Pokémon a Trainer brings to a Battle.
_Avoid_: Party, roster

**Rental Pokémon**:
A Pokémon at level 50, knowing the last four damaging moves it would have learned by that level in Pokémon Red/Blue/Green/Yellow, that a Trainer picks for its Team, as in Pokémon Stadium's rental system. Mew and Mewtwo cannot be rented.
_Avoid_: Owned Pokémon, loaned Pokémon

**Revealed**:
The state of an opponent's Pokémon once it has been sent into battle. A Trainer can only see its opponent's Revealed Pokémon. An opponent's Archetype is Revealed along with its first Pokémon.
_Avoid_: Visible, known, scouted