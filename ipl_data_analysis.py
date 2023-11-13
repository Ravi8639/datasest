import csv
from matplotlib import pyplot as plt

scores_by_team = {}
id_to_year = {}
batsman_runs = {}
umpire_country = {}
total_umpires = set()
winner_by_team = {}
matches_by_team = {}
matches_by_season = {}
extra_runs_team = {}
balls_bowled = {}
runs_conceded = {}



        
def team():
    with open("data/umpires.csv", encoding="utf-8") as csv_file:
        umpires_reader = csv.DictReader(csv_file)
        for umpires in umpires_reader:
            if umpires["umpire"] != "":
                umpire_country[umpires["umpire"]] = umpires["country"]

                
    with open("data/matches.csv",  encoding="utf-8") as csv_file:
        matches_reader = csv.DictReader(csv_file)
        for matches in matches_reader:
            id_to_year[matches["id"]] = int(matches["season"])
            total_umpires.add(matches["umpire1"])
            total_umpires.add(matches["umpire2"])
            
            
            # matches by team
            if matches["team1"] not in matches_by_team:
                games_by_season = {"2008":0, "2009":0, "2010":0, "2011":0, "2012":0, "2013":0, "2014":0,
                                  "2015":0, "2016":0, "2017":0}
                games_by_season[matches["season"]] += 1
                matches_by_team[matches["team1"]] = games_by_season
            else:
                if matches["season"] not in matches_by_team[matches["team1"]]:
                    matches_by_team[matches["team1"]][matches["season"]] = 1
                else:
                    matches_by_team[matches["team1"]][matches["season"]] += 1
            if matches["team2"] not in matches_by_team:
                games_by_season = {"2008":0, "2009":0, "2010":0, "2011":0, "2012":0, "2013":0, "2014":0,
                                  "2015":0, "2016":0, "2017":0}
                games_by_season[matches["season"]] += 1
                matches_by_team[matches["team2"]] = games_by_season
            else:
                if matches["season"] not in matches_by_team[matches["team1"]]:
                    matches_by_team[matches["team1"]][matches["season"]] = 1
                else:
                    matches_by_team[matches["team1"]][matches["season"]] += 1
                    
                    
            # number of matches played evry year
            if int(matches["season"]) not in matches_by_season:
                matches_by_season[int(matches["season"])] = 1
            else:
                matches_by_season[int(matches["season"])] += 1
                
                
            # number of macthes won by ateam per year
            if matches["winner"] not in winner_by_team:
                game_by_season = {'2008': 0, '2009': 0, '2010': 0, '2011': 0,
                                  '2012': 0, '2013': 0, '2014': 0, '2015': 0, '2016': 0, '2017': 0}
                game_by_season[matches["season"]] += 1
                winner_by_team[matches["winner"]] = game_by_season
            else:
                if matches["season"] not in winner_by_team[matches["winner"]]:
                    winner_by_team[matches["winner"]][matches["season"]] = 1
                else:
                    winner_by_team[matches["winner"]][matches["season"]] += 1
                    
                
        
    with open("data/deliveries.csv", encoding="utf-8") as csv_file:
        deliveries_reader = csv.DictReader(csv_file)
        for matches in deliveries_reader:
            if matches["batting_team"] not in scores_by_team:
                year_to_runs = {id_to_year[matches["match_id"]]:int(matches["total_runs"])}
                scores_by_team[matches["batting_team"]] = year_to_runs
            else:
                if id_to_year[matches["match_id"]] not in scores_by_team[matches["batting_team"]]:
                    scores_by_team[matches["batting_team"]][id_to_year[matches["match_id"]]] = int(matches["total_runs"])
        
                else:
                    scores_by_team[matches["batting_team"]][id_to_year[matches["match_id"]]] += int(matches["total_runs"])
                    
                             
            # top ten batsman from royal challengers Bangalore
            if matches["batting_team"] == "Royal Challengers Bangalore":
                if matches["batsman"] not in batsman_runs:
                    batsman_runs[matches["batsman"]] = int(matches["total_runs"])
                else:
                    batsman_runs[matches["batsman"]] += int(matches["total_runs"])
                    
                    
            # Extra runs conceded per team in the year 2016
            if id_to_year[matches["match_id"]] == 2016:
                if matches["bowling_team"] not in extra_runs_team:
                    extra_runs_team[matches["bowling_team"]] = int(matches["extra_runs"])
                else:
                    extra_runs_team[matches["bowling_team"]] += int(matches["extra_runs"])
                    
                    
            #top 10 economical bowlers in 2015
            if id_to_year[matches["match_id"]] == 2015:
                if matches["bowler"] not in balls_bowled:
                    balls_bowled[matches["bowler"]] = 1
                else:
                    balls_bowled[matches["bowler"]] += 1
                if matches["bowler"] not in runs_conceded:
                    runs_conceded[matches["bowler"]] = int(matches["total_runs"])
                else:
                    runs_conceded[matches["bowler"]] += int(matches["total_runs"])
                    
                

                                               
                
def plot_total_runs():
   
    """Plots total tuns scored by teams over the years in form of a line chart"""
    # print(scores_by_team)
    for team in scores_by_team.items():
        x_axis = list(team[1].keys())
        y_axis = list(team[1].values())
        x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis)))
        plt.plot(x_axis, y_axis, label=team[0])
    plt.xlabel("Years")
    plt.ylabel("Total Runs")
    plt.title("Total runs scored by Teams over the years")
    plt.legend()
    plt.show()   


