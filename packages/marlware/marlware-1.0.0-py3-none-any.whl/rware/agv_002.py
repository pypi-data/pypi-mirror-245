import logging

from collections import defaultdict, OrderedDict
import gym
from gym import spaces

from rware.utils import MultiAgentActionSpace, MultiAgentObservationSpace

from enum import Enum
import numpy as np

from typing import List, Tuple, Optional, Dict

import networkx as nx

_AXIS_Z = 0
_AXIS_Y = 1
_AXIS_X = 2

_COLLISION_LAYERS = 2  # 碰撞层=2

_LAYER_AGENTS = 0  # Agent层=0
_LAYER_SHELFS = 1  # 架子层=1
_LAYER_WALLS = 3  # 墙体层=3


# 定义向量类
class _VectorWriter:
    def __init__(self, size: int):
        self.vector = np.zeros(size, dtype=np.float32)
        self.idx = 0

    # 定义写 def xxx(self,xxxx)   python的魔法方法
    def write(self, data):
        data_size = len(data)
        self.vector[self.idx: self.idx + data_size] = data
        self.idx += data_size

    # 定义跳跃
    def skip(self, bits):
        self.idx += bits


# 定义动作
class Action(Enum):
    NOOP = 0  # 无操作
    FORWARD = 1  # 前
    LEFT = 2  # 左
    RIGHT = 3  # 右
    TOGGLE_LOAD = 4  # 切换负载（背负货物？）


# 定义方向类-上下左右
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# 定义奖励类型
class RewardType(Enum):
    GLOBAL = 0  # 全局=0
    INDIVIDUAL = 1  # 个人=1
    TWO_STAGE = 2  # 上述俩个阶段=2


# 定义观察类型（枚举）
class ObserationType(Enum):
    DICT = 0  # 字典=0
    FLATTENED = 1  # 变平=1
    IMAGE = 2  ##图像=2


# 定义图像层（枚举）
class ImageLayer(Enum):
    """
    Input layers of image-style observations #输入图像样式观测的图层
    """
    SHELVES = 0  # binary layer indicating shelves (also indicates carried shelves)    #货架= 0 #二进制层表示货架(也表示携带货架)
    REQUESTS = 1  # binary layer indicating requested shelves  #请求=1  二进制层，表示请求的货架
    AGENTS = 2  # binary layer indicating agents in the environment (no way to distinguish agents)  #Agent = 2 #二进制层表示环境中的agent(无法区分agent)
    AGENT_DIRECTION = 3  # layer indicating agent directions as int (see Direction enum + 1 for values)  #agent 方向 = 3层，指示Agent方向为int(参见Direction enum + 1的值)
    AGENT_LOAD = 4  # binary layer indicating agents with load     agent负载= 4 二进制层表示agent负载
    GOALS = 5  # binary layer indicating goal/ delivery locations  #目标= 5 指示目标/交付位置的二进制层
    ACCESSIBLE = 6  # binary layer indicating accessible cells (all but occupied cells/ out of map)  #无障碍= 6 # 二进制层表示可访问的单元(除了已占用的单元格/不在地图上)


# 定义基类
class Entity:
    def __init__(self, id_: int, x: int, y: int):
        self.id = id_
        self.prev_x = None  # 先前的x=none
        self.prev_y = None
        self.x = x
        self.y = y


