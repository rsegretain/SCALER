trainticket = require("ressources.wrk3_scripts.trainticket")

response = trainticket.response

function init_data()
	trips = load_table("trips_blob")
end

function save_data(threads)
	save_table(threads[1]:get("in_booking_trip"), "in_booking_trip_blob")
end

requests_functions = {
	{
		name = "start_booking", -- the name to display for this function
		func = trainticket.start_booking, -- the function itself
		repartition = 1, -- the repartition value
	}
}