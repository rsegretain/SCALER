teastore = require("ressources.wrk3_scripts.teastore")

function init_data()
	logged_in_blob = load_table("logged_in_blob")
end

requests_functions = {
	{
		name = "add_to_cart",
		func = teastore.add_to_cart,
		repartition = 1
	}
}
