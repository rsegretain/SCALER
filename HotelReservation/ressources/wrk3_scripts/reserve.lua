hotel = require("ressources.wrk3_scripts.hotel")

response = hotel.response

requests_functions = {
	{
		name = "reserve",
		func = hotel.reserve,
		repartition = 1 --0.5
	}
}
