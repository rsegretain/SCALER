teastore = require("ressources.wrk3_scripts.teastore")

response = teastore.response

function init_data()
	logged_in_blob = load_table("logged_in_blob")
end

function save_data(threads)
	product_in_cart_blob = threads[1]:get("product_in_cart_blob")
	save_table(product_in_cart_blob, "product_in_cart_blob")
end

requests_functions = {
	{
		name = "add_to_cart",
		func = teastore.add_to_cart,
		repartition = 1
	}
}