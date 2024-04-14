import csv
import os
from threading import Thread
from world_model import WorldModel


def in_shoot_area(opp_x, opp_y):
    return opp_x < -34 and ( 0 < opp_y < 20.16 or -20.16  < opp_y < 0)


class Log2CSV:
    def __init__(self, wm):
        self.our_name = wm.get_our_team_name()
        self.opp_name = wm.get_their_team_name()
        self.rows = self.get_row_list(wm)

    def get_row_list(self, wm):
        right_team_Score_count=0
        rows = []
        while 1 <= wm.get_cycle() < 6000:

           # if the right team has scored in this cycle we record last 100 cycles
            if wm.is_goal_cycle_right(wm.get_cycle()):
                right_team_Score_count+=1
                first_cycle=0
                last_cycle=wm.get_cycle()
                if wm.get_cycle()>100:
                    first_cycle=wm.get_cycle()-100

                for this_cycle in range(first_cycle,last_cycle+1):    
                    
                    wm.game_mode(cycle=this_cycle)
                    ball_x = wm.get_ball(this_cycle).get_x()
                    ball_y = wm.get_ball(this_cycle).get_y()
                    row = {
                           'right_team':self.opp_name,
                           'left_team':self.our_name,
                           'cycle': this_cycle,
                           'mode': wm.mode,
                           'ball_x': ball_x,
                           'ball_y': ball_y,
                           'right_team_score':right_team_Score_count,
                           'game_id':wm.file_name
                           }
                    our_players_nearest_to_ball,their_players_nearest_to_ball=wm.get_nearest_players_to_ball(this_cycle)

                    for i in range(0, 6):
                        opp_x = their_players_nearest_to_ball[i].get_x()
                        opp_y = their_players_nearest_to_ball[i].get_y()
                        row[f'opp_player_{i}_unum']=their_players_nearest_to_ball[i].get_unum()
                        row[f'opp_player_{i}_x'] = opp_x
                        row[f'opp_player_{i}_y'] = opp_y
                        row[f'opp_player_{i}_kick'] = 1 if their_players_nearest_to_ball[i].get_kick() else 0
                        row[f'opp_player_{i}_shoot'] = 1 if in_shoot_area(opp_x,opp_y) and their_players_nearest_to_ball[i].get_kick()  else 0 
                    rows.append(row)
            wm.time().add_time()
            continue
        return rows


    def init_csv(self,csv_path):
        with open(csv_path, 'w') as f:
            if len(self.rows)!=0:
               writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
               writer.writeheader()

    def append_csv(self,csv_path):
        existing_games = set()  
        
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # print(row)
                    existing_games.add((row['game_id'],int(row['right_team_score']),int(row['cycle'])))
        # print(existing_games)
        # print(existing_games.pop())
        # print(('20240403174641-ma_1-vs-RoboCIn_1', '1', '4403') in existing_games)
        with open(csv_path, 'a') as f:
                if len(self.rows)!=0:
                     writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
                     for row in self.rows:
                        #   print((row['game_id'],row['right_team_score'],row['cycle']))
                          if (row['game_id'],row['right_team_score'],row['cycle'])  not in existing_games:
                              writer.writerow(row)

SRC_DIRECTORY='/home/sana/robotic/R32D'
OUTPUT_DIRECTORY='/home/sana/robotic/advanced-log-analyzer'
def read_file(file):
    log_path = os.path.join(SRC_DIRECTORY, file) 
    wm = WorldModel(log_path)
    l2c = Log2CSV(wm)
    csv_filename = wm.right_team_name+ '.csv'
    csv_path = os.path.join(OUTPUT_DIRECTORY, csv_filename)
    if not os.path.exists(csv_path):
        l2c.init_csv(csv_path)
    l2c.append_csv(csv_path)
    print('done')


def main():
    threads = []
    for file in os.listdir(SRC_DIRECTORY): #directory_path of all .rcg/.rcl files
        if file.endswith('.rcg'):
            t = Thread(target=read_file, args=(file,))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
    print('done2')