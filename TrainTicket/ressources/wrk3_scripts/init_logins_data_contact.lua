trainticket = require("ressources.wrk3_scripts.trainticket")

response = trainticket.response

function init_data()
	logins_data = load_table("logins_data_blob")
end

function save_data(threads)
	save_table(threads[1]:get("logins_data_contact"), "logins_data_contact_blob")
end

requests_functions = {
	{
		name = "select_contact", -- the name to display for this function
		func = trainticket.select_contact, -- the function itself
		repartition = 1, -- the repartition value
	}
}