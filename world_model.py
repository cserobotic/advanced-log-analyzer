import re

FULL_STATE_TIME = 6000


def get_object_area(obj):
    penalty_area = Rect2D(Vector2D(-52.5, -20), Vector2D(-36, 20))
    left_corner_area = Rect2D(Vector2D(-52.5, -34), Vector2D(-36, -20))
    right_corner_area = Rect2D(Vector2D(-52.5, 20), Vector2D(-36, 34))
    upper_penalty_area = Rect2D(Vector2D(-36, -34), Vector2D(-25, 34))

    if penalty_area.is_point_in(obj):
        return 3
    elif left_corner_area.is_point_in(obj) or right_corner_area.is_point_in(obj):
        return 2
    elif upper_penalty_area.is_point_in(obj):
        return 1
    return 0


class WorldModel:

    def __init__(self, file_path):

        self.playmode = []
        self.rcg = []
        self.rcg.append("(show 0 ((b) 0.000 0.000")
        self.right_scored=[]
        self.left_scored=[]

        self.rcl_l = [[None for j in range(12)]
                      for i in range(FULL_STATE_TIME + 1)]
        self.rcl_r = [[None for j in range(12)]
                      for i in range(FULL_STATE_TIME + 1)]

        self.file_path = file_path
        self.file_name = file_path.split("/")[-1].split(".")[0]
        self.left_team_name =         re.split(
        "_[0-9]+", re.split("^[0-9]+-", self.file_name.split("-vs-")[0])[1])[0]  # ^[0-9]+-  yz modify
        # re.split(
        # "_[0-9]+", re.split("^[0-9]+-", self.file_name.split("-vs-")[0])[1])[0]  # ^[0-9]+-  yz modify
        self.right_team_name =   re.split(
            "_[0-9]+", self.file_name.split("-vs-")[1])[0]
        # re.split(
        #     "_[0-9]+", self.file_name.split("-vs-")[1])[0]

        # self.left_team_score = int(self.file_name.split(
        #     "-vs-")[0].split(self.left_team_name + "_")[1])

        # self.right_team_score = int(self.file_name.split(
        #     "-vs-")[1].split(self.right_team_name + "_")[1])

        self.game_time = GameTime(0, 6000)
        # print(self.right_team_name)
        # print(self.left_team_name)
        self.last_kicker_side = "left"

        self.mode = 'before_kick_off_l'

        rcgfile = file_path[0:-3] + "rcg"
        rclfile = file_path[0:-3] + "rcl"

        with open(rcgfile, 'r') as rcg:
            for line in rcg:
                if "show" in line and int(self.rcg[-1].split(" ")[1]) < int(line.split(" ")[1]):
                    self.rcg.append(line)
                    self.game_time.game_time += 1
                    if int(self.rcg[-1].split(" ")[1]) == 2999:
                        self.rcg.append("(show 3000 ((b) 0.000 0.000")
                        self.game_time.game_time += 1

                elif "playmode" in line:
                    mode = line.split(" ")[2].split(")")[0]
                    cycle = int(line.split(" ")[1])
                    self.playmode.append([cycle, mode])

            self.game_time.t_over = self.time().cycle()

            # error handling
            if self.ball() is None:
                self.game_time.t_over -= 1

            # reset cycle count
            self.time().reset_time()

        with open(rclfile, 'r') as rcl:
            for line in rcl:
                if int(line.split(',')[0]) >= 1:
                    rcl_cycle = int(line.split(',')[0])

                    action = {'kick': None, 'dash': None, 'catch': None, 'turn': None, 'turn_neck': None,
                              'change_view': None, 'tackle': None, 'attentionto': None, 'say': None, 'pointto': None}

                    if self.left_team_name+"_" in line and not "Coach" in line:
                        # print(line)
                        rcl_unum = int(line.split(self.left_team_name)[1].split(": ")[0].split("_")[1])
                        # if rcl_cycle >= 6000 or rcl_cycle == 3000:
                        if  rcl_cycle == 3000 or rcl_cycle>=6000:
                            if rcl_cycle<=6000:
                                self.rcl_l[rcl_cycle][rcl_unum] = PlayerObject(_unum=rcl_unum, action=action, team="left")
                            continue

                        rcl_action = line.split(self.left_team_name)[1].split(": ")[1]

                        pattern = " \(\(l [0-9]+\) "
                        match = self.rcg[rcl_cycle]
                        player_x = float(re.split(pattern, match)[rcl_unum].split(" ")[2])
                        player_y = float(re.split(pattern, match)[rcl_unum].split(" ")[3])
                        player_vx = float(re.split(pattern, match)[rcl_unum].split(" ")[4])
                        player_vy = float(re.split(pattern, match)[rcl_unum].split(" ")[5])
                        action = self.parse_rcl_actions(rcl_action, action)

                        self.rcl_l[rcl_cycle][rcl_unum] = PlayerObject(x=player_x, y=player_y, vx=player_vx,
                                                                       vy=player_vy, _unum=rcl_unum, action=action,
                                                                       team="left")

                    elif self.right_team_name+"_" in line and not "Coach" in line:
                        # print(line)
                        rcl_unum = int(line.split(self.right_team_name)[1].split(": ")[0].split("_")[1])

                        # if rcl_cycle >= 6000 or rcl_cycle == 3000:
                        if  rcl_cycle == 3000 or rcl_cycle>=6000:
                            if rcl_cycle<=6000:
                                self.rcl_r[rcl_cycle][rcl_unum] = PlayerObject(_unum=rcl_unum, action=action, team="right")
                            continue

                        rcl_action = line.split(self.right_team_name)[1].split(": ")[1]

                        pattern = " \(\(r [0-9]+\) "
                        match = self.rcg[rcl_cycle]
                        player_x = float(re.split(pattern, match)[rcl_unum].split(" ")[2])
                        player_y = float(re.split(pattern, match)[rcl_unum].split(" ")[3])
                        player_vx = float(re.split(pattern, match)[rcl_unum].split(" ")[4])
                        player_vy = float(re.split(pattern, match)[rcl_unum].split(" ")[5])

                        action = self.parse_rcl_actions(rcl_action, action)
                        self.rcl_r[rcl_cycle][rcl_unum] = PlayerObject(x=player_x, y=player_y, vx=player_vx,
                                                                       vy=player_vy, _unum=rcl_unum, action=action,
                                                                       team="right")
                    #if the right team scored a goal in the gial we should save the cycle    
                    elif "referee goal_r" in line:
                        self.right_scored.append(rcl_cycle)
                    elif "referee goal_l" in line:
                        self.left_scored.append(rcl_cycle)
                    
                        # print(line)
        print("World Model init done!")

    @staticmethod
    def parse_rcl_actions(rcl_action, action):
        if 'kick' in rcl_action:
            action['kick'] = [rcl_action.split('kick')[1].split(' ')[1],
                              rcl_action.split('kick')[1].split(' ')[2].split(')')[0]]
        if 'dash' in rcl_action:
            dash_power=list(map(float,rcl_action.split('dash')[1].split(')')[0].strip().split(' ')))
            # print(dash_power)
            # print(rcl_action)
            action['dash']=dash_power
            # action['dash'] = [float(rcl_action.split('dash')[1].split(' ')[1].split(')')[0])] if '(' in \
            #                                                                                      rcl_action.split(
            #                                                                                          'dash')[
            #                                                                                          1].split(' ')[
            #                                                                                          1] else [
            #     float(rcl_action.split('dash')[1].split(' ')[1]),
            #     float(rcl_action.split('dash')[1].split(' ')[2].split(')')[0])]
        if 'catch' in rcl_action:
            action['catch'] = float(rcl_action.split('catch')[1].split(' ')[1].split(')')[0])
        if 'turn_neck' in rcl_action:
            action['turn_neck'] = float(rcl_action.split('turn_neck')[1].split(' ')[1].split(')')[0])
        if 'pointto' in rcl_action:
            action['pointto'] = rcl_action.split('pointto')[1].split(' ')[1].split(')')[0]
        if 'say' in rcl_action:
            action['say'] = rcl_action.split('say')[1].split(' ')[1].split(')')[0].split('"')[1]
        if 'turn' in rcl_action:
            action['turn'] = float(rcl_action.split('turn')[1].split(' ')[1].split(')')[0])
        if 'tackle' in rcl_action:
            action['tackle'] = ' '.join(rcl_action.split('tackle')[1].split(' ')[1:]).split(')')[0]
        if 'change_view' in rcl_action:
            action['change_view'] = rcl_action.split('change_view')[1].split(' ')[1].split(')')[0]
        if 'attentionto' in rcl_action:
            action['attentionto'] = \
                " ".join(rcl_action.split('attentionto')[1].split(' ')[1:]).split(')')[0]
        return action

    def time(self):
        return self.game_time

    def is_goal_cycle_right(self,cycle):
        return cycle in self.right_scored
        # return cycle in self.right_scored
    def is_goal_cycle_left(self,cycle):
        return cycle in self.left_scored
        # return cycle in self.right_scored
    
    def ball(self, cycle=0):
        if cycle == 0:
            cycle = self.game_time.cycle()

        if len(self.rcg) <= cycle:
            return None

        ball_x = float(self.rcg[cycle].split("((b) ")[1].split(" ")[0])
        ball_y = float(self.rcg[cycle].split("((b) ")[1].split(" ")[1])

        ball_vx = float(self.rcg[cycle].split("((b) ")[1].split(" ")[2])
        ball_vy = float(self.rcg[cycle].split("((b) ")[1].split(" ")[3][0:-1])

        return Ball(ball_x, ball_y, ball_vx, ball_vy)

    def game_mode(self, cycle):
        for i in self.playmode:
            if i[0] <= cycle:
                self.mode = i[1]
            else:
                break

    def get_our_players(self, cycle):
        return self.rcl_l[cycle]

    def get_their_players(self, cycle):
        return self.rcl_r[cycle]

    def get_nearest_players_to_goalie(self, cycle):
        goalie = self.rcl_l[cycle][1]
        our_players = self.rcl_l[cycle][2:]
        their_players = self.rcl_r[cycle][1:]
        our_players.sort(key=lambda z: z.dist(goalie))
        their_players.sort(key=lambda z: z.dist(goalie))
        return our_players, their_players

    def get_nearest_players_to_ball(self, cycle):
        ball = self.ball(cycle)
        our_players = self.rcl_l[cycle][1:]  #hassan :| az bazikon 0 gzshti in hey none type mide 5 saate oskol shdm
        their_players = self.rcl_r[cycle][1:]
        our_players.sort(key=lambda z: z.dist(ball.get_pos()))
        their_players.sort(key=lambda z: z.dist(ball.get_pos()))
        return our_players, their_players

    def get_our_team_name(self):
        return self.left_team_name

    def get_their_team_name(self):
        return self.right_team_name

    def get_our_goalie(self, cycle):
        return self.rcl_l[cycle][1]

    def get_cycle(self):
        return self.game_time.cycle()

    def our_player(self, unum, cycle):
        return self.rcl_l[cycle][unum]

    def their_player(self, unum, cycle):
        return self.rcl_r[cycle][unum]

    def get_ball(self, cycle):
        return self.ball(cycle)


