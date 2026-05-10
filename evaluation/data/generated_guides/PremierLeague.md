# PremierLeague Schema Reference Guide

## Schema Summary
This schema contains Premier League football match data, including player performance statistics across 206 detailed action metrics, match results, team information, and player identities.

---

## Join Paths

**Player actions in a specific match:**
```sql
SELECT a.* FROM PremierLeague.Actions a
JOIN PremierLeague.Matches m ON a.MatchID = m.MatchID
WHERE m.MatchID = ?
```

**Player performance for a team:**
```sql
SELECT a.*, p.Name FROM PremierLeague.Actions a
JOIN PremierLeague.Players p ON a.PlayerID = p.PlayerID
WHERE a.TeamID = ?
```

**Match details with team names:**
```sql
SELECT m.*, th.Name AS HomeTeam, ta.Name AS AwayTeam
FROM PremierLeague.Matches m
JOIN PremierLeague.Teams th ON m.TeamHomeID = th.TeamID
JOIN PremierLeague.Teams ta ON m.TeamAwayID = ta.TeamID
```

**Player actions with full context:**
```sql
SELECT a.*, p.Name AS PlayerName, t.Name AS TeamName, m.Date
FROM PremierLeague.Actions a
JOIN PremierLeague.Players p ON a.PlayerID = p.PlayerID
JOIN PremierLeague.Teams t ON a.TeamID = t.TeamID
JOIN PremierLeague.Matches m ON a.MatchID = m.MatchID
```

---

## Table Reference

### `PremierLeague.Actions`
Player-level performance statistics for individual matches. One row per player per match.

**Key columns (non-obvious semantics):**

| Column | Meaning | Notes |
|--------|---------|-------|
| `PlayerID` | Foreign key to Players | |
| `MatchID` | Foreign key to Matches | |
| `TeamID` | Foreign key to Teams | |
| `TimePlayed` | Minutes played in match | |
| `PositionID` | Player position code | Numeric identifier |
| `Starts` | 1 if player started, 0 if substitute | |
| `SubstituteOn`, `SubstituteOff` | 1 if player came on/went off bench | |
| `FirstGoal`, `WinningGoal` | 1 if player scored first/winning goal | |
| `shot_eff`, `passes_eff`, `tackle_eff`, `dribble_eff` | Efficiency metrics | DOUBLE; -1.0 indicates no attempts |
| `Team1`, `Team2` | Team names (denormalized) | Enum: Arsenal, Aston Villa, Blackburn Rovers, Bolton Wanderers, Chelsea, Everton, Fulham, Liverpool, Manchester City, Manchester United, Newcastle United, Norwich City, Queens Park Rangers, Stoke City, Sunderland, Swansea City, Tottenham Hotspur, West Bromwich Albion, Wigan Athletic, Wolverhampton Wanderers |

**Shooting metrics:**
- `Goals`, `ShotsonTargetincgoals`, `ShotsOffTargetincwoodwork`, `BlockedShots`
- By location: `GoalsfromInsideBox`, `GoalsfromOutsideBox`
- By body part: `HeadedGoals`, `LeftFootGoals`, `RightFootGoals`, `OtherGoals`
- By situation: `GoalsOpenPlay`, `GoalsfromCorners`, `GoalsfromThrows`, `GoalsfromDirectFreeKick`, `GoalsfromSetPlay`, `Goalsfrompenalties`
- Penalties: `PenaltiesTaken`, `PenaltyGoals`, `PenaltiesSaved`, `PenaltiesOffTarget`, `PenaltiesNotScored`

**Passing metrics:**
- `TotalSuccessfulPassesAll`, `TotalUnsuccessfulPassesAll`
- By area: `SuccessfulPassesOwnHalf`, `SuccessfulPassesOppositionHalf`, `SuccessfulPassesDefensivethird`, `SuccessfulPassesMiddlethird`, `SuccessfulPassesFinalthird`
- By type: `SuccessfulShortPasses`, `SuccessfulLongPasses`, `SuccessfulCrossesCorners`, `SuccessfulFlickOns`
- Assists and key passes: `Assists`, `KeyPasses`

