teastore = require("ressources.wrk3_scripts.teastore")

requests_functions = {
	{
		name = "visit_home",
		func = teastore.visit_home,
		repartition = 1
	},
	{
		name = "browse_category",
		func = teastore.browse_category,
		repartition = 3
	},
	{
		name = "browse_product",
		func = teastore.browse_product,
		repartition = 3
	}
}