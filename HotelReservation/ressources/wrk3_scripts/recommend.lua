hotel = require("ressources.wrk3_scripts.hotel")

response = hotel.response

requests_functions = {
	{
		name = "recommend",
		func = hotel.recommend,
		repartition = 1 --39
	}
}
