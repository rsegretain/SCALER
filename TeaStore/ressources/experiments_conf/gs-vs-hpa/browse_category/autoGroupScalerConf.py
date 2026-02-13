DEPLOYMENTS = [
	"teastore-webui",
	"teastore-persistence",
	"teastore-image"
] 


THRESHOLDS = [
	66,
	100,
	413
]

WRK_PROFILE="ressources/wrk3_scripts/browse_category.lua"

WARMUP_PROFILE="ressources/wrk3_scripts/browse_category.lua"
WARMUP_LOAD_FILE="../global-ressources/load-profiles/linear_loads/linear_1-100_2m.csv"