class Vector2D:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def pos(self):
        return self.x, self.y

    def abs(self):
        return abs(self.x), abs(self.y)

    def vel(self):
        return self.vx, self.vy

    def absX(self):
        return abs(self.x)

    def absY(self):
        return abs(self.y)

    def dist(self, other) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Rect2D:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.width = bottom_right.x - top_left.x
        self.height = bottom_right.y - top_left.y

    def top(self):
        return self.top_left.y

    def bottom(self):
        return self.bottom_right.y

    def left(self):
        return self.top_left.x

    def right(self):
        return self.bottom_right.x

    def center(self):
        return Vector2D(self.left() + self.width / 2, self.top() + self.height / 2)

    def is_point_in(self, point):
        return self.left() <= point.get_x() <= self.right() and self.top() <= point.get_y() <= self.bottom()


class Ball:
    def __init__(self, x, y, vx, vy):
        self.pos = Vector2D(x, y, vx, vy)
        self.ball_size = 0.5

    def get_x(self):
        return self.pos.x

    def get_y(self):
        return self.pos.y

    def get_pos(self):
        return self.pos

    def get_ball_size(self):
        return self.ball_size

    def get_vx(self):
        return self.pos.vx

    def get_vy(self):
        return self.pos.vy


class PlayerObject(Vector2D):
    def __init__(self, x=0, y=0, vx=0, vy=0, _unum=-1, action=None, team="unknown", ball_pos=Vector2D(0, 0)):
        super().__init__(x, y, vx, vy)
        self._unum = _unum
        self.action = action
        self.team = team
        self.ball_pos = ball_pos

        if action is not None:
            self._kick = action['kick']
            self._dash = action['dash']
            self._catch = action['catch']
            self._turn_neck = action['turn_neck']
            self._pointto = action['pointto']
            self._say = action['say']
            self._turn = action['turn']
            self._tackle = action['tackle']
            self._change_view = action['change_view']
            self._attentionto = action['attentionto']
        else:
            self._kick = None
            self._dash = None
            self._catch = None
            self._turn_neck = None
            self._pointto = None
            self._say = None
            self._turn = None
            self._tackle = None
            self._change_view = None
            self._attentionto = None

    def is_kickable(self):
        return self.dist(self.ball_pos) <= 1.5

    def is_catchable(self):
        return self.dist(self.ball_pos) <= 2 and self._unum == 1

    def pos(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_vx(self):
        return self.vx

    def get_vy(self):
        return self.vy

    def vel(self):
        return self.vx, self.vy

    def get_kick(self):
        return self._kick

    def get_dash(self):
        return self._dash

    def get_catch(self):
        return self._catch

    def get_turn_neck(self):
        return self._turn_neck

    def get_pointto(self):
        return self._pointto

    def get_say(self):
        return self._say

    def get_turn(self):
        return self._turn

    def get_tackle(self):
        return self._tackle

    def get_change_view(self):
        return self._change_view

    def get_attentionto(self):
        return self._attentionto

    def get_unum(self):
        return self._unum


class GameTime:

    def __init__(self, game_time, t_over):
        self.game_time = game_time
        self.t_over = t_over

    def reset_time(self):
        self.game_time = 1

    def kick_off(self):
        return 1

    def time_over(self):
        return self.t_over

    def add_time(self):
        self.game_time += 1

        if self.game_time == 3000:
            self.game_time = 3001

    def cycle(self):
        return self.game_time

    def set_cycle_to(self, c):
        if 1 <= c <= 6000:
            self.game_time = c
