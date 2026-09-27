# The UI drives each Turn through a job, with no server-side Battle loop

Nothing on the server runs a Battle from start to finish. The UI plays back the previous Turn's Turn Events, then requests the next Turn. A create-job Lambda returns a job ID straight away and invokes the Referee asynchronously. The Referee loads the state from DynamoDB, invokes both Trainers, saves the new state, and marks the job complete. A polling Lambda reports the job's status to the UI. We chose this over a synchronous request, because a Turn with several LLM calls can go past API Gateway's 29-second limit. We also chose it over a server-side loop (a self-invoking Lambda or Step Functions), because the UI needs to control the pace of playback anyway, and a job system is a pattern we're comfortable running.

## Consequences

- Each Turn saves state with a conditional write on the expected Turn number, so a duplicate request (a double-click, a browser retry, or an async Lambda retry) can't run the same Turn twice.
- If the UI stops making requests, the Battle simply pauses. No Battle continues without a viewer.
- Step Functions remains a possible later step if orchestration grows beyond one Referee step per Turn.