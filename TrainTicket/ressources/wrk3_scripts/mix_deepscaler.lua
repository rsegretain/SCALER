trainticket = require("ressources.wrk3_scripts.trainticket")

function init_data()
	logins_data = load_table("logins_data_blob")
	logins_data_contact = load_table("logins_data_contact_blob")
	trips = load_table("trips_blob")
	in_booking_trip = load_table("in_booking_trip_blob")
end

requests_functions = {
	{
		name = "home", -- the name to display for this function
		func = trainticket.home, -- the function itself
		repartition = 1, -- the repartition value
	},
	{
		name = "login", -- the name to display for this function
		func = trainticket.login, -- the function itself
		repartition = 1, -- the repartition value
	},
	{
		name = "search_ticket", -- the name to display for this function
		func = trainticket.search_ticket, -- the function itself
		repartition = 10, -- the repartition value
	},
	-- {
	-- 	name = "start_booking", -- the name to display for this function
	-- 	func = trainticket.start_booking, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	-- {
	-- 	name = "get_assurance_types", -- the name to display for this function
	-- 	func = trainticket.get_assurance_types, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	-- {
	-- 	name = "get_foods", -- the name to display for this function
	-- 	func = trainticket.get_foods, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	{
		name = "select_contact", -- the name to display for this function
		func = trainticket.select_contact, -- the function itself
		repartition = 1, -- the repartition value
	},
	-- {
	-- 	name = "create_contact", -- the name to display for this function
	-- 	func = trainticket.create_contact, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	{
		name = "finish_booking", -- the name to display for this function
		func = trainticket.finish_booking, -- the function itself
		repartition = 1, -- the repartition value
	},
	{
		name = "select_order", -- the name to display for this function
		func = trainticket.select_order, -- the function itself
		repartition = 1, -- the repartition value
	}--,
	-- {
	-- 	name = "pay", -- the name to display for this function
	-- 	func = trainticket.pay, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	-- {
	-- 	name = "collect", -- the name to display for this function
	-- 	func = trainticket.collect, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	-- {
	-- 	name = "enter_station", -- the name to display for this function
	-- 	func = trainticket.enter_station, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	-- {
	-- 	name = "get_consigns", -- the name to display for this function
	-- 	func = get_consigns, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- },
	-- {
	-- 	name = "confirm_consign", -- the name to display for this function
	-- 	func = confirm_consign, -- the function itself
	-- 	repartition = 1, -- the repartition value
	-- }
}