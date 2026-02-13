trainticket = require("ressources.wrk3_scripts.trainticket")

response = trainticket.response

function save_data(threads)
	save_table(threads[1]:get("trips"), "trips_blob")
end

requests_functions = {
	{
		name = "search_ticket", -- the name to display for this function
		func = trainticket.search_ticket, -- the function itself
		repartition = 1, -- the repartition value
	}
}