def plot_top_batsman():    
    """Plots the top ten runscore batsman over the history of ipl"""   
    batsman = list(batsman_runs.keys())
    runs = list(batsman_runs.values())
    runs, batsman = zip(*sorted(zip(runs,batsman),reverse=True))
    batsman = list(batsman[:10])
    runs = list(runs[:10])
    plt.bar(batsman,runs, width=0.3)
    plt.xlabel("batsman")
    plt.ylabel("runs")
    plt.title("Top 10 batsman of RCB in the history of IPL")
    plt.show()

def umpires_by_country():
    country_count = {}
    for i in total_umpires:
        if i == "":
            continue
        if umpire_country[i] == "":
            continue
        if umpire_country[i] != " India":
            if umpire_country[i] not in country_count:
                country_count[umpire_country[i]] = 1
            else:
                country_count[umpire_country[i]] += 1
    print(country_count)
    x_axis = list(country_count.keys())
    y_axis = list(country_count.values())
    plt.bar(x_axis,y_axis,width=0.3)
    plt.xlabel("Countries")
    plt.ylabel("Umpires Count")
    plt.title("umpires By Country")
    plt.show()

def add_two_lists(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Lists must have the same length for element-wise addition.")
    
    result = [x + y for x, y in zip(list1, list2)]
    return result 

def games_by_season():
    team_list = list(matches_by_team.keys())
    baseline = [0]*10
    for team in matches_by_team.items():
        seasons = list(team[1].keys())
        matches = list(team[1].values())
        seasons, matches =zip(*sorted(zip(seasons, matches)))
        plt.bar(seasons, matches, bottom=baseline)
        baseline = add_two_lists(baseline,matches)
        print(matches)
        print(baseline)
    plt.xlabel("Seasons")
    plt.ylabel("Matches")
    plt.legend(team_list)
    plt.show()
            

def games_every_year():
    x_axis = list(matches_by_season.keys())
    y_axis = list(matches_by_season.values())
    plt.bar(x_axis,y_axis)
    plt.xlabel("Years")
    plt.ylabel("matches")   
    plt.title("Matches played every year over history of  IPL")
    plt.show() 

        
def matches_won_per_team_by_year():
    team_list = list(winner_by_team.keys())
    baseline = [0]*10
    for team in winner_by_team.items():
        x_axis = list(team[1].keys())
        y_axis = list(team[1].values())
        x_axis, y_axis = zip(*sorted(zip(x_axis,y_axis)))
        plt.bar(x_axis,y_axis, bottom=baseline)
        baseline = add_two_lists(baseline,y_axis)
    plt.xlabel("Year")
    plt.ylabel("macthes")
    plt.title("Matches won by a team per year")
    plt.legend(team_list)
    plt.show()

                   
def extra_runs():
    x_axis = list(extra_runs_team.keys())
    y_axis = list(extra_runs_team.values())
    plt.bar(x_axis,y_axis, width=0.3)
    plt.xlabel("bowling_teams in 2016")
    plt.ylabel("extra_runs")
    plt.title("Extra runs conceded by bowling team in 2016")
    plt.show()

def economical_rate():
    bolwer_economic_rate = {}
    for balls in balls_bowled.items():
        bolwer_economic_rate[balls[0]] = (runs_conceded[balls[0]]/balls_bowled[balls[0]])*6
    bowlers = list(bolwer_economic_rate.keys())
    economic_rate = list(bolwer_economic_rate.values())
    economic_rate, bowlers = zip(*sorted(zip(economic_rate, bowlers)))
    x_axis = bowlers[:10]
    y_axis = economic_rate[:10]
    plt.bar(x_axis, y_axis)
    plt.xlabel("Bolwers")
    plt.ylabel("Economic rate ")
    plt.title("Economy rate of top 10 bowlers")
    plt.show()


def main():
    """main function"""
    team()
    while True:
        print("Please Enter the corresponding number to select an option: ")
        print("1. Plot a chart of total runs scored by each teams over the history of IPL")
        print("2. Plot the total runs scored by top 10 batsmen",
              "playing for Royal Challengers Bangalore")
        print("3. Plot a chart of umpires by country (Ignoring",
              "Indian umpires since they would dominate the charts)")
        print("4. Plot a stacked bar chart of number of games played: by team and by season")
        print("5. Plot of a bar chart of number of",
              "matches played per year for all the years in IPL.")
        print("6. Plot a stacked bar chart of number of matches won per team per year in IPL.")
        print("7. Plot a bar chart of Extra runs conceded per team in the year 2016")
        print("8. Plot a bar chart of top 10 economical bowlers in the year 2015")
        print("Press any other number to exit")
        choice = int(input())
        if choice == 1:
            plot_total_runs()
        elif choice == 2:
            plot_top_batsman()
        elif choice == 3:
            umpires_by_country()
        elif choice == 4:
            games_by_season()
        elif choice == 5:
            games_every_year()
        elif choice == 6:
            matches_won_per_team_by_year()
        elif choice == 7:
            extra_runs()
        elif choice == 8:
            economical_rate()
        else:
            break
main()