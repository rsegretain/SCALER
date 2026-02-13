hotel = require("ressources.wrk3_scripts.hotel")

response = hotel.response

requests_functions = {
	{
		name = "user_login",
		func = hotel.user_login,
		repartition = 1 --0.5
	}
}
