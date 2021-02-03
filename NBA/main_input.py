from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog, teamgamelog, playernextngames, leaguestandings
import statistics

r = 0
Play = [
"DeMar DeRozan"
]
li = [
18.5
]
for pl in Play:
    Line = li[r]
    name = pl
    the_factor = 'null'
    player_dict = players.get_active_players()
    for player in player_dict:
        if player['full_name'] == name:
            the_factor = player['id']

    gamelog = playergamelog.PlayerGameLog(player_id = the_factor, season = '2020')
    df = gamelog.get_data_frames()

    str_matchup = str(df[0].MATCHUP[0])
    str_matchup = str_matchup[:-2]
    the_team_factor = 'null'
    team_dict = teams.get_teams()
    for team in team_dict:
        if team['abbreviation'] in str_matchup:
            the_team_factor = team['id']

    team_game_log = teamgamelog.TeamGameLog(team_id=the_team_factor, season='2020')
    tdf = team_game_log.get_data_frames()

    next_games = playernextngames.PlayerNextNGames(player_id=the_factor, number_of_games='1')
    ndf = next_games.get_data_frames()

    oppo_stats = leaguestandings.LeagueStandings(league_id='00', season='2020')
    odf = oppo_stats.get_data_frames()

    PTS = df[0].PTS
    def PTS_TO_LINE(PTS, line):
        avg = sum(PTS) / len(PTS)
        std = statistics.stdev(PTS)
        if line < avg and line > avg - std:
            probability_index = + 1
        elif line < avg - std:
            probability_index = + 2
        elif line > avg and line < avg + std:
            probability_index = - 1
        else:
            probability_index = - 2

        return probability_index

    def HISTORY(line):
        points = 0
        probibility_index = 0
        a = 0
        T = False
        homeID = ndf[0].HOME_TEAM_ID
        awayID = ndf[0].VISITOR_TEAM_ID
        HOM_ABBR = str(ndf[0].HOME_TEAM_ABBREVIATION)
        HOM_ABBR = HOM_ABBR[5:-47]
        VIS_ABBR = str(ndf[0].VISITOR_TEAM_ABBREVIATION)
        VIS_ABBR = VIS_ABBR[5:-47]
        if str(tdf[0].Team_ID[0]) not in str(homeID):
            for match in df[0].MATCHUP:
                if str(HOM_ABBR) in str(match):
                    points = df[0].PTS[a]
                    T = True
                a = a + 1
            if T == True:
                if line < points:
                    probibility_index = + 1
                else:
                    probibility_index = - 1

        if str(tdf[0].Team_ID[0]) not in str(awayID):
            for match in df[0].MATCHUP:
                if str(VIS_ABBR) in str(match):
                    points = df[0].PTS[a]
                    T = True
                a = a + 1
            if T == True:
                if line < points:
                    probibility_index = + 1
                else:
                    probibility_index = - 1

        return probibility_index

    def SHOT_PER():
        shots = sum(df[0].FGA)/len(df[0].FGA)
        team_shots = sum(tdf[0].FGA)/len(tdf[0].FGA)
        per = shots/team_shots
        if per >= .18:
            probibility_index = 1
        elif per >= .23:
            probibility_index = 2
        elif per < .18 and per > .10:
            probibility_index = 0
        else:
            probibility_index = -2
        return probibility_index


    def TRUE_SHOOTING():
        avg_pts_last_3 = (df[0].PTS[0] +  df[0].PTS[1] +  df[0].PTS[2]) / 3
        avg_fga_last_3 = (df[0].FGA[0] + df[0].FGA[1] + df[0].FGA[2]) / 3
        avg_fta_last_3 = (df[0].FTA[0] + df[0].FTA[1] + df[0].FTA[2]) / 3
        true_shooting = (avg_pts_last_3 / (2*(avg_fga_last_3 + (.44 * avg_fta_last_3))))*1
        if true_shooting > .50:
            probibility_index = 1
        elif true_shooting > .60:
            probibility_index = 2
        elif true_shooting < .49 and true_shooting > .40:
            probibility_index = -1
        else:
            probibility_index = -2
        return probibility_index


    def OPPO_STATS():
        a = 0
        opp = 0
        homeID = ndf[0].HOME_TEAM_ID
        awayID = ndf[0].VISITOR_TEAM_ID
        if str(homeID) == str(tdf[0].Team_ID[0]):
            OPPO_TEAM = awayID
        else:
            OPPO_TEAM = homeID
        for team in odf[0].TeamID:
            if str(team) in str(OPPO_TEAM):
                opp = odf[0].OppPointsPG[a]
            a = a + 1
        if opp < 108:
            probibility_index = -1
        elif opp > 115:
            probibility_index = 1
        else:
            probibility_index = 0
        return probibility_index

    x1 = PTS_TO_LINE(PTS, Line)
    x2 = HISTORY(Line)
    x3 = SHOT_PER()
    x4 = TRUE_SHOOTING()
    x5 = OPPO_STATS()
    prob_index = x1 + x2 + x3 + x4 + x5


    print(name)
    print(prob_index)
    r = r + 1