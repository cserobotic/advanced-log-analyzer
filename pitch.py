import csv
import matplotlib.pyplot as plt
import pandas as pd
import os


CSV_DIRECTORY = '/home/sana/robotic/advanced-log-analyzer'

def process_csv_file(filename):
    df = pd.read_csv(filename)
    if df.empty:
        return None
    grouped = df.groupby('right_team_score')
    result = []
    
    for group_name, group_data in grouped:
        group_data = group_data.reset_index(drop=True) 
        group_dict = group_data.to_dict('records')  # group dict is a list of dictionaries, each dict is a cycle
        # print(type(group_dict))
        result.append(group_dict)  
    
    return result


def get_unum_last_kicker(last_100_cycles:list):
    kicker_unum=-1
    for cycle in last_100_cycles[::-1]:
        if cycle['opp_player_0_kick']==1:
            kicker_unum=cycle['opp_player_0_unum']
            return kicker_unum
        
    return -1
       

def get_kicker_moves(player_unum:int,last_100_cycles:list):
    print(player_unum)
    kicker_x=[]
    kicker_y=[]
    for cycle in last_100_cycles:
        if cycle['opp_player_0_unum']==player_unum:
            kicker_x.append(cycle['opp_player_0_x'])
            kicker_y.append(cycle['opp_player_0_y'])
        elif cycle['opp_player_1_unum']==player_unum:
             kicker_x.append(cycle['opp_player_1_x'])
             kicker_y.append(cycle['opp_player_1_y'])
        elif cycle['opp_player_2_unum']==player_unum:
             kicker_x.append(cycle['opp_player_2_x'])
             kicker_y.append(cycle['opp_player_2_y'])
        elif cycle['opp_player_3_unum']==player_unum:
            kicker_x.append(cycle['opp_player_3_x'])
            kicker_y.append(cycle['opp_player_3_y'])
        elif cycle['opp_player_4_unum']==player_unum:
            kicker_x.append(cycle['opp_player_4_x'])
            kicker_y.append(cycle['opp_player_4_y'])
        elif cycle['opp_player_5_unum']==player_unum:
             kicker_x.append(cycle['opp_player_5_x'])
             kicker_y.append(cycle['opp_player_5_y'])
    return kicker_x,kicker_y

def get_ball_moves(last_100_cycles:list):
    ball_x = [float(position['ball_x'])  for position in last_100_cycles]
    ball_y = [float(position['ball_y'])  for position in last_100_cycles]
    return ball_x,ball_y


def draw_football_ground(p_unum,kicker_x,kicker_y,ball_x,ball_y,right_team,left_team,image_path):
    fig, ax = plt.subplots()
    # ax.set_aspect('equal')

    ax.plot(ball_x, ball_y,'g--', linewidth=1 ,label='ball')
    ax.plot(kicker_x,kicker_y,'r--',linewidth=1, label='kicker')
    for i, (x, y) in enumerate(zip(ball_x, ball_y)):
         if i<=3 or i==len(ball_x)-1:
           ax.text(x, y, str(i), ha='center', va='bottom')
    for i, (x, y) in enumerate(zip(kicker_x, kicker_y)):
         if i==0 or i==len(kicker_x)-1:
           ax.text(x, y, str(i), ha='center', va='bottom')
    ax.plot([0, 0], [-34, 34], color='white')
    ax.plot([-52.5,-47],[-9,-9],color='white')
    ax.plot([-52.5,-47],[9,9],color='white')
    ax.plot([-47,-47],[-9,9],color='white')
    ax.set_xlim(-52.5, 52.5)
    ax.set_ylim(-34, 34)
    ax.set_facecolor('lightgreen')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Football Ground {left_team}-{right_team}, right team kicker is: {p_unum}')
    plt.legend()
    plt.draw()
    plt.savefig(image_path)
    plt.show()
    plt.close()


def main():
    for filename in os.listdir(CSV_DIRECTORY):
        if filename.endswith('.csv'):
            print(filename)
            csv_path = os.path.join(CSV_DIRECTORY, filename)
            groups = process_csv_file(csv_path)
            if groups:
                print('yes')
                for group in groups:
                    p_unum = get_unum_last_kicker(group)
                    kicker_x, kicker_y = get_kicker_moves(p_unum, group)
                    ball_x, ball_y = get_ball_moves(group)
                    right_team = group[0]['right_team']
                    left_team = group[0]['left_team']
                    image_path=os.path.join(CSV_DIRECTORY, os.path.splitext(filename)[0] + '.png')
                    draw_football_ground(p_unum, kicker_x, kicker_y, ball_x, ball_y, right_team, left_team,image_path)



if __name__ == '__main__':
    main()
