from enum import Enum


class TaskStatus(Enum):
	DEFAULT = 0
	RUNNING = 1
	FINISHED = 2
	PAUSE = 3
	FAIL = 4
	DEL = 5

class TaskContorlCmds(Enum):
	DEFAULT = 0
	RESTART = 1
	STOP = 2
	PAUSE = 3
	CONTINUE = 4
	DEL = 5

class CmdIdCenter2Master(Enum):
	INIT_CENTER = 1
	UPDATE_TASK_INFO = 2
	FINISH_TASK = 3

class CmdIdMaster2Center(Enum):
	RESTART = 1
	KILL = 2
	EDIT = 3

class RetcodeMaster2Center(Enum):
	OK = 0 
	TIMEOUT_ERR = 2

class RetcodeCenter2Master(Enum):
	OK = 0
	TIMEOUT_ERR = 2

class RetcodeCl2Ct(Enum):
	OK = 0
	WORKER_CHOOSE_ERROR = 100001
	THREAD_START_ERROR = 100002
	UNKOWN_ERROR = 999999

class RetcodeCenter2Crawler(Enum):
	OK = 0
	TIMEOUT_ERR = 10001

class CmdIdCenter2Crawler(Enum):
	SEND_ONE_REQUEST = 1
	SEND_BATCH_REQUEST = 2
	CHECK_STATUS = 3

class CmdIdCl2Ct(Enum):
	REPORT_ONE_REQUEST = 1
	REPORT_BATCH_REQUEST = 2
	REPORT_STATUS = 3

class CrawlType(Enum):
	LOGIN_JS = 10
	LOGIN_PY = 11
	VIEW_DIRECTLY = 20 # request http(s)
	VIEW_JS = 21 # use js engine to view
	VIEW_SPEC = 22 # view By site
	VOTE_JS = 30 # vote by js engine
	VOTE_SPEC = 31 # vote by site
	SHARE_JS = 40 # share by js engine
	SHARE_SPEC = 41 # share by site

