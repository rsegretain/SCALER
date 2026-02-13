DEPLOYMENTS = [
	"teastore-webui",
	"teastore-persistence",
	"teastore-auth",
	"teastore-image"
]


THRESHOLDS = [
	77,
	584,
	705,
	2174
]

WRK_PROFILE="ressources/wrk3_scripts/visit_profile.lua"

WARMUP_PROFILE="ressources/wrk3_scripts/visit_profile.lua"
WARMUP_LOAD_FILE="../global-ressources/load-profiles/linear_loads/linear_1-100_2m.csv"