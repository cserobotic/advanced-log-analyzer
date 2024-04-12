import csv
import matplotlib.pyplot as plt
import pandas as pd
import os


CSV_DIRECTORY = '/home/sana/robotic/advanced-log-analyzer'

def process_csv_file(filename):
    print(filename)
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

def get_shoot_kick_coordinate(last_100_cycles:list):
    shoot_data = {"unum": [], "x": [], "y": []}
    kick_data = {"unum": [], "x": [], "y": []}

    for cycle in last_100_cycles:
        if cycle["opp_player_0_shoot"] == 1:
            shoot_data["unum"].append(cycle["opp_player_0_unum"])
            shoot_data["x"].append(cycle["opp_player_0_x"])
            shoot_data["y"].append(cycle["opp_player_0_y"])
        elif cycle["opp_player_0_kick"] == 1:
            kick_data["unum"].append(cycle["opp_player_0_unum"])
            kick_data["x"].append(cycle["opp_player_0_x"])
            kick_data["y"].append(cycle["opp_player_0_y"])
    return shoot_data,kick_data


def draw_football_ground(p_unum,kicker_x,kicker_y,ball_x,ball_y,right_team,left_team,image_path,shoot_data,kick_data):
    fig, ax = plt.subplots()
    # ax.set_aspect('equal')


    #draw ball path
    cmap = plt.get_cmap('viridis')
    for i in range(len(ball_x) - 1):
        x_start, y_start = ball_x[i], ball_y[i]
        x_end, y_end = ball_x[i + 1], ball_y[i + 1]
        color = cmap(i / len(ball_x))
        ax.plot([x_start, x_end], [y_start, y_end], linewidth=1, color=color)


    plt.scatter(kick_data["x"], kick_data["y"], color='hotpink',s=80, label='potential Pass')
    plt.scatter(shoot_data["x"], shoot_data["y"], color='red',s=60, label='Shoot')
    for i, txt in enumerate(kick_data["unum"]):
         plt.annotate(txt, (kick_data["x"][i], kick_data["y"][i]),  ha='center',fontsize=12)

    for i, txt in enumerate(shoot_data["unum"]):
          plt.annotate(txt, (shoot_data["x"][i], shoot_data["y"][i]),  ha='center',fontsize=12)

    ax.plot([0, 0], [-34, 34], color='white')
    ax.plot([-52.5,-47],[-9,-9],color='white')
    ax.plot([-52.5,-47],[9,9],color='white')
    ax.plot([-47,-47],[-9,9],color='white')
    ax.set_xlim(-53.5, 53.5)
    ax.set_ylim(-35, 35)
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
                    shoot_data,kick_data=get_shoot_kick_coordinate(group)
                    image_path=os.path.join(CSV_DIRECTORY, os.path.splitext(filename)[0] + '.png')
                    draw_football_ground(p_unum, kicker_x, kicker_y, ball_x, ball_y, right_team, left_team,image_path,shoot_data,kick_data)



if __name__ == '__main__':
    main()
