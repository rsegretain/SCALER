hotel = require("ressources.wrk3_scripts.hotel")

response = hotel.response

requests_functions = {
	{
		name = "user_login",
		func = hotel.user_login,
		repartition = 1 --0.5
	},
	{
		name = "recommend",
		func = hotel.recommend,
		repartition = 1 --39
	},
	{
		name = "search_hotel",
		func = hotel.search_hotel,
		repartition = 1 --60
	},
	{
		name = "reserve",
		func = hotel.reserve,
		repartition = 1 --0.5
	}
}
