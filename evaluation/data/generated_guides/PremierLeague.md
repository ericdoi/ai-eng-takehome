# Premier League Schema Reference Guide

## Schema Summary
This schema contains Premier League football (soccer) match data, including detailed player performance statistics across matches, team information, and match results.

---

## Table Reference

### Table: `PremierLeague.Teams`
**Meaning:** Team master data for Premier League clubs.
**Synonyms:** Club, Organization

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `TeamID` | BIGINT | Unique team identifier | Club ID |
| `Name` | VARCHAR | Team name | Club Name |

**Notable Values (Name):**
Arsenal, Aston Villa, Blackburn Rovers, Bolton Wanderers, Chelsea, Everton, Fulham, Liverpool, Manchester City, Manchester United, Newcastle United, Norwich City, Queens Park Rangers, Stoke City, Sunderland, Swansea City, Tottenham Hotspur, West Bromwich Albion, Wigan Athletic, Wolverhampton Wanderers

---

### Table: `PremierLeague.Players`
**Meaning:** Player master data with player identifiers and names.
**Synonyms:** Athlete, Squad Member

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `PlayerID` | BIGINT | Unique player identifier | Athlete ID |
| `Name` | VARCHAR | Player full name | Player Name, Athlete Name |

---

### Table: `PremierLeague.Matches`
**Meaning:** Match-level data including teams, formations, results, and dates.
**Synonyms:** Game, Fixture

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `MatchID` | BIGINT | Unique match identifier | Game ID, Fixture ID |
| `TeamHomeID` | BIGINT | Home team identifier (foreign key to `Teams.TeamID`) | Home Team ID |
| `TeamAwayID` | BIGINT | Away team identifier (foreign key to `Teams.TeamID`) | Away Team ID |
| `TeamHomeFormation` | BIGINT | Home team formation code (e.g., 4-4-2 represented as integer) | Home Formation |
| `TeamAwayFormation` | BIGINT | Away team formation code | Away Formation |
| `ResultOfTeamHome` | BIGINT | Match result from home team perspective: 1 = Win, 0 = Draw, -1 = Loss | Home Result, Match Outcome |
| `Date` | TIMESTAMP | Match date and time | Match Date, Fixture Date |

---

