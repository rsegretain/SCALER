trainticket = require("ressources.wrk3_scripts.trainticket")

function init_data()
	logins_data = load_table("logins_data_blob")
	logins_data_contact = load_table("logins_data_contact_blob")
	trips = load_table("trips_blob")
	in_booking_trip = load_table("in_booking_trip_blob")
end

requests_functions = {
	-- {
	-- 	name = "start_booking", -- the name to display for this function
	-- 	func = trainticket.start_booking, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	{
		name = "finish_booking", -- the name to display for this function
		func = trainticket.finish_booking, -- the function itself
		repartition = 1, -- the repartition value
	}
}