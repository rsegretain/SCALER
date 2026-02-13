trainticket = require("ressources.wrk3_scripts.trainticket")

requests_functions = {
	{
		name = "pay", -- the name to display for this function
		func = trainticket.pay, -- the function itself
		repartition = 1, -- the repartition value
	}
}