### Table: `PremierLeague.Actions`
**Meaning:** Detailed player performance statistics per match, including shooting, passing, defensive, and goalkeeper actions.
**Synonyms:** Player Match Stats, Performance Data, Event Statistics

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `PlayerID` | BIGINT | Player identifier (foreign key to `Players.PlayerID`) | Athlete ID |
| `MatchID` | BIGINT | Match identifier (foreign key to `Matches.MatchID`) | Game ID |
| `TeamID` | BIGINT | Team identifier (foreign key to `Teams.TeamID`) | Club ID |
| `Team1` | VARCHAR | Home team name | Home Team Name |
| `Team2` | VARCHAR | Away team name | Away Team Name |
| **Shooting Statistics** | | | |
| `Goals` | BIGINT | Total goals scored | Scoring |
| `ShotsonTargetincgoals` | BIGINT | Shots on target including goals | On-Target Shots |
| `ShotsOffTargetincwoodwork` | BIGINT | Shots off target including woodwork | Off-Target Shots |
| `BlockedShots` | BIGINT | Shots blocked by opposition | Blocked Attempts |
| `BigChances` | BIGINT | High-quality scoring opportunities created | Clear Chances |
| `BigChancesFaced` | BIGINT | High-quality scoring opportunities faced | Chances Against |
| `FirstGoal` | BIGINT | Indicator: player scored first goal of match | Opening Goal |
| `WinningGoal` | BIGINT | Indicator: player scored winning goal | Match-Winning Goal |
| **Penalty Statistics** | | | |
| `PenaltiesTaken` | BIGINT | Penalties attempted | Penalty Attempts |
| `PenaltyGoals` | BIGINT | Penalties converted | Penalty Conversions |
| `PenaltiesSaved` | BIGINT | Penalties saved (goalkeeper) | Penalty Saves |
| `PenaltiesOffTarget` | BIGINT | Penalties missed off target | Penalty Misses Off Target |
| `PenaltiesNotScored` | BIGINT | Penalties not converted | Penalty Failures |
| `PenaltiesConceded` | BIGINT | Penalties conceded by player | Fouls Resulting in Penalties |
| **Free Kick Statistics** | | | |
| `DirectFreekickGoals` | BIGINT | Goals from direct free kicks | Free Kick Goals |
| `DirectFreekickOnTarget` | BIGINT | Direct free kicks on target | Free Kick On Target |
| `DirectFreekickOffTarget` | BIGINT | Direct free kicks off target | Free Kick Off Target |
| `BlockedDirectFreekick` | BIGINT | Direct free kicks blocked | Blocked Free Kicks |
| **Shot Location Statistics** | | | |
| `GoalsfromInsideBox` | BIGINT | Goals from inside penalty box | Inside Box Goals |
| `ShotsOnfromInsideBox` | BIGINT | On-target shots from inside box | Inside Box On Target |
| `ShotsOfffromInsideBox` | BIGINT | Off-target shots from inside box | Inside Box Off Target |
| `BlockedShotsfromInsideBox` | BIGINT | Blocked shots from inside box | Inside Box Blocked |
| `GoalsfromOutsideBox` | BIGINT | Goals from outside penalty box | Outside Box Goals |
| `ShotsOnTargetOutsideBox` | BIGINT | On-target shots from outside box | Outside Box On Target |
| `ShotsOffTargetOutsideBox` | BIGINT | Off-target shots from outside box | Outside Box Off Target |
| `BlockedShotsOutsideBox` | BIGINT | Blocked shots from outside box | Outside Box Blocked |
| **Shot Type Statistics** | | | |
| `HeadedGoals` | BIGINT | Goals scored with head | Header Goals |
| `HeadedShotsOnTarget` | BIGINT | Headed shots on target | Header On Target |
| `HeadedShotsOffTarget` | BIGINT | Headed shots off target | Header Off Target |
| `HeadedBlockedShots` | BIGINT | Headed shots blocked | Header Blocked |
| `LeftFootGoals` | BIGINT | Goals with left foot | Left Foot Goals |
| `LeftFootShotsOnTarget` | BIGINT | Left foot shots on target | Left Foot On Target |
| `LeftFootShotsOffTarget` | BIGINT | Left foot shots off target | Left Foot Off Target |
| `LeftFootBlockedShots` | BIGINT | Left foot shots blocked | Left Foot Blocked |
| `RightFootGoals` | BIGINT | Goals with right foot | Right Foot Goals |
| `RightFootShotsOnTarget` | BIGINT | Right foot shots on target | Right Foot On Target |
| `RightFootShotsOffTarget` | BIGINT | Right foot shots off target | Right Foot Off Target |
| `RightFootBlockedShots` | BIGINT | Right foot shots blocked | Right Foot Blocked |
| `OtherGoals` | BIGINT | Goals by other means | Other Goals |
| `OtherShotsOnTarget` | BIGINT | Other shots on target | Other On Target |
| `OtherShotsOffTarget` | BIGINT | Other shots off target | Other Off Target |
| `OtherBlockedShots` | BIGINT | Other shots blocked | Other Blocked |
| **Goal Context Statistics** | | | |
| `GoalsOpenPlay` | BIGINT | Goals from open play | Open Play Goals |
| `GoalsfromCorners` | BIGINT | Goals from corner kicks | Corner Goals |
| `GoalsfromThrows` | BIGINT | Goals from throw-ins | Throw-In Goals |
| `GoalsfromDirectFreeKick` | BIGINT | Goals from direct free kicks | Direct Free Kick Goals |
| `GoalsfromSetPlay` | BIGINT | Goals from set plays | Set Play Goals |
| `Goalsfrompenalties` | BIGINT | Goals from penalties | Penalty Goals |
| `Goalsasasubstitute` | BIGINT | Goals scored as substitute | Substitute Goals |
| **Attempt Context Statistics** | | | |
| `AttemptsOpenPlayontarget` | BIGINT | Open play attempts on target | Open Play On Target |
| `AttemptsfromCornersontarget` | BIGINT | Corner attempts on target | Corner On Target |
| `AttemptsfromThrowsontarget` | BIGINT | Throw-in attempts on target | Throw-In On Target |
| `AttemptsfromDirectFreeKickontarget` | BIGINT | Direct free kick attempts on target | Free Kick On Target |
| `AttemptsfromSetPlayontarget` | BIGINT | Set play attempts on target | Set Play On Target |
| `AttemptsfromPenaltiesontarget` | BIGINT | Penalty attempts on target | Penalty On Target |
| `AttemptsOpenPlayofftarget` | BIGINT | Open play attempts off target | Open Play Off Target |
| `AttemptsfromCornersofftarget` | BIGINT | Corner attempts off target | Corner Off Target |
| `AttemptsfromThrowsofftarget` | BIGINT | Throw-in attempts off target | Throw-In Off Target |
| `AttemptsfromDirectFreeKickofftarget` | BIGINT | Direct free kick attempts off target | Free Kick Off Target |
| `AttemptsfromSetPlayofftarget` | BIGINT | Set play attempts off target | Set Play Off Target |
| `AttemptsfromPenaltiesofftarget` | BIGINT | Penalty attempts off target | Penalty Off Target |
| **Passing Statistics** | | | |
| `TotalSuccessfulPassesAll` | BIGINT | Total successful passes including crosses and corners | Completed Passes |
| `TotalUnsuccessfulPassesAll` | BIGINT | Total unsuccessful passes | Incomplete Passes |
| `TotalSuccessfulPassesExclCrossesCorners` | BIGINT | Successful passes excluding crosses and corners | Passes Excl. Set Pieces |
| `TotalUnsuccessfulPassesExclCrossesCorners` | BIGINT | Unsuccessful passes excluding crosses and corners | Incomplete Passes Excl. Set Pieces |
| `SuccessfulPassesOwnHalf` | BIGINT | Successful passes in own half | Own Half Passes |
| `UnsuccessfulPassesOwnHalf` | BIGINT | Unsuccessful passes in own half | Own Half Incomplete |
| `SuccessfulPassesOppositionHalf` | BIGINT | Successful passes in opposition half | Opposition Half Passes |
| `UnsuccessfulPassesOppositionHalf` | BIGINT | Unsuccessful passes in opposition half | Opposition Half Incomplete |
| `SuccessfulPassesDefensivethird` | BIGINT | Successful passes in defensive third | Defensive Third Passes |
| `UnsuccessfulPassesDefensivethird` | BIGINT | Unsuccessful passes in defensive third | Defensive Third Incomplete |
| `SuccessfulPassesMiddlethird` | BIGINT | Successful passes in middle third | Middle Third Passes |
| `UnsuccessfulPassesMiddlethird` | BIGINT | Unsuccessful passes in middle third | Middle Third Incomplete |
| `SuccessfulPassesFinalthird` | BIGINT | Successful passes in final third | Final Third Passes |
| `UnsuccessfulPassesFinalthird` | BIGINT | Unsuccessful passes in final third | Final Third Incomplete |
| `SuccessfulShortPasses` | BIGINT | Successful short passes | Short Passes |
| `UnsuccessfulShortPasses` | BIGINT | Unsuccessful short passes | Incomplete Short Passes |
| `SuccessfulLongPasses` | BIGINT | Successful long passes | Long Passes |
| `UnsuccessfulLongPasses` | BIGINT | Unsuccessful long passes | Incomplete Long Passes |
| `SuccessfulFlickOns` | BIGINT | Successful flick-on passes | Flick-Ons |
| `UnsuccessfulFlickOns` | BIGINT | Unsuccessful flick-on passes | Incomplete Flick-Ons |
| `PassForward` | BIGINT | Forward passes | Forward Passes |
| `PassBackward` | BIGINT | Backward passes | Backward Passes |
| `PassLeft` | BIGINT | Passes to the left | Left Passes |
| `PassRight` | BIGINT | Passes to the right | Right Passes |
| **Crossing and Corner Statistics** | | | |
| `SuccessfulCrossesCorners` | BIGINT | Successful crosses and corners | Successful Crosses/Corners |
| `UnsuccessfulCrossesCorners` | BIGINT | Unsuccessful crosses and corners | Unsuccessful Crosses/Corners |
| `CornersTakeninclshortcorners` | BIGINT | Corners taken including short corners | Corners Taken |
| `CornersConceded` | BIGINT | Corners conceded | Corners Against |
| `SuccessfulCornersintoBox` | BIGINT | Successful corners into box | Corners Into Box |
| `UnsuccessfulCornersintoBox` | BIGINT | Unsuccessful corners into box | Corners Into Box Unsuccessful |
| `ShortCorners` | BIGINT | Short corner kicks taken | Short Corners |
| `SuccessfulCrossesLeft` | BIGINT | Successful crosses from left | Left Crosses |
| `UnsuccessfulCrossesLeft` | BIGINT | Unsuccessful crosses from left | Left Crosses Unsuccessful |
| `SuccessfulCornersLeft` | BIGINT | Successful corners from left | Left Corners |
| `UnsuccessfulCornersLeft` | BIGINT | Unsuccessful corners from left | Left Corners Unsuccessful |
| `SuccessfulCrossesCornersLeft` | BIGINT | Successful crosses and corners from left | Left Crosses/Corners |
| `UnsuccessfulCrossesCornersLeft` | BIGINT | Unsuccessful crosses and corners from left | Left Crosses/Corners Unsuccessful |
| `SuccessfulCrossesRight` | BIGINT | Successful crosses from right | Right Crosses |
| `UnsuccessfulCrossesRight` | BIGINT | Unsuccessful crosses from right | Right Crosses Unsuccessful |
| `SuccessfulCornersRight` | BIGINT | Successful corners from right | Right Corners |
| `UnsuccessfulCornersRight` | BIGINT | Unsuccessful corners from right | Right Corners Unsuccessful |
| `SuccessfulCrossesCornersRight` | BIGINT | Successful crosses and corners from right | Right Crosses/Corners |
| `UnsuccessfulCrossesCornersRight` | BIGINT | Unsuccessful crosses and corners from right | Right Crosses/Corners Unsuccessful |
| `SuccessfulCrossesCornersintheair` | BIGINT | Successful crosses and corners in the air | Aerial Crosses/Corners |
| `UnsuccessfulCrossesCornersintheair` | BIGINT | Unsuccessful crosses and corners in the air | Aerial Crosses/Corners Unsuccessful |
| `Successfulcrossesintheair` | BIGINT | Successful crosses in the air | Aerial Crosses |
| `Unsuccessfulcrossesintheair` | BIGINT | Unsuccessful crosses in the air | Aerial Crosses Unsuccessful |
| `Successfulopenplaycrosses` | BIGINT | Successful open play crosses | Open Play Crosses |
| `Unsuccessfulopenplaycrosses` | BIGINT | Unsuccessful open play crosses | Open Play Crosses Unsuccessful |
| **Throw