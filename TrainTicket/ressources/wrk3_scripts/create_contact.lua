trainticket = require("ressources.wrk3_scripts.trainticket")

function init_data()
	logins_data = load_table("logins_data_blob")
end

requests_functions = {
	{
		name = "create_contact", -- the name to display for this function
		func = trainticket.create_contact, -- the function itself
		repartition = 1, -- the repartition value
	}
}