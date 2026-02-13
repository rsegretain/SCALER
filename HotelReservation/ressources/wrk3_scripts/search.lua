hotel = require("ressources.wrk3_scripts.hotel")

response = hotel.response

requests_functions = {
	{
		name = "search_hotel",
		func = hotel.search_hotel,
		repartition = 1 --60
	}
}
