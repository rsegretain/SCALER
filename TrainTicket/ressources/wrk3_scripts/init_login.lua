trainticket = require("ressources.wrk3_scripts.trainticket")

response = trainticket.response

function save_data(threads)
	save_table(threads[1]:get("logins_data"), "logins_data_blob")
end

requests_functions = {
	{
		name = "login", -- the name to display for this function
		func = trainticket.login, -- the function itself
		repartition = 1, -- the repartition value
	}
}