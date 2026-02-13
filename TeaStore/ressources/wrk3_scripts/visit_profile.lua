teastore = require("ressources.wrk3_scripts.teastore")

function init_data()
	logged_in_blob = load_table("logged_in_blob")
end

requests_functions = {
	{
		name = "visit_profile",
		func = teastore.visit_profile,
		repartition = 1
	}
}
