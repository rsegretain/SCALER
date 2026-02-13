trainticket = require("ressources.wrk3_scripts.trainticket")

requests_functions = {
	{
		name = "search_ticket", -- the name to display for this function
		func = trainticket.search_ticket, -- the function itself
		repartition = 1, -- the repartition value
	}
}