# The Referee judges legality; code decides outcomes

The Referee is an LLM agent, but it never writes Battle state. It decides only whether a Trainer's action is legal and reports what happened. Everything numeric or outcome-deciding (damage, healing, turn order, speed-tie coin tosses, fainting, the win condition, and filtering each Trainer's view of the Battle) is done by deterministic code, which the Referee reaches through tools. We chose this because LLMs make arithmetic mistakes, can be argued with, and don't give the same result on replay. If an LLM decided outcomes, a Battle could be won because the Referee made a mistake rather than because one Vendor played better, which would defeat the point of comparing Vendors.

## Consequences

- Because the Referee can't change an outcome, it doesn't need to be neutral. It runs on a fixed Vendor (DeepSeek) that doesn't play as a Trainer.
- All randomness (coin tosses) is seeded and recorded, so a Battle can be replayed exactly.