**Defensive metrics:**
- Duels: `Duelswon`, `Duelslost`, `AerialDuelswon`, `AerialDuelslost`, `GroundDuelswon`, `GroundDuelslost`
- Tackles: `TacklesWon`, `TacklesLost`, `LastManTackle`
- Clearances: `TotalClearances`, `HeadedClearances`, `OtherClearances`, `ClearancesOfftheLine`
- Other: `Blocks`, `Interceptions`, `Recoveries`

**Goalkeeper-specific metrics:**
- `SavesMade`, `SavesMadefromInsideBox`, `SavesMadefromOutsideBox`, `SavesfromPenalty`
- `Catches`, `Punches`, `Drops`, `CrossesnotClaimed`
- `GKDistribution`, `GKSuccessfulDistribution`, `GKUnsuccessfulDistribution`
- `CleanSheets`, `TeamCleansheet`

**Discipline & Fouls:**
- `YellowCards`, `RedCards`
- `TotalFoulsConceded`, `FoulsConcededexchandballspens`, `TotalFoulsWon`
- `HandballsConceded`, `PenaltiesConceded`, `Offsides`

**Other:**
- `Touches`, `BigChances`, `BigChancesFaced`
- `Turnovers`, `Dispossessed`
- `GoalsConceded`, `GoalsConcededInsideBox`, `GoalsConcededOutsideBox`

---

### `PremierLeague.Matches`
Match-level records. One row per match.

| Column | Meaning | Notes |
|--------|---------|-------|
| `MatchID` | Primary key | |
| `TeamHomeID` | Foreign key to Teams (home team) | |
| `TeamAwayID` | Foreign key to Teams (away team) | |
| `TeamHomeFormation` | Formation code for home team | Numeric |
| `TeamAwayFormation` | Formation code for away team | Numeric |
| `ResultOfTeamHome` | Match result from home team perspective | 1 = win, 0 = draw, -1 = loss |
| `Date` | Match date and time | TIMESTAMP |

---

### `PremierLeague.Players`
Player master data.

| Column | Meaning |
|--------|---------|
| `PlayerID` | Primary key |
| `Name` | Player full name |

---

### `PremierLeague.Teams`
Team master data.

| Column | Meaning | Notes |
|--------|---------|-------|
| `TeamID` | Primary key | |
| `Name` | Team name | Enum: Arsenal, Aston Villa, Blackburn Rovers, Bolton Wanderers, Chelsea, Everton, Fulham, Liverpool, Manchester City, Manchester United, Newcastle United, Norwich City, Queens Park Rangers, Stoke City, Sunderland, Swansea City, Tottenham Hotspur, West Bromwich Albion, Wigan Athletic, Wolverhampton Wanderers |

---

## Synonym Glossary

| Question Term | Schema Reference |
|---|---|
| player goals | `PremierLeague.Actions.Goals` |
| shots on target | `PremierLeague.Actions.ShotsonTargetincgoals` |
| assists | `PremierLeague.Actions.Assists` |
| passes completed | `PremierLeague.Actions.TotalSuccessfulPassesAll` |
| tackles won | `PremierLeague.Actions.TacklesWon` |
| clean sheet | `PremierLeague.Actions.CleanSheets = 1` |
| yellow card | `PremierLeague.Actions.YellowCards` |
| red card | `PremierLeague.Actions.RedCards` |
| minutes played | `PremierLeague.Actions.TimePlayed` |
| started match | `PremierLeague.Actions.Starts = 1` |
| substitute appearance | `PremierLeague.Actions.SubstituteOn = 1` |
| home win | `PremierLeague.Matches.ResultOfTeamHome = 1` |
| away win | `PremierLeague.Matches.ResultOfTeamHome = -1` |
| draw | `PremierLeague.Matches.ResultOfTeamHome = 0` |