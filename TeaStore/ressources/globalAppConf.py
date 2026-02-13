CPU_LIMIT = 1
CPU_THRESHOLD = 0.7
MAX_LATENCY = 200
FRONTEND="teastore-webui"

INIT_PROFILES=["ressources/wrk3_scripts/init_login.lua", "ressources/wrk3_scripts/init_product_in_cart.lua"]
INIT_LOAD_FILE="../global-ressources/load-profiles/constant_loads/const_1_5-minutes.csv"
INIT_DURATION=20

WARMUP_DURATION=120
WARMUP_CONNECTIONS_NUMBER=20

WRK_THREAD_NUMBER=5
WRK_W_CX_RESET=60
EXPERIMENT_CONNECTIONS_NUMBER=100