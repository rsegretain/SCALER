-- Keep that at the start of the script
require("ressources.wrk3_scripts.wrk_script_commons")

-- Global variables

logged_in_blob = {}
product_in_cart_blob = {}

local url_prefix = "/tools.descartes.teastore.webui"

-- Requests functions

local function visit_home()
	local url = url_prefix .. "/"
	return wrk.format(method.GET, url)
end

local function login()
	local url =  url_prefix .. "/loginAction"
	local user_id = math.random(1,90)
	local headers = {
		["Content-Type"] = "application/x-www-form-urlencoded"
	}
	local body = "username=user" .. user_id .. "&password=password"
	return wrk.format(method.POST, url, headers, body)
end

local function browse_category()
	local url = url_prefix .. "/category"
	local category_id = math.random(2,6)
	local page_id = math.random(1, 5)
	url = url .. "?category=" .. category_id .. "&page=" .. page_id
	return wrk.format(method.GET, url)
end

local function browse_product()
	local url = url_prefix .. "/product"
	local product_id = math.random(7, 506)
	url =  url .. "?id=" .. product_id
	return wrk.format(method.GET, url)
end

local function add_to_cart()
	if (#logged_in_blob == 0) then
		error("missing blob")
	end

	local url = url_prefix .. "/cartAction"
	local product_id = math.random(7, 506)
	local headers = {
		Cookie = logged_in_blob[math.random(#logged_in_blob)],
		["Content-Type"] = "application/x-www-form-urlencoded"
	}
	local body = "productid=" .. product_id .. "&addToCart="
	return wrk.format(method.POST, url, headers, body)
end

local function buy()
	if (#product_in_cart_blob == 0) then
		error("missing blob")
	end

	local url = url_prefix .. "/cartAction"
	local headers = {
		Cookie = product_in_cart_blob[math.random(#product_in_cart_blob)],
		["Content-Type"] = "application/x-www-form-urlencoded"
	}
	local body = "firstname=User&lastname=User&address1=Road&address2=City&cardtype=volvo&cardnumber=314159265359&expirydate=12%2F2050&confirm=Confirm"
	return wrk.format(method.POST, url, headers, body)
end

local function visit_profile()
	if (#logged_in_blob == 0) then
		error("missing blob")
	end

	local url = url_prefix .. "/profile"
	local headers = {
		Cookie = logged_in_blob[math.random(#logged_in_blob)]
	}
	return wrk.format(method.GET, url, headers)
end

local function logout()
	if (#logged_in_blob == 0) then
		error("missing blob")
	end

	local url = url_prefix .. "/loginAction"
	local headers = {
		["Content-Type"] = "application/x-www-form-urlencoded"
	}
	local body = "logout="
	return wrk.format(method.POST, url, headers, body)
end

-- responses handling function

local function response(status, request, headers, body)
	if (headers["set-cookie"]) then
		local sessionBlob = nil
		for _, cookie in ipairs(headers["set-cookie"]) do
			if (cookie:find("sessionBlob", 1, true)) then
				sessionBlob = cookie
			elseif (cookie:find("You_are_logged_in!", 1, true)) then

				table.insert(logged_in_blob, sessionBlob)

			elseif (cookie:find("is_added_to_cart!", 1, true)) then
				
				table.insert(product_in_cart_blob, sessionBlob)
				
			end
		end
	end

	if (print_debug) then
		print("########")
		print(request)
		print("STATUS: ", status)
		local content_type = ""
		for k, v in pairs(headers) do
			if (k == "set-cookie") then
				print(k)
				for k1, v1 in pairs(v) do
					print("\t", k1, v1)
				end
			else
				print(k, v)
			end

			if (k:lower():find("content-type", 1, true)) then
				content_type = v
			end
		end
		print("BODY:")
		if body and not content_type:lower():find("html") then
			print(body)
		end
		print("########")
	end
end

return {
	visit_home = visit_home,
	login = login,
	browse_category = browse_category,
	browse_product = browse_product,
	add_to_cart = add_to_cart,
	buy = buy,
	visit_profile = visit_profile,
	logout = logout,
	response = response
}
