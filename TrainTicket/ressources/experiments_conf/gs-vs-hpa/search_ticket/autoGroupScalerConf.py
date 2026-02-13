DEPLOYMENTS = [
	"ts-travel-service",
	"ts-ticketinfo-service",
	"ts-basic-service",
	"ts-station-service",
	"ts-route-service",
	"ts-seat-service",
	"ts-train-service",
	"ts-order-service",
	"ts-price-service",
	"ts-config-service"
]

# 500ms
THRESHOLDS = [
	25,
	30,
	30,
	30,
	45,
	45,
	40,
	45,
	0,
	0
]

ACTIVELY_SCALED_SERVICES = [0]
PASSIVELY_SCALED_SERVICES = [
	[1,4,5,6,7],
	[2],
	[3],
	[],
	[],
	[],
	[],
	[],
	[],
	[]
]

WRK_PROFILE="ressources/wrk3_scripts/search_ticket.lua"
WARMUP_PROFILE="ressources/wrk3_scripts/search_ticket.lua"
WARMUP_LOAD_FILE="../global-ressources/load-profiles/linear_loads/linear_1-15_10m.csv"
WARMUP_DURATION=600