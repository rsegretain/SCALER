DEPLOYMENTS = [
	"teastore-webui",
	"teastore-persistence",
	"teastore-image",
	"teastore-auth"
]


THRESHOLDS = [
	505,
	880,
	2382,
	2839
]

WRK_PROFILE="ressources/wrk3_scripts/visit_home.lua"


WARMUP_PROFILE="ressources/wrk3_scripts/visit_home.lua"
WARMUP_LOAD_FILE="../global-ressources/load-profiles/linear_loads/linear_1-100_2m.csv"