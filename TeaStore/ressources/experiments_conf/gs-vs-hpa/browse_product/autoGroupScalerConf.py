DEPLOYMENTS = [
	"teastore-webui",
	"teastore-persistence",
	"teastore-image"
]


THRESHOLDS = [
	34,
	47,
	285,
]

WRK_PROFILE="ressources/wrk3_scripts/browse_product.lua"

WARMUP_PROFILE="ressources/wrk3_scripts/browse_product.lua"
WARMUP_LOAD_FILE="../global-ressources/load-profiles/linear_loads/linear_1-100_2m.csv"