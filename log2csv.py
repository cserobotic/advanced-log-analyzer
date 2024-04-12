import csv
import os
from threading import Thread

from world_model import WorldModel, get_object_area


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
            if (wm.is_goal_cycle_right(wm.get_cycle())):
                right_team_Score_count+=1
                first_cycle=0
                last_cycle=wm.get_cycle()
                if wm.get_cycle()>100:
                    first_cycle=wm.get_cycle()-100

                for this_cycle in range(first_cycle,last_cycle):    
                    
                    wm.game_mode(cycle=this_cycle)
                    # tm_players, opp_players = wm.get_nearest_players_to_goalie(this_cycle)
                    row = {'right_team':self.opp_name,'left_team':self.our_name,
                        'cycle': this_cycle, 'mode': wm.mode, 'ball_x': wm.get_ball(this_cycle).get_x(),
                        'ball_y': wm.get_ball(this_cycle).get_y(),
                        # 'ball_vx': wm.get_ball(this_cycle).get_vx(),
                        # 'ball_vy': wm.get_ball(this_cycle).get_vy(),
                        # 'ball_area': get_object_area(wm.get_ball(this_cycle)),
                        # 'my_x': wm.our_player(1, this_cycle).get_x(),
                        # 'my_y': wm.our_player(1, this_cycle).get_y(), 'my_vx': wm.our_player(1, this_cycle).get_vx(),
                        # 'my_vy': wm.our_player(1, this_cycle).get_vy(),
                        # 'my_dash_power': wm.our_player(1, this_cycle).get_dash()[0] if wm.our_player(1,
                                                                                                            # this_cycle).get_dash() else 0,
                        # 'my_dash_dir': wm.our_player(1, this_cycle).get_dash()[1] if wm.our_player(1,
                                                                                                        # this_cycle).get_dash() and len(
                            # wm.our_player(1, this_cycle).get_dash()) > 1 else 0,
                        # 'my_turn': wm.our_player(1, this_cycle).get_turn(),
                        'right_team_score':right_team_Score_count}
                    our_players_nearest_to_ball,their_players_nearest_to_ball=wm.get_nearest_players_to_ball(this_cycle)
                    for i in range(0, 6):
                        row[f'opp_player_{i}_unum']=their_players_nearest_to_ball[i].get_unum()
                        row[f'opp_player_{i}_x'] = their_players_nearest_to_ball[i].get_x()
                        row[f'opp_player_{i}_y'] = their_players_nearest_to_ball[i].get_y()
                        row[f'opp_player_{i}_kick'] = 1 if their_players_nearest_to_ball[i].get_kick() else 0

                    # for i in range(0, 6):
                    #     row[f'tm_player_{i}_x'] = tm_players[i].get_x()
                    #     row[f'tm_player_{i}_y'] = tm_players[i].get_y()
                    #     row[f'tm_player_{i}_vx'] = tm_players[i].get_vx()
                    #     row[f'tm_player_{i}_vy'] = tm_players[i].get_vy()
                    #     row[f'tm_player_{i}_kick'] = 1 if tm_players[i].get_kick() else 0
                    #     row[f'tm_player_{i}_dist'] = tm_players[i].dist(wm.our_player(1, this_cycle))
                    #     row[f'tm_player_{i}_area'] = get_object_area(tm_players[i])

                    # for i in range(0, 6):
                    #     row[f'opp_player_{i}_x'] = opp_players[i].get_x()
                    #     row[f'opp_player_{i}_y'] = opp_players[i].get_y()
                    #     row[f'opp_player_{i}_vx'] = opp_players[i].get_vx()
                    #     row[f'opp_player_{i}_vy'] = opp_players[i].get_vy()
                    #     row[f'opp_player_{i}_kick'] = 1 if opp_players[i].get_kick() else 0
                    #     row[f'opp_player_{i}_dist'] = opp_players[i].dist(wm.our_player(1, this_cycle))
                    #     row[f'opp_player_{i}_area'] = get_object_area(opp_players[i])
                    rows.append(row)
            wm.time().add_time()
            continue
            
            # if wm.get_ball(wm.get_cycle()).get_x() > -25:
            #     wm.time().add_time()
            #     continue

            # wm.game_mode(cycle=wm.get_cycle())
            # tm_players, opp_players = wm.get_nearest_players_to_goalie(wm.get_cycle())
            # row = {'right_team':self.opp_name,'left_team':self.our_name,
            #       'cycle': wm.get_cycle(), 'mode': wm.mode, 'ball_x': wm.get_ball(wm.get_cycle()).get_x(),
            #        'ball_y': wm.get_ball(wm.get_cycle()).get_y(), 'ball_vx': wm.get_ball(wm.get_cycle()).get_vx(),
            #        'ball_vy': wm.get_ball(wm.get_cycle()).get_vy(),
            #        'ball_area': get_object_area(wm.get_ball(wm.get_cycle())),
            #        'my_x': wm.our_player(1, wm.get_cycle()).get_x(),
            #        'my_y': wm.our_player(1, wm.get_cycle()).get_y(), 'my_vx': wm.our_player(1, wm.get_cycle()).get_vx(),
            #        'my_vy': wm.our_player(1, wm.get_cycle()).get_vy(),
            #        'my_dash_power': wm.our_player(1, wm.get_cycle()).get_dash()[0] if wm.our_player(1,
            #                                                                                         wm.get_cycle()).get_dash() else 0,
            #        'my_dash_dir': wm.our_player(1, wm.get_cycle()).get_dash()[1] if wm.our_player(1,
            #                                                                                       wm.get_cycle()).get_dash() and len(
            #            wm.our_player(1, wm.get_cycle()).get_dash()) > 1 else 0,
            #        'my_turn': wm.our_player(1, wm.get_cycle()).get_turn(),
           #}

            # for i in range(0, 6):
            #     row[f'tm_player_{i}_x'] = tm_players[i].get_x()
            #     row[f'tm_player_{i}_y'] = tm_players[i].get_y()
            #     row[f'tm_player_{i}_vx'] = tm_players[i].get_vx()
            #     row[f'tm_player_{i}_vy'] = tm_players[i].get_vy()
            #     row[f'tm_player_{i}_kick'] = 1 if tm_players[i].get_kick() else 0
            #     row[f'tm_player_{i}_dist'] = tm_players[i].dist(wm.our_player(1, wm.get_cycle()))
            #     row[f'tm_player_{i}_area'] = get_object_area(tm_players[i])

            # for i in range(0, 6):
            #     row[f'opp_player_{i}_x'] = opp_players[i].get_x()
            #     row[f'opp_player_{i}_y'] = opp_players[i].get_y()
            #     row[f'opp_player_{i}_vx'] = opp_players[i].get_vx()
            #     row[f'opp_player_{i}_vy'] = opp_players[i].get_vy()
            #     row[f'opp_player_{i}_kick'] = 1 if opp_players[i].get_kick() else 0
            #     row[f'opp_player_{i}_dist'] = opp_players[i].dist(wm.our_player(1, wm.get_cycle()))
            #     row[f'opp_player_{i}_area'] = get_object_area(opp_players[i])

            # rows.append(row)
            # wm.time().add_time()
        return rows

    def init_csv(self,csv_path):
        with open(csv_path, 'w') as f:
            if (len(self.rows)!=0):
               writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
               writer.writeheader()

    def append_csv(self,csv_path):
        with open(csv_path, 'a') as f:
            if (len(self.rows)!=0):
                writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
                # writer.writerow(None)
                writer.writerows(self.rows)

SRC_DIRECTORY='/home/sana/robotic/R32D/src'
OUTPUT_DIRECTORY='/home/sana/robotic/advanced-log-analyzer'
def read_file(file):
    log_path = os.path.join(SRC_DIRECTORY, file) 
    wm = WorldModel(log_path)
    l2c = Log2CSV(wm)
    csv_filename = os.path.splitext(file)[0] + '.csv'
    csv_path = os.path.join(OUTPUT_DIRECTORY, csv_filename)
    if not os.path.exists(csv_path):
        l2c.init_csv(csv_path)
    l2c.append_csv(csv_path)


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
