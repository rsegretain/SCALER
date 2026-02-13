DEPLOYMENTS = [
	"teastore-webui",
	"teastore-auth",
	"teastore-persistence"
]


THRESHOLDS = [
	523,
	637,
	2082
]

WRK_PROFILE="ressources/wrk3_scripts/add_to_cart.lua"

WARMUP_PROFILE="ressources/wrk3_scripts/add_to_cart.lua"
WARMUP_LOAD_FILE="../global-ressources/load-profiles/linear_loads/linear_1-100_2m.csv"