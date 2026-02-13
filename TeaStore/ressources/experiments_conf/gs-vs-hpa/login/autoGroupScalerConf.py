DEPLOYMENTS = [
	"teastore-webui",
	"teastore-auth"
]


THRESHOLDS = [
	92,
	40
]

WRK_PROFILE="ressources/wrk3_scripts/login.lua"

WARMUP_PROFILE="ressources/wrk3_scripts/login.lua"
WARMUP_LOAD_FILE="../global-ressources/load-profiles/linear_loads/linear_1-100_2m.csv"