# 定义Agent类
class Agent(Entity):
    counter = 0  # 计数器=0

    def __init__(self, x: int, y: int, dir_: Direction, msg_bits: int):
        Agent.counter += 1
        super().__init__(Agent.counter, x, y)
        self.dir = dir_
        self.message = np.zeros(msg_bits)  # 信息清零
        self.req_action: Optional[Action] = None  # 请求的行动：选[动作]=none
        self.carrying_shelf: Optional[Shelf] = None  # 携带架子:可选[shelf] =none
        self.canceled_action = None  # 取消的动作=none
        self.has_delivered = False  # 已交付= False

    @property
    def collision_layers(self):  # 定义碰撞层
        if self.loaded:  # 如果被加载
            return (_LAYER_AGENTS, _LAYER_SHELFS)  # 返回图层agent ,图层货架
        else:
            return (_LAYER_AGENTS,)  #

    # 20230718晚新增
    grid_size = (
        83,
        160,
    )
    highways1 = np.zeros(grid_size, dtype=np.int32)  # 创建一个83×160的空层
    # 定义白色路径函数
    highway_func = lambda x1, y1: (
        (  # 从左到右的一整行格子
            (x1 == 41)
            and ((y1 > 0) or (y1 < 159))
        )
        or (  # 1号到8号分拣仓库的竖线
            (x1 < 42)
            and ((y1 == 1) or (y1 == 17) or (y1 == 33) or (y1 == 49) or (y1 == 116) or (y1 == 128) or (y1 == 140) or (
            y1 == 152))
        )
        or (  # 通往主仓库的竖线1
            (x1 > 41) and (x1 < 51)
            and (y1 == 54)
        )
        or (  # 通往主仓库的横线1
            (x1 == 50)
            and ((y1 > 54) and (y1 < 74))
        )
        or (  # 通往主仓库的竖线2
            (x1 > 41) and (x1 < 51)
            and (y1 == 111)
        )
        or (  # 通往主仓库的横线2
            (x1 == 50)
            and ((y1 > 85) and (y1 < 111))
        )
        or (  # 主仓库停车位左
            (x1 > 45) and (x1 < 55)
            and ((y1 > 73) and (y1 < 77))
        )
        or (  # 主仓库停车位右
            (x1 > 45) and (x1 < 55)
            and ((y1 > 82) and (y1 < 86))
        )
        or (  # 1号到8号分拣仓库旁边的格子，2×8
            (x1 == 1)
            and ((y1 == 0) or (y1 == 2) or (y1 == 16) or (y1 == 18) or (y1 == 32) or (y1 == 34) or (y1 == 48) or (
            y1 == 50) or (
                     y1 == 115) or (y1 == 117) or (y1 == 127) or (y1 == 129) or (y1 == 139) or (y1 == 141) or (
                     y1 == 151) or (y1 == 153))
        )
        or (  # 1号到8号分拣仓库格子，2×8
            (x1 == 0)
            and ((y1 == 0) or (y1 == 2) or (y1 == 16) or (y1 == 18) or (y1 == 32) or (y1 == 34) or (y1 == 48) or (
            y1 == 50) or (
                     y1 == 115) or (y1 == 117) or (y1 == 127) or (y1 == 129) or (y1 == 139) or (y1 == 141) or (
                     y1 == 151) or (y1 == 153))
        )
        or (  # 9号到15号分拣仓库的竖线
            (x1 > 41)
            and ((y1 == 9) or (y1 == 25) or (y1 == 41) or (y1 == 122) or (y1 == 134) or (y1 == 146) or (y1 == 158))
        )
        or (  # 9号到15号分拣仓库旁边的格子，2×7
            (x1 == 81)
            and ((y1 == 8) or (y1 == 10) or (y1 == 24) or (y1 == 26) or (y1 == 40) or (y1 == 42) or (y1 == 121) or (
            y1 == 123) or (y1 == 133) or (y1 == 135) or (y1 == 145) or (y1 == 147) or (y1 == 157) or (y1 == 159))
        )
        or (  # 9号到15号分拣仓库格子，2×7
            (x1 == 82)
            and ((y1 == 8) or (y1 == 10) or (y1 == 24) or (y1 == 26) or (y1 == 40) or (y1 == 42) or (y1 == 121) or (
            y1 == 123) or (y1 == 133) or (y1 == 135) or (y1 == 145) or (y1 == 147) or (y1 == 157) or (y1 == 159))
        )
        or(
            ((x1 > 45) and (x1 < 55))
            and ((y1 > 76) and (y1 < 83))
        )


    )
    # 在空白层填充白色格子
    for x1 in range(grid_size[1]):
        for y1 in range(grid_size[0]):
            highways1[y1, x1] = highway_func(y1, x1)
    def _is_highway1(self, x1: int, y1: int) -> bool:
        return self.highways1[y1, x1]

    # 定义请求的位置 todo:判断是否在高速公路上，然后选择动作
    def req_location(self, grid_size) -> Tuple[int, int]:  # ->这是一个叫做返回值注解的符号
        # if self.req_action != Action.FORWARD:
        #     return self.x, self.y
        # elif self.dir == Direction.UP:
        #     return self.x, max(0, self.y - 1)
        # elif self.dir == Direction.DOWN:
        #     return self.x, min(grid_size[0] - 1, self.y + 1)
        # elif self.dir == Direction.LEFT:
        #     return max(0, self.x - 1), self.y
        # elif self.dir == Direction.RIGHT:
        #     return min(grid_size[1] - 1, self.x + 1), self.y
        #  todo:20230718晚更改(上10行)
        if self.req_action != Action.FORWARD:  # 如果请求的行动不等于下向前行动(这里相当于noop无运动)
            return self.x, self.y
        elif self.dir == Direction.UP:
            if self._is_highway1(self.x, max(0, self.y - 1)):
                return self.x, max(0, self.y - 1)  # 上，因为害怕负值，所以和0作比较
            else:
                return self.x, self.y  # 如果越界，返回原值
        elif self.dir == Direction.DOWN:
            if self._is_highway1(self.x, min(grid_size[0] - 1, self.y + 1)):
                return self.x, min(grid_size[0] - 1, self.y + 1)   # 下，怕超越下界，因此取最小
            else:
                return self.x, self.y  # 如果越界，返回原值
        elif self.dir == Direction.LEFT:
            if self._is_highway1(max(0, self.x - 1), self.y):
                return max(0, self.x - 1), self.y
            else:
                return self.x, self.y  # 如果越界，返回原值
        elif self.dir == Direction.RIGHT:
            if self._is_highway1(min(grid_size[1] - 1, self.x + 1), self.y):
                return min(grid_size[1] - 1, self.x + 1), self.y
            else:
                return self.x, self.y  # 如果越界，返回原值


        raise ValueError(
            f"Direction is {self.dir}. Should be one of {[v for v in Direction]}"
        )
    #定义的方向
    def req_direction(self) -> Direction:
        wraplist = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        if self.req_action == Action.RIGHT:
            return wraplist[(wraplist.index(self.dir) + 1) % len(wraplist)]
        elif self.req_action == Action.LEFT:
            return wraplist[(wraplist.index(self.dir) - 1) % len(wraplist)]
        else:
            return self.dir


class Shelf(Entity):
    counter = 0

    def __init__(self, x, y):
        Shelf.counter += 1
        super().__init__(Shelf.counter, x, y)

    @property
    def collision_layers(self):
        return (_LAYER_SHELFS,)


class Wall(Entity):
    counter = 0

    def __init__(self, x, y):
        Wall.counter += 1
        super().__init__(Wall.counter, x, y)

    @property
    def collision_layers(self):  # Todo：是否正确？墙体应该限制agv行走
        return (_LAYER_WALLS,)


