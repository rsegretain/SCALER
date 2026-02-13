-- Keep that at the start of the script
require("ressources.wrk3_scripts.wrk_script_commons")

-- Global variables

products = {
    '0PUK6V6EV0',
    '1YMWWN1N4O',
    '2ZYFJ3GM2N',
    '66VCHSJNUP',
    '6E92ZMYYFZ',
    '9SIQT8TOJO',
    'L9ECAV7KIM',
    'LS4PSXUNUM',
    'OLJCESPC7Z'
}

currencies = {'EUR', 'USD', 'JPY', 'CAD', 'GBP', 'TRY'}

shop_session_ids = {}

local url_prefix = ""

-- Requests functions

local function index()
	local url = url_prefix .. "/"
	return wrk.format(method.GET, url)
end

local function setCurrency()
	if (#shop_session_ids == 0) then
		error("missing shop session id")
	end

	local url = url_prefix .. "/setCurrency"
	local currency = currencies[math.random(#currencies)]
	local headers = {
		Cookie = shop_session_ids[1] .. "; shop_currency=EUR",
		["Content-Type"] = "application/x-www-form-urlencoded"
	}
	local body = "currency_code=" .. currency
	return wrk.format(method.POST, url, headers, body)
end

local function browseProduct()
	if (#shop_session_ids == 0) then
		error("missing shop session id")
	end

	local url = url_prefix .. "/product"
	local product = products[math.random(#products)]
	url =  url .. "/" .. product
	local headers = {
		Cookie = shop_session_ids[1] .. "; shop_currency=EUR"
	}
	return wrk.format(method.GET, url, headers)
end

local function viewCart()
	if (#shop_session_ids == 0) then
		error("missing shop session id")
	end

	local url = url_prefix .. "/cart"
	local headers = {
		Cookie = shop_session_ids[1] .. "; shop_currency=EUR"
	}
	return wrk.format(method.GET, url, headers)
end

local function addToCart()
	if (#shop_session_ids == 0) then
		error("missing shop session id")
	end

	local url = url_prefix .. "/cart"
	local product = products[math.random(#products)]
	local headers = {
		Cookie = shop_session_ids[1] .. "; shop_currency=EUR",
		["Content-Type"] = "application/x-www-form-urlencoded"
	}
	local body = "product_id=" .. product .. "&quantity=" .. math.random(1,10)

	return wrk.format(method.POST, url, headers, body)
end

local function emptyCart()
	if (#shop_session_ids == 0) then
		error("missing shop session id")
	end

	local url = url_prefix .. "/cart/empty"
	local headers = {
		Cookie = shop_session_ids[1] .. "; shop_currency=EUR"
	}
	local body = ""
	return wrk.format(method.POST, url, headers, body)
end

local function checkout()
	if (#shop_session_ids == 0) then
		error("missing shop session id")
	end

	local url = url_prefix .. "/cart/checkout"
	local headers = {
		Cookie = shop_session_ids[1] .. "; shop_currency=EUR",
		["Content-Type"] = "application/x-www-form-urlencoded"
	}
	local body = "email=someone%40example.com&street_address=1600+Amphitheatre+Parkway&zip_code=94043&city=Mountain+View&state=CA&country=United+States&credit_card_number=4432801561520454&credit_card_expiration_month=1&credit_card_expiration_year=2050&credit_card_cvv=672"

	return wrk.format(method.POST, url, headers, body)
end

local function logout()
	if (#shop_session_ids == 0) then
		error("missing shop session id")
	end

	local url = url_prefix .. "/logout"
	local headers = {
		Cookie = shop_session_ids[1] .. "; shop_currency=EUR"
	}
	return wrk.format(method.GET, url, headers)
end

-- responses handling function

local function response(status, request, headers, body)
	if (headers["set-cookie"]) then
		for _, cookie in ipairs(headers["set-cookie"]) do
			if (cookie:find("shop_session-id", 1, true)) then
				-- print(cookie)
				for v in cookie:gmatch("(shop_session%-id=[a-z0-9%-]*)") do
					-- print(v)
					table.insert(shop_session_ids, v)
				end
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
	index = index,
	setCurrency = setCurrency,
	browseProduct = browseProduct,
	addToCart = addToCart,
	viewCart = viewCart,
	emptyCart = emptyCart,
	checkout = checkout,
	logout = logout,
	response = response
}
