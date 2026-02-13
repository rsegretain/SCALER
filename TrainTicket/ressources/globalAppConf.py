CPU_LIMIT = 1
CPU_THRESHOLD = 0.7
MAX_LATENCY = 600
FRONTEND="ts-ui-dashboard"

WRK_THREAD_NUMBER=5
WRK_W_CX_RESET=60

INIT_PROFILES=[
	"ressources/wrk3_scripts/init_login.lua",
	"ressources/wrk3_scripts/init_logins_data_contact.lua",
	"ressources/wrk3_scripts/init_trips.lua",
	"ressources/wrk3_scripts/init_in_booking_trips.lua"
]
INIT_LOAD_FILE="../global-ressources/load-profiles/constant_loads/const_1_5-minutes.csv"
INIT_DURATION=20

WARMUP_CONNECTIONS_NUMBER=20

EXPERIMENT_CONNECTIONS_NUMBER=100