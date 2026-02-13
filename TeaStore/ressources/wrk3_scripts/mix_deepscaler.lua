teastore = require("ressources.wrk3_scripts.teastore")

function init_data()
	logged_in_blob = load_table("logged_in_blob")
	product_in_cart_blob = load_table("product_in_cart_blob")
end

requests_functions = {
	{
		name = "visit_home",
		func = teastore.visit_home,
		repartition = 1
	},
	-- {
	-- 	name = "login",
	-- 	func = teastore.login,
	-- 	repartition = 1
	-- },
	{
		name = "browse_category",
		func = teastore.browse_category,
		repartition = 5
	},
	{
		name = "browse_product",
		func = teastore.browse_product,
		repartition = 5
	},
	{
		name = "add_to_cart",
		func = teastore.add_to_cart,
		repartition = 5
	},
	{
		name = "buy",
		func = teastore.buy,
		repartition = 1
	},
	{
		name = "visit_profile",
		func = teastore.visit_profile,
		repartition = 2
	}
}
