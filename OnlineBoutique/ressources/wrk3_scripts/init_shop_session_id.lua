onlineboutique = require("ressources.wrk3_scripts.onlineboutique")

response = onlineboutique.response

function save_data(threads)
	shop_session_ids = threads[1]:get("shop_session_ids")
	while #shop_session_ids > 1 do
		table.remove(shop_session_ids)
	end
	save_table(shop_session_ids, "shop_session_ids")
end

requests_functions = {
	{
		name = "index",
		func = onlineboutique.index,
		repartition = 1
	}
}