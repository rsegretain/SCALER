teastore = require("ressources.wrk3_scripts.teastore")

response = teastore.response

function save_data(threads)
	logged_in_blob = threads[1]:get("logged_in_blob")
	save_table(logged_in_blob, "logged_in_blob")
end

requests_functions = {
	{
		name = "login",
		func = teastore.login,
		repartition = 1
	}
}