# 定义仓库类
class Warehouse(gym.Env):  # 9, 8, 3, 10, 3, 1, 5, None, None, RewardType.GLOBAL

    metadata = {"render.modes": ["human", "rgb_array"]}  # 元数据=渲染模式：【人、rgb数组】

    def __init__(
        self,
        shelf_columns: int,  # 架子的列 =9
        column_height: int,  # 列的高度=8
        shelf_rows: int,  # 架子的行=3
        n_agents: int,  # agent数量=10
        msg_bits: int,  # =3
        sensor_range: int,  # 传感器观测范围=1
        request_queue_size: int,  # 请求队列的大小=5 (同时需要多少个货架)
        max_inactivity_steps: Optional[int],  # 最大不活动步数:可选[int]=none
        max_steps: Optional[int],  # 最大步数:可选[int]=none
        reward_type: RewardType,  # 奖励类型:全局
        layout: str = None,  # 布局
        observation_type: ObserationType = ObserationType.FLATTENED,  # 观察类型：观察类型=观察类型.flatened方法
        image_observation_layers: List[ImageLayer] = [  # 图像观察层：listp[图像层]
            ImageLayer.SHELVES,  # 图像层.架子
            ImageLayer.REQUESTS,  # 图像层.请求
            ImageLayer.AGENTS,  ##图像层.agent
            ImageLayer.GOALS,  # 图像层.目标
            ImageLayer.ACCESSIBLE  # 图像层.可访问单元
        ],
        image_observation_directional: bool = True,  # 图像观察方向
        normalised_coordinates: bool = False,  # 指定绝对坐标是否应该相对于总仓库大小进行标准化
    ):
        """The robotic warehouse environment

        Creates a grid world where multiple agents (robots)
        are supposed to collect shelfs, bring them to a goal
        and then return them.
        .. note:
            The grid looks like this:

            shelf
            columns
                vv
            ----------
            -XX-XX-XX-        ^
            -XX-XX-XX-  Column Height
            -XX-XX-XX-        v
            ----------
            -XX----XX-   <\
            -XX----XX-   <- Shelf Rows
            -XX----XX-   </
            ----------
            ----GG----

            G: is the goal positions where agents are rewarded if
            they bring the correct shelfs.

            The final grid size will be
            height: (column_height + 1) * shelf_rows + 2
            width: (2 + 1) * shelf_columns + 1

            The bottom-middle column will be removed to allow for
            robot queuing next to the goal locations

        :param shelf_columns: Number of columns in the warehouse
        :type shelf_columns: int
        :param column_height: Column height in the warehouse
        :type column_height: int
        :param shelf_rows: Number of columns in the warehouse
        :type shelf_rows: int
        :param n_agents: Number of spawned and controlled agents
        :type n_agents: int
        :param msg_bits: Number of communication bits for each agent
        :type msg_bits: int
        :param sensor_range: Range of each agents observation
        :type sensor_range: int
        :param request_queue_size: How many shelfs are simultaneously requested
        :type request_queue_size: int
        :param max_inactivity: Number of steps without a delivered shelf until environment finishes
        :type max_inactivity: Optional[int]
        :param reward_type: Specifies if agents are rewarded individually or globally
        :type reward_type: RewardType
        :param layout: A string for a custom warehouse layout. X are shelve locations, dots are corridors, and g are the goal locations. Ignores shelf_columns, shelf_height and shelf_rows when used.
        :type layout: str
        :param observation_type: Specifies type of observations
        :param image_observation_layers: Specifies types of layers observed if image-observations
            are used
        :type image_observation_layers: List[ImageLayer]
        :param image_observation_directional: Specifies whether image observations should be
            rotated to be directional (agent perspective) if image-observations are used
        :type image_observation_directional: bool
        :param normalised_coordinates: Specifies whether absolute coordinates should be normalised
            with respect to total warehouse size
        :type normalised_coordinates: bool
        """

        self.goals: List[Tuple[int, int]] = []  # 创建目标地点：二维数组的一个list
        self.reception_bays: List[Tuple[int, int]] = []  # 创建目标地点：二维数组的一个list#todo:20230815新增接货位
        self.shelfs_fix: List[Tuple[int, int]] = []  # 创建目标地点：二维数组的一个list #todo:20230812新增固定架子层
        self.main_warehouse: List[Tuple[int, int]] = []  # 创建目标地点：二维数组的一个list #todo:20230812新增主仓库层
        self.main_warehouse_left_transverse: List[Tuple[int, int]] = []  # 创建目标地点：二维数组的一个list #todo:20230812新增主仓库左横

        if not layout:  # 如果没布局
            self._make_layout_from_params(shelf_columns, shelf_rows, column_height)  # 根据参数(货架列、货架行、列高)进行布局
        # else:
        #     self._make_layout_from_str(layout)  # 从str创建布局 20230711屏蔽***************************************************************************

        self.n_agents = n_agents  # =10
        self.msg_bits = msg_bits  # 每个Agent的交流位数=3
        self.sensor_range = sensor_range  # =1
        self.max_inactivity_steps: Optional[int] = max_inactivity_steps  # 在环境结束之前没有交付货架的步骤数
        self.reward_type = reward_type  # 全局
        self.reward_range = (0, 1)  # 奖励范围

        self._cur_inactive_steps = None  # 当前不活跃的步骤
        self._cur_steps = 0  # 当前步骤
        self.max_steps = max_steps  # 最大步数=none

        self.normalised_coordinates = normalised_coordinates  # 指定绝对坐标是否应该相对于总仓库大小进行标准化


        sa_action_space = [len(Action), *msg_bits * (2,)]  # 采样动作空间

        if len(sa_action_space) == 1:
            sa_action_space = spaces.Discrete(sa_action_space[0])  # gym一维空间离散化
        else:
            sa_action_space = spaces.MultiDiscrete(sa_action_space)  # gym多维空间离散化
        self.action_space = spaces.Tuple(tuple(n_agents * [sa_action_space]))  # Tuple类，它允许我们将几个Space类实例组合在一起

        self.request_queue_size = request_queue_size  # 同时需要货架的数量
        self.request_queue = []

        self.agents: List[Agent] = []  # 定义一个Agents空列表

        # default values:#默认的值
        self.fast_obs = None  #
        self.image_obs = None  # 图片观察
        self.observation_space = None  # 观察空间
        if observation_type == ObserationType.IMAGE:  # 如果观察类型为IMAGE
            self._use_image_obs(image_observation_layers, image_observation_directional)
        else:
            # used for DICT observation type and needed as preceeding stype to generate
            # FLATTENED observations as well    #<<<<<<<<<<<<<用于DICT观测类型，也需要作为前面的类型来生成flat观测
            self._use_slow_obs()

        # for performance reasons we
        # can flatten the obs vector   #<<<<<<<<<<<<<出于性能考虑，我们可以将obs向量扁平化
        if observation_type == ObserationType.FLATTENED:
            self._use_fast_obs()

        self.renderer = None  # 渲染为none

    # 创建参数布局
    def _make_layout_from_params(self, shelf_columns, shelf_rows, column_height):  # 9、3、8
        # assert shelf_columns % 2 == 1, "Only odd number of shelf columns is supported"  # 架子列个数仅支持奇数  20230711屏蔽***************************************************************************
        # 网格尺寸 29×28
        # self.grid_size = (
        #     (column_height + 1) * shelf_rows + 2,
        #     (2 + 1) * shelf_columns + 1,
        # )
        # 158×83

        #整体网格尺寸=83*160
        self.grid_size = (
            83,
            160,
        )

        # self.column_height = column_height  # 8
        self.grid = np.zeros((_COLLISION_LAYERS, *self.grid_size), dtype=np.int32)  # 创建一个83×160的空层   #todo:此处改为highways

        self.goals = [    ##目标为俩个黑色的箱子
            (0, 0),  # ＃1-1
            (2, 0),  # ＃1-2
            (16, 0),  # ＃2-1
            (18, 0),  # ＃2-2
            (32, 0),  # ＃3-1
            (34, 0), # ＃3-2
            (48, 0), # ＃4-1
            (50, 0), # ＃4-2
            (115, 0), # ＃5-1
            (117, 0), # ＃5-1
            (127, 0), # ＃6-1
            (129, 0), # ＃6-1
            (139, 0), # ＃7-1
            (141, 0),  # ＃7-2
            (151, 0),  # ＃8-1
            (153, 0),  # ＃8-2
            (8, 82),  # ＃9-1
            (10, 82),  # ＃9-2
            (24,82),  # ＃10-1
            (26, 82),  # ＃10-2
            (40, 82),  # ＃11-1
            (42, 82),  # ＃11-2
            (121, 82),  # ＃12-1
            (123, 82),  # ＃12-1
            (133, 82),  # ＃13-1
            (135, 82),  # ＃13-1
            (145, 82),  # ＃14-1
            (147, 82),  # ＃14-2
            (157, 82),  # ＃15-1
            (159, 82),  # ＃15-2
        ]

        # todo:20230815新增(下6行)
        for i in range(76, 77):
            for j in range(48, 52):
                self.reception_bays.append((i, j))
        for i in range(83, 84):
            for j in range(48, 52):
                self.reception_bays.append((i, j))
        # todo:20230812新增
        for i in range(77, 83):
            for j in range(46, 55):
                self.shelfs_fix.append((i, j))
        # todo:20230815新增,主仓库坐标
        for i in range(74, 86):
            for j in range(46, 55):
                self.main_warehouse.append((i, j))
        # todo:20230816新增,主仓库左横
        for i in range(55, 74):
            for j in range(50, 51):
                self.main_warehouse_left_transverse.append((i, j))

        # self.goals = [  ##目标为俩个黑色的箱子
        #     (self.grid_size[1] // 2 - 1, self.grid_size[0] - 1),  # （13，28）
        #     (self.grid_size[1] // 2, self.grid_size[0] - 1),  # （14，28）
        # ]

        self.highways = np.zeros(self.grid_size, dtype=np.int32)  # 创建一个83×160的空层
        # 定义白色路径函数
        highway_func = lambda x, y: (
            (  # 从左到右的一整行格子
                (x == 41)
                and ((y > 0) or (y < 159))
            )
            or (  # 1号到8号分拣仓库的竖线
                (x < 42)
                and ((y == 1) or (y == 17) or (y == 33) or (y == 49) or (y == 116) or (y == 128) or (y == 140) or (
                    y == 152))
            )
            or (  # 通往主仓库的竖线1
                (x > 41) and (x < 51)
                and (y == 54)
            )
            or (  # 通往主仓库的横线1
                (x == 50)
                and ((y > 54) and (y < 74))
            )
            or (  # 通往主仓库的竖线2
                (x > 41) and (x < 51)
                and (y == 111)
            )
            or (  # 通往主仓库的横线2
                (x == 50)
                and ((y > 85) and (y < 111))
            )
            or (  # 主仓库停车位左
                (x > 45) and (x < 55)
                and ((y > 73) and (y < 77))
            )
            or (  # 主仓库停车位右
                (x > 45) and (x < 55)
                and ((y > 82) and (y < 86))
            )
            or (  # 1号到8号分拣仓库旁边的格子，2×8
                (x == 1)
                and ((y == 0) or (y == 2) or (y == 16) or (y == 18) or (y == 32) or (y == 34) or (y == 48) or (
                    y == 50) or (
                         y == 115) or (y == 117) or (y == 127) or (y == 129) or (y == 139) or (y == 141) or (
                             y == 151) or (y == 153))
            )
            or (  # 1号到8号分拣仓库格子，2×8
                (x == 0)
                and ((y == 0) or (y == 2) or (y == 16) or (y == 18) or (y == 32) or (y == 34) or (y == 48) or (
                y == 50) or (
                         y == 115) or (y == 117) or (y == 127) or (y == 129) or (y == 139) or (y == 141) or (
                         y == 151) or (y == 153))
            )
            or (  # 9号到15号分拣仓库的竖线
                (x > 41)
                and ((y == 9) or (y == 25) or (y == 41) or (y == 122) or (y == 134) or (y == 146) or (y == 158))
            )
            or (  # 9号到15号分拣仓库旁边的格子，2×7
                (x == 81)
                and ((y == 8) or (y == 10) or (y == 24) or (y == 26) or (y == 40) or (y == 42) or (y == 121) or (
                y == 123) or (y == 133) or (y == 135) or (y == 145) or (y == 147) or (y == 157) or (y == 159))
            )
            or (  # 9号到15号分拣仓库格子，2×7
                (x == 82)
                and ((y == 8) or (y == 10) or (y == 24) or (y == 26) or (y == 40) or (y == 42) or (y == 121) or (
                y == 123) or (y == 133) or (y == 135) or (y == 145) or (y == 147) or (y == 157) or (y == 159))
            )

        )
        # 在空白层填充白色格子
        for x in range(self.grid_size[1]):
            for y in range(self.grid_size[0]):
                self.highways[y, x] = highway_func(y, x)

        # self.grid2 = np.zeros((_COLLISION_LAYERS, *self.highways), dtype=np.int32)


        self.highways3 = np.zeros(self.grid_size, dtype=np.int32)  # 创建一个83×160的空层
        # 定义货架函数
        highway_func3 = lambda x, y: (

            (  #
                (x < 46)
                and ((y > 0) or (y < 159))
            )
            or (
                (x > 45) and (x < 55)
                and ((y < 77) or (y > 82))
            )
            or (
                (x > 54)
                and ((y > 0) or (y < 159))
            )
        )
        # 在空白层填充白色格子
        for x in range(self.grid_size[1]):
            for y in range(self.grid_size[0]):
                self.highways3[y, x] = highway_func3(y, x)

        self.wall = np.zeros(self.grid_size, dtype=np.int32)  # 创建一个83×160的空层
        # 定义白色路径函数
        wall_func = lambda x, y: (
            (
                (x > 45) and (x < 55)
                and ((y > 76) and (y < 83))
            )
        )
        # 在空白层填充白色格子
        for x in range(self.grid_size[1]):
            for y in range(self.grid_size[0]):
                self.wall[y, x] = wall_func(y, x)



    # 创建布局（暂时没用到）20230711屏蔽***************************************************************************
    # def _make_layout_from_str(self, layout):
    #     layout = layout.strip()  # strip() 方法用于移除字符串头尾指定的字符(默认为空格或换行符)或字符序列
    #     layout = layout.replace(" ", "")  #
    #     grid_height = layout.count("\n") + 1
    #     lines = layout.split("\n")
    #     grid_width = len(lines[0])
    #     for line in lines:
    #         assert len(line) == grid_width, "Layout must be rectangular"  # 布局必须为矩形
    #
    #     self.grid_size = (grid_height, grid_width)
    #     self.grid = np.zeros((_COLLISION_LAYERS, *self.grid_size), dtype=np.int32)
    #     self.highways = np.zeros(self.grid_size, dtype=np.int32)
    #
    #     for y, line in enumerate(lines):
    #         for x, char in enumerate(line):
    #             assert char.lower() in "gx."
    #             if char.lower() == "g":
    #                 self.goals.append((x, y))
    #                 self.highways[y, x] = 1
    #             elif char.lower() == ".":
    #                 self.highways[y, x] = 1
    #
    #     assert len(self.goals) >= 1, "At least one goal is required"  # 至少要有一个目标

    # 使用图像观察
    def _use_image_obs(self, image_observation_layers, directional=True):
        """
        Set image observation space   #设置图像观测空间
        :param image_observation_layers (List[ImageLayer]): list of layers to use as image channels #用作图像通道的图层列表
        :param directional (bool): flag whether observations should be directional (pointing in
            direction of agent or north-wise)  #标记观察是否应该是定向的(指向代理的方向或向北)
        """
        self.image_obs = True  # 设置图片观察为true
        self.fast_obs = False  ##设置fast观察为false
        self.image_observation_directional = directional  # 图片观察方方向化为True
        self.image_observation_layers = image_observation_layers

        observation_shape = (1 + 2 * self.sensor_range, 1 + 2 * self.sensor_range)

        layers_min = []
        layers_max = []
        for layer in image_observation_layers:
            if layer == ImageLayer.AGENT_DIRECTION:
                # directions as int  #方向如下:
                layer_min = np.zeros(observation_shape, dtype=np.float32)
                layer_max = np.ones(observation_shape, dtype=np.float32) * max([d.value + 1 for d in Direction])
            else:
                # binary layer #二进制层
                layer_min = np.zeros(observation_shape, dtype=np.float32)
                layer_max = np.ones(observation_shape, dtype=np.float32)
            layers_min.append(layer_min)
            layers_max.append(layer_max)

        # total observation  #总观察
        min_obs = np.stack(layers_min)
        max_obs = np.stack(layers_max)
        self.observation_space = spaces.Tuple(
            tuple([spaces.Box(min_obs, max_obs, dtype=np.float32)] * self.n_agents)
        )

    # 使用缓慢观察
    def _use_slow_obs(self):
        self.fast_obs = False

        self._obs_bits_for_self = 4 + len(Direction)
        self._obs_bits_per_agent = 1 + len(Direction) + self.msg_bits
        self._obs_bits_per_shelf = 2
        self._obs_bits_for_requests = 2

        self._obs_sensor_locations = (1 + 2 * self.sensor_range) ** 2

        self._obs_length = (
            self._obs_bits_for_self
            + self._obs_sensor_locations * self._obs_bits_per_agent
            + self._obs_sensor_locations * self._obs_bits_per_shelf
        )

        if self.normalised_coordinates:
            location_space = spaces.Box(
                low=0.0,
                high=1.0,
                shape=(2,),
                dtype=np.float32,
            )
        else:
            location_space = spaces.MultiDiscrete(
                [self.grid_size[1], self.grid_size[0]]
            )

        self.observation_space = spaces.Tuple(
            tuple(
                [
                    spaces.Dict(
                        OrderedDict(
                            {
                                "self": spaces.Dict(
                                    OrderedDict(
                                        {
                                            "location": location_space,
                                            "carrying_shelf": spaces.MultiDiscrete([2]),
                                            "direction": spaces.Discrete(4),
                                            "on_highway": spaces.MultiBinary(1),
                                        }
                                    )
                                ),
                                "sensors": spaces.Tuple(
                                    self._obs_sensor_locations
                                    * (
                                        spaces.Dict(
                                            OrderedDict(
                                                {
                                                    "has_agent": spaces.MultiBinary(1),
                                                    "direction": spaces.Discrete(4),
                                                    "local_message": spaces.MultiBinary(
                                                        self.msg_bits
                                                    ),
                                                    "has_shelf": spaces.MultiBinary(1),
                                                    "shelf_requested": spaces.MultiBinary(
                                                        1
                                                    ),
                                                }
                                            )
                                        ),
                                    )
                                ),
                            }
                        )
                    )
                    for _ in range(self.n_agents)
                ]
            )
        )

    # 使用快观察
    def _use_fast_obs(self):
        if self.fast_obs:
            return

        self.fast_obs = True
        ma_spaces = []
        for sa_obs in self.observation_space:
            flatdim = spaces.flatdim(sa_obs)
            ma_spaces += [
                spaces.Box(
                    low=-float("inf"),
                    high=float("inf"),
                    shape=(flatdim,),
                    dtype=np.float32,
                )
            ]

        self.observation_space = spaces.Tuple(tuple(ma_spaces))

    # 是高速公路
    def _is_highway(self, x: int, y: int) -> bool:
        return self.highways[y, x]
    # 是“货架位置取反”
    def _is_highway3(self, x: int, y: int) -> bool:
        return self.highways3[y, x]

    def _is_wall(self, x: int, y: int) -> bool:
        return self.wall[y, x]



    # 进行观察
    def _make_obs(self, agent):
        if self.image_obs:
            # write image observations #写图像观察
            if agent.id == 1:
                layers = []
                # first agent's observation --> update global observation layers    #第一个agent的观测->更新全局观测层
                for layer_type in self.image_observation_layers:
                    if layer_type == ImageLayer.SHELVES:
                        layer = self.grid[_LAYER_SHELFS].copy().astype(np.float32) #
                        # set all occupied shelf cells to 1.0 (instead of shelf ID)  #设置所有已占用的货架单元格为1.0(而不是货架ID)
                        layer[layer > 0.0] = 1.0
                        # print("SHELVES LAYER") #打印货架层
                    elif layer_type == ImageLayer.REQUESTS:
                        layer = np.zeros(self.grid_size, dtype=np.float32)
                        for requested_shelf in self.request_queue:
                            layer[requested_shelf.y, requested_shelf.x] = 1.0
                        # print("REQUESTS LAYER") #打印请求层
                    elif layer_type == ImageLayer.AGENTS:
                        layer = self.grid[_LAYER_AGENTS].copy().astype(np.float32)    #
                        # set all occupied agent cells to 1.0 (instead of agent ID)  ##将所有已占用的代理单元设置为1.0(而不是Agent ID)
                        layer[layer > 0.0] = 1.0
                        # print("AGENTS LAYER") #打印Agent层
                    elif layer_type == ImageLayer.AGENT_DIRECTION:
                        layer = np.zeros(self.grid_size, dtype=np.float32)
                        for ag in self.agents:
                            agent_direction = ag.dir.value + 1
                            layer[ag.x, ag.y] = float(agent_direction)
                        # print("AGENT DIRECTIONS LAYER") #打印Agent方向层
                    elif layer_type == ImageLayer.AGENT_LOAD:
                        layer = np.zeros(self.grid_size, dtype=np.float32)
                        for ag in self.agents:
                            if ag.carrying_shelf is not None:
                                layer[ag.x, ag.y] = 1.0
                        # print("AGENT LOAD LAYER") #打印负载层
                    elif layer_type == ImageLayer.GOALS:
                        layer = np.zeros(self.grid_size, dtype=np.float32)
                        for goal_y, goal_x in self.goals:
                            layer[goal_x, goal_y] = 1.0
                        # print("GOALS LAYER") #打印目标层
                    elif layer_type == ImageLayer.ACCESSIBLE:
                        layer = np.ones(self.grid_size, dtype=np.float32)
                        for ag in self.agents:
                            layer[ag.y, ag.x] = 0.0
                        # print("ACCESSIBLE LAYER") #打印访问层
                    # print(layer)
                    # print()
                    # pad with 0s for out-of-map cells  #对于地图外的单元格，垫上0
                    layer = np.pad(layer, self.sensor_range, mode="constant")
                    layers.append(layer)
                self.global_layers = np.stack(layers)

            # global information was generated --> get information for agent  #生成全局信息-->获取Agent信息
            start_x = agent.y
            end_x = agent.y + 2 * self.sensor_range + 1
            start_y = agent.x
            end_y = agent.x + 2 * self.sensor_range + 1
            obs = self.global_layers[:, start_x:end_x, start_y:end_y]

            if self.image_observation_directional:
                # rotate image to be in direction of agent  #旋转图像到Agent的方向
                if agent.dir == Direction.DOWN:
                    # rotate by 180 degrees (clockwise)  #旋转180度(顺时针)
                    obs = np.rot90(obs, k=2, axes=(1, 2))
                elif agent.dir == Direction.LEFT:
                    # rotate by 90 degrees (clockwise)  #旋转90度(顺时针)
                    obs = np.rot90(obs, k=3, axes=(1, 2))
                elif agent.dir == Direction.RIGHT:
                    # rotate by 270 degrees (clockwise) #旋转270度(顺时针)
                    obs = np.rot90(obs, k=1, axes=(1, 2))
                # no rotation needed for UP direction #向上方向不需要旋转
            return obs

        min_x = agent.x - self.sensor_range
        max_x = agent.x + self.sensor_range + 1

        min_y = agent.y - self.sensor_range
        max_y = agent.y + self.sensor_range + 1
        # 传感器
        # sensors
        if (
            (min_x < 0)
            or (min_y < 0)
            or (max_x > self.grid_size[1])
            or (max_y > self.grid_size[0])
        ):
            padded_agents = np.pad(
                self.grid[_LAYER_AGENTS], self.sensor_range, mode="constant"  #
            )
            padded_shelfs = np.pad(
                self.grid[_LAYER_SHELFS], self.sensor_range, mode="constant" #
            )
            # + self.sensor_range due to padding #传感器范围
            min_x += self.sensor_range
            max_x += self.sensor_range
            min_y += self.sensor_range
            max_y += self.sensor_range

        else:
            padded_agents = self.grid[_LAYER_AGENTS]   # todo:此处改为highways     #在83*160的网格上填充agent
            padded_shelfs = self.grid[_LAYER_SHELFS]   # todo:此处改为highways     #在83*160的网格上填充货架

        agents = padded_agents[min_y:max_y, min_x:max_x].reshape(-1)
        shelfs = padded_shelfs[min_y:max_y, min_x:max_x].reshape(-1)

        if self.fast_obs:  # 快速观察
            # write flattened observations   #写一个平面观察
            obs = _VectorWriter(self.observation_space[agent.id - 1].shape[0])
            # 正常化 坐标 （暂时没用到）
            if self.normalised_coordinates:
                agent_x = agent.x / (self.grid_size[1] - 1)
                agent_y = agent.y / (self.grid_size[0] - 1)
            else:
                agent_x = agent.x
                agent_y = agent.y

            obs.write([agent_x, agent_y, int(agent.carrying_shelf is not None)])
            direction = np.zeros(4)
            direction[agent.dir.value] = 1.0
            obs.write(direction)
            obs.write([int(self._is_highway(agent.x, agent.y))])

            for i, (id_agent, id_shelf) in enumerate(zip(agents, shelfs)):
                if id_agent == 0:
                    obs.skip(1)
                    obs.write([1.0])
                    obs.skip(3 + self.msg_bits)
                else:
                    obs.write([1.0])
                    direction = np.zeros(4)
                    direction[self.agents[id_agent - 1].dir.value] = 1.0
                    obs.write(direction)
                    if self.msg_bits > 0:
                        obs.write(self.agents[id_agent - 1].message)
                if id_shelf == 0:
                    obs.skip(2)
                else:
                    obs.write(
                        [1.0, int(self.shelfs[id_shelf - 1] in self.request_queue)]   # 判断 架子是否在要求队列中，是的话返回True.int(True)=1
                    )

            return obs.vector

        # write dictionary observations #写观察字典
        obs = {}
        # 正常化 坐标 （暂时没用到）
        if self.normalised_coordinates:
            agent_x = agent.x / (self.grid_size[1] - 1)
            agent_y = agent.y / (self.grid_size[0] - 1)
        else:
            agent_x = agent.x
            agent_y = agent.y
        # --- self data #自己的数据
        obs["self"] = {
            "location": np.array([agent_x, agent_y]),
            "carrying_shelf": [int(agent.carrying_shelf is not None)],
            "direction": agent.dir.value,
            "on_highway": [int(self._is_highway(agent.x, agent.y))],
        }
        # --- sensor data #传感器数据
        obs["sensors"] = tuple({} for _ in range(self._obs_sensor_locations))

        # find neighboring agents #查找相邻Agent
        for i, id_ in enumerate(agents):
            if id_ == 0:
                obs["sensors"][i]["has_agent"] = [0]
                obs["sensors"][i]["direction"] = 0
                obs["sensors"][i]["local_message"] = self.msg_bits * [0]
            else:
                obs["sensors"][i]["has_agent"] = [1]
                obs["sensors"][i]["direction"] = self.agents[id_ - 1].dir.value
                obs["sensors"][i]["local_message"] = self.agents[id_ - 1].message

        # find neighboring shelfs:  #找到邻近的架子
        for i, id_ in enumerate(shelfs):
            if id_ == 0:
                obs["sensors"][i]["has_shelf"] = [0]
                obs["sensors"][i]["shelf_requested"] = [0]
            else:
                obs["sensors"][i]["has_shelf"] = [1]
                obs["sensors"][i]["shelf_requested"] = [
                    int(self.shelfs[id_ - 1] in self.request_queue)
                ]

        return obs
    # 重新计算网格？
    def _recalc_grid(self):
        self.grid[:] = 0    # todo:此处grid改为highways
        for s in self.shelfs:
            self.grid[_LAYER_SHELFS, s.y, s.x] = s.id   # 获取货架初始54个位置坐标

        for a in self.agents:
            self.grid[_LAYER_AGENTS, a.y, a.x] = a.id   # 获取agent初始8个坐标
    # 重置环境状态，回到初始环境，方便下一次训练
    def reset(self):
        Shelf.counter = 0
        Agent.counter = 0
        self._cur_inactive_steps = 0  # 最近的活动步骤
        self._cur_steps = 0  # 最近的步骤

        # n_xshelf = (self.grid_size[1] - 1) // 3
        # n_yshelf = (self.grid_size[0] - 2) // 9

        # make the shelfs  #制作架子
        self.shelfs = [
            Shelf(x, y)
            for y, x in zip(
                np.indices(self.grid_size)[0].reshape(-1),
                np.indices(self.grid_size)[1].reshape(-1),
            )
            if not self._is_highway3(x, y)
        ]

        # make the walls  #制作墙体
        self.walls = [
            Wall(x, y)
            for y, x in zip(
                np.indices(self.grid_size)[0].reshape(-1),
                np.indices(self.grid_size)[1].reshape(-1),
            )
            if not self._is_highway(x, y)
            if not self._is_wall(x, y)  # todo:是否正确，不正确需要枚举除墙体以外的路线
        ]

        # spawn agents at random locations  # todo:在随机地点生成Agent，这个地方可以修改为指定坐标
        # agent_locs = np.random.choice(
        #     np.arange(self.grid_size[0] * self.grid_size[1]),
        #     size=self.n_agents,
        #     replace=False,
        # )
        # agent_locs = np.unravel_index(agent_locs, self.grid_size)
        # todo:在指定地点生成agent
        agent_locs = ((48, 49, 50, 51, 48, 49, 50, 51), (76,  76,  76, 76,  83,  83,  83,  83))
        # and direction #和方向
        agent_dirs = np.random.choice([d for d in Direction], size=self.n_agents)
        # 定义agent，并获取初始坐标
        self.agents = [
            Agent(x, y, dir_, self.msg_bits)
            for y, x, dir_ in zip(*agent_locs, agent_dirs)
        ]

        self._recalc_grid()  # 重新计算网络？

        self.request_queue = list(   #todo:随机获取需求货架列表，可以改成指定
            np.random.choice(self.shelfs, size=self.request_queue_size, replace=False)
        )

        return tuple([self._make_obs(agent) for agent in self.agents])  # 遍历8个agent观测
        # for s in self.shelfs:
        #     self.grid[0, s.y, s.x] = 1
        # print(self.grid[0])

    # 完成一个时间步，返回4个值（observation：object, 对环境的观测、reward：float，即时的奖励、done：bool 是否需要重置环境（如游戏这个时间步后游戏结束）、info ：dict 用于调试诊断信息）
    def step(
        self, actions: List[Action]
    ) -> Tuple[List[np.ndarray], List[float], List[bool], Dict]:
        assert len(actions) == len(self.agents)
        # 分别给8个agent 赋予行动
        for agent, action in zip(self.agents, actions):
            if self.msg_bits > 0:
                agent.req_action = Action(action[0])
                agent.message[:] = action[1:]
            else:
                agent.req_action = Action(action) #

        # # stationary agents will certainly stay where they are  #固定的智能体肯定会待在原地
        # stationary_agents = [agent for agent in self.agents if agent.action != Action.FORWARD]

        # # forward agents will move only if they avoid collisions  #前进agent只有在避免碰撞的情况下才会移动
        # forward_agents = [agent for agent in self.agents if agent.action == Action.FORWARD]
        commited_agents = set()

        G = nx.DiGraph()

        for agent in self.agents:
            start = agent.x, agent.y  # agent起始位置
            target = agent.req_location(self.grid_size)  # agent要求指定的位置

            if (                       # 如果
                agent.carrying_shelf   # agent携带货架
                and start != target    # 并且起始位置不等于指定位置
                and self.grid[_LAYER_SHELFS, target[1], target[0]]  # 判断该位置是否在架子层==1
                and not (
                self.grid[_LAYER_AGENTS, target[1], target[0]] #
                and self.agents[
                    self.grid[_LAYER_AGENTS, target[1], target[0]] - 1 #
                ].carrying_shelf
            )
            ):
                # there's a standing shelf at the target location #在目标位置有一个站立的架子
                # our agent is carrying a shelf so there's no way #我们的代理商带着一个架子，所以没有办法
                # this movement can succeed. Cancel it.  #这场运动可以成功。取消它
                agent.req_action = Action.NOOP   # 因此要求的行动=无动作
                G.add_edge(start, start)   # 回到初始位置

            # todo:20230815增加, 如果不携带架子则不会出主仓库（下6行）
            elif (agent.carrying_shelf == None
                  and start != target  # 并且起始位置不等于指定位置
                  and start in self.main_warehouse
                  and target not in self.main_warehouse):
                agent.req_action = Action.NOOP  # 因此要求的行动=无动作
                G.add_edge(start, start)  # 回到初始位置
            # todo:20230811增加, 如果不携带架子则不会到达goals（下5行）
            elif (agent.carrying_shelf==None
                  and start != target  # 并且起始位置不等于指定位置
                  and (target in self.goals)):
                agent.req_action = Action.NOOP  # 因此要求的行动=无动作
                G.add_edge(start, start)  # 回到初始位置
            else:
                G.add_edge(start, target)  # 否则，到指定位置

        wcomps = [G.subgraph(c).copy() for c in nx.weakly_connected_components(G)]

        for comp in wcomps:
            try:
                # if we find a cycle in this component we have to
                # commit all nodes in that cycle, and nothing else  #如果我们在这个组件中找到一个循环，我们必须提交该循环中的所有节点，而不是其他节点
                cycle = nx.algorithms.find_cycle(comp)
                if len(cycle) == 2:
                    # we have a situation like this: [A] <-> [B]  #我们有一个这样的情况:[a] <-> [B]
                    # which is physically impossible. so skip    #这在物理上是不可能的。所以跳过
                    continue
                for edge in cycle:
                    start_node = edge[0]
                    agent_id = self.grid[_LAYER_AGENTS, start_node[1], start_node[0]] #
                    if agent_id > 0:
                        commited_agents.add(agent_id)
            except nx.NetworkXNoCycle:

                longest_path = nx.algorithms.dag_longest_path(comp)
                for x, y in longest_path:
                    agent_id = self.grid[_LAYER_AGENTS, y, x]  #
                    if agent_id:
                        commited_agents.add(agent_id)

        commited_agents = set([self.agents[id_ - 1] for id_ in commited_agents])  #已提交的agent=
        failed_agents = set(self.agents) - commited_agents

        for agent in failed_agents:
            assert agent.req_action == Action.FORWARD
            agent.req_action = Action.NOOP
        # 定义奖励
        rewards = np.zeros(self.n_agents)

        for agent in self.agents: #遍历每个agent
            agent.prev_x, agent.prev_y = agent.x, agent.y

            if agent.req_action == Action.FORWARD:
                agent.x, agent.y = agent.req_location(self.grid_size)
                if agent.carrying_shelf:  # 如果agent携带货架
                    agent.carrying_shelf.x, agent.carrying_shelf.y = agent.x, agent.y   # 那么携带货架的坐标 = Agent 的坐标
            elif agent.req_action in [Action.LEFT, Action.RIGHT]:
                agent.dir = agent.req_direction()
            elif agent.req_action == Action.TOGGLE_LOAD and not agent.carrying_shelf:  # 如果 请求的行动==切换负载 并且没有携带架子
                shelf_id = self.grid[_LAYER_SHELFS, agent.y, agent.x]  # shelf_id=0  判断三维坐标agent是否在架子区域
                if shelf_id:   # 如果 shelf_id==1 (True)
                    agent.carrying_shelf = self.shelfs[shelf_id - 1]  # 那么携带一个架子

            #todo:如果注释掉会导致agent卡在中间出不去
            elif agent.req_action == Action.TOGGLE_LOAD and agent.carrying_shelf:
                if not self._is_highway(agent.x, agent.y):  # 判断agent是否在高速公路上
                    agent.carrying_shelf = None  # 把架子卸下
            # todo:20230812注释（下4行），用于测试
            ###
            #         if agent.has_delivered and self.reward_type == RewardType.TWO_STAGE:  # agent.has_delivered 与下面的自锁，如果下面的代码执行了，这里才会解封
            #             rewards[agent.id - 1] += 0.5
            #             # assert False  #20230803增加用于测试
            #             print(f'rewards_one, {rewards}')

                    # agent.has_delivered = False #todo:20230814注释，用于测试
        #上面的代码并没有一定带上货物才出发  todo:考虑是否带上货物在出发，不考虑使用强化学习来寻找货物，单单是依靠逻辑把货物带上

            # #todo:基于势能给予奖励
            if ((agent.x,agent.y) in self.main_warehouse_left_transverse):  #如果在主仓库横
                diff = agent.x - agent.prev_x
                agent_id = self.grid[_LAYER_AGENTS, agent.x, agent.y]  #
                if self.agents[agent_id - 1].has_delivered == True :
                    if diff > 0:
                        rewards += 0.01
                        print(f'11111111, {rewards}')
                    else:
                        rewards += -0.01
                        print(f'22222222, {rewards}')
                elif self.agents[agent_id - 1].has_delivered == False:
                    if diff > 0:
                        rewards += -0.01
                        print(f'33333333, {rewards}')
                    else:
                        rewards += 0.01
                        print(f'44444444, {rewards}')





        self._recalc_grid()

        shelf_delivered = False
        for y, x in self.goals:  # 遍历集合 goals（y.x）
            # shelf_id = self.grid[_LAYER_SHELFS, x, y]
            # if not shelf_id:
            #     continue  #跳出本次循环
            # shelf = self.shelfs[shelf_id - 1]
            # if shelf not in self.request_queue:
            #     continue
            # todo:20230810修改(上6行被注释)
            agent_id = self.grid[_LAYER_AGENTS, x, y]
            if not agent_id: #先判断agent是否在goal坐标上
                continue  # 跳出本次循环
            agent = self.agents[agent_id - 1] #

            # todo:20230810测试加，判断是否执行下面获得奖励的代码
            if agent.carrying_shelf == None:
                continue

            # a shelf was successfully delived. #货架已成功交付
            shelf_delivered = True

            # remove from queue and replace it  #删除队列并替换它
            # todo:20230727 注释掉，如果需要返回队列，则需要（下4行）
            # new_request = np.random.choice(
            #     list(set(self.shelfs) - set(self.request_queue))
            # )
            # self.request_queue[self.request_queue.index(shelf)] = new_request

            # also reward the agents #也奖励agents
            if self.reward_type == RewardType.GLOBAL:
                rewards += 1
                print(rewards)
            elif self.reward_type == RewardType.INDIVIDUAL:
                agent_id = self.grid[_LAYER_AGENTS, x, y]  #
                rewards[agent_id - 1] += 1
            elif self.reward_type == RewardType.TWO_STAGE:
                agent_id = self.grid[_LAYER_AGENTS, x, y]  #
                self.agents[agent_id - 1].has_delivered = True
                self.agents[agent_id - 1].carrying_shelf = None  # todo:20230808测试加，相当于放下货架
                rewards[agent_id - 1] += 0.5
                print(f'rewards_2, {rewards}')

        #todo:20230812新增，当agent交付成功并返回架子层固定位置（6×9），那么奖励0.5，并且交付改为false，进行下一个运输任务
        for y, x in self.shelfs_fix:
            agent_id = self.grid[_LAYER_AGENTS, x, y]
            if not agent_id:  # 先判断agent是否在shelfs坐标上
                continue  # 跳出本次循环
            agent = self.agents[agent_id - 1]  #
            if self.agents[agent_id - 1].has_delivered == False:  #与上面自锁，如果上面has_delivered=true,这里才能解封
                continue  # 跳出本次循环
            rewards[agent_id - 1] += 0.5
            print(f'rewards_three, {rewards}')
            self.agents[agent_id - 1].has_delivered = False


        if shelf_delivered:
            self._cur_inactive_steps = 0
        else:
            self._cur_inactive_steps += 1
        self._cur_steps += 1

        if (
            self.max_inactivity_steps
            and self._cur_inactive_steps >= self.max_inactivity_steps
        ) or (self.max_steps and self._cur_steps >= self.max_steps):
            dones = self.n_agents * [True]
        else:
            dones = self.n_agents * [False]

        new_obs = tuple([self._make_obs(agent) for agent in self.agents])
        info = {}
        return new_obs, list(rewards), dones, info

    # 定义渲染函数
    def render(self, mode="human"):
        if not self.renderer:
            from rware.rendering import Viewer

            self.renderer = Viewer(self.grid_size)
        return self.renderer.render(self, return_rgb_array=mode == "rgb_array")

    # 关闭渲染
    def close(self):
        if self.renderer:
            self.renderer.close()

    # 定义随机种子
    def seed(self, seed=None):
        ...


if __name__ == "__main__":
    # env = Warehouse(9, 8, 3, 10, 3, 1, 5, None, None, RewardType.GLOBAL)
    env = Warehouse(0, 0, 0, 8, 3, 1, 54, None, None, RewardType.TWO_STAGE)    # 架子列数，列的高度，架子行数，agent数8，交流个数3，传感器观测范围1，#请求队列的大小=5 (同时需要多少个货架)
    env.reset()
    import time
    from tqdm import tqdm

    time.sleep(2)
    env.render()
    # env.step(18 * [Action.LOAD] + 2 * [Action.NOOP])

    # 打印进度条
    for _ in tqdm(range(1000000)):
        # time.sleep(2)
        env.render()
        actions = env.action_space.sample()
        env.step(actions)
