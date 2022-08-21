import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Plot Win/Loss % for every team in the NBA for a specific period of time', epilog='by RBW')
parser.add_argument('--f', default= 2000, 
                    help='Start year for stat to be calculated (default= 2000)')
parser.add_argument('--t', default= 2022, 
                    help='End year for stat to be calculated -eg. 2022 would count 2021-2022 season (default: 2022)')
# parser.add_argument('--r', metavar='res-path', help='path for results')
args = parser.parse_args()

teams = pd.read_csv('../teams.csv')

period = teams[(teams.Year >= int(args.f)) & (teams.Year < int(args.t))]

# Get rid of * after teams that made the playoffs (data not interesting for this study)
new_period = period.copy()
new_period.Team = new_period.Team.apply(lambda t: t[:-1] if (t[-1] == '*') else t)

# Group data from period by team & sum the values to get all Wins and Losses per team
sum_info = new_period.groupby(by = 'Team').sum()
sum_info = sum_info[['W', 'L']]

# Create all data we need to calculate W/L%
data = sum_info.copy()
data['GP'] =  data.W + data.L
data['W/L%'] = data.W / data.GP
data = data.sort_values('W/L%')

fig, ax = plt.subplots()
ax.set_title('W/L%-per-teams from {}-{}'.format(int(args.f), int(args.t)))
ax.barh(data[data['W/L%'] < 0.5].index,data[data['W/L%'] < 0.5]['W/L%'], color = 'r', label = 'W/L% < 0.5')
ax.barh(data[data['W/L%'] >= 0.5].index,data[data['W/L%'] >= 0.5]['W/L%'], color = 'b', label = 'W/L% $\geq$ 0.5')
ax.legend()
plt.tight_layout()
# plt.savefig('W%-per-teams-{}-{}.pdf'.format(int(args.f), int(args.t)), bbox_inches = 'tight')
plt.show()