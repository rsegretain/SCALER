FRONTEND = "teastore-webui"

DEPLOYMENTS = [
	"teastore-webui",
	"teastore-auth",
	"teastore-persistence"
]


THRESHOLDS = [
	406,
	415,
	498

]


WRK_PROFILE="ressources/wrk3_scripts/buy.lua"

WARMUP_PROFILE="ressources/wrk3_scripts/buy.lua"
WARMUP_LOAD_FILE="../global-ressources/load-profiles/linear_loads/linear_1-100_2m.csv"