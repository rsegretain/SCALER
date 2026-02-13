teastore = require("ressources.wrk3_scripts.teastore")

function init_data()
	product_in_cart_blob = load_table("product_in_cart_blob")
end

requests_functions = {
	{
		name = "buy",
		func = teastore.buy,
		repartition = 1
	}
}
