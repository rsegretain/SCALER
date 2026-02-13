onlineboutique = require("ressources.wrk3_scripts.onlineboutique")

response = onlineboutique.response

function init_data()
	shop_session_ids = load_table("shop_session_ids")
end

requests_functions = {
	{
		name = "browseProduct",
		func = onlineboutique.browseProduct,
		repartition = 1
	}
}