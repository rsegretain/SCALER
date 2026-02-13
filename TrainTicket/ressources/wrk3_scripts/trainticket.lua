-- Keep that at the start of the script
-- point to a link you must create, the actual file is in global-ressources
require("ressources.wrk3_scripts.wrk_script_commons")

-- Global variables / functions

logins_data = {}
logins_data_contact = {}
trips = {}
in_booking_trip = {}

local unpaid_orders = {}
local paid_orders = {}
local collected_orders = {}

TRAVEL_DATES = {
	'2025-04-11', '2025-04-12', '2025-04-13', '2025-04-14',
	'2025-04-15', '2025-04-16', '2025-04-17', '2025-04-18',
	'2025-04-19', '2025-04-20','2025-04-21', '2025-04-22',
	'2025-04-23', '2025-04-24', '2025-04-25', '2025-04-26',
	'2025-04-27', '2025-04-28', '2025-05-01', '2025-05-04',
	'2025-05-05', '2025-05-04','2025-05-05', '2025-05-06',
	'2025-05-07', '2025-05-08', '2025-05-09','2025-05-10',
	'2025-05-11', '2025-05-12'
}

-- ["nanjing","zhenjiang","wuxi","suzhou","shanghai"]
-- ["nanjing","shanghai"]
-- ["nanjing","suzhou","shanghai"]
-- ["suzhou","shanghai"]
-- ["shanghai","suzhou"]
-- ["shanghai","nanjing","shijiazhuang","taiyuan"]
-- ["nanjing","xuzhou","jinan","beijing"]
-- ["taiyuan","shijiazhuang","nanjing","shanghai"]
-- ["shanghai","taiyuan"]
-- ["shanghaihongqiao","jiaxingnan","hangzhou"]

-- the five first are in travelservice
-- the five last are in travel2service
local ROUTES = {
	{"Shang Hai","Su Zhou"},
	{"Su Zhou","Shang Hai"},
	{"Nan Jing","Zhen Jiang","Wu Xi","Su Zhou","Shang Hai"},
	{"Nan Jing","Su Zhou","Shang Hai"},
	{"Nan Jing","Shang Hai"}--,

	-- {"Shang Hai Hong Qiao","Jia Xing Nan","Hang Zhou"},
	-- {"Shang Hai","Tai Yuan"},
	-- {"Tai Yuan","Shi Jia Zhuang","Nan Jing","Shang Hai"},
	-- {"Nan Jing","Xu Zhou","Ji Nan","Bei Jing"},
	-- {"Shang Hai","Nan Jing","Shi Jia Zhuang","Tai Yuan"}
}


-- Requests functions

-- home
-- GET /index.html
local function home()
	local url = "/index.html"
	return wrk.format(method.GET, url)
end

-- login:
-- POST /api/v1/users/login
local function login()
	local url = "/api/v1/users/login"
	local headers = {
        ["Content-Type"] = "application/json"
    }
	local body = '{"username": "fdse_microservice", "password": "111111"}'
	return wrk.format(method.POST, url, headers, body)
end

-- search_ticket
-- POST /api/v1/travelservice/trips/left
local function search_ticket()

	local urls = {
		"/api/v1/travelservice/trips/left"--,
		-- "/api/v1/travel2service/trips/left"
	}
	local route_idx = math.random(#ROUTES)
	-- the five first are in travelservice, the five last are in travel2service
	local url = urls[1]--urls[math.floor((route_idx - 1) / 5) + 1]
	
	local headers = {
		['Content-Type'] = "application/json"
	}
	local route = ROUTES[route_idx]
	local start_id = math.random(#route - 1)
	local end_id = math.random(start_id + 1, #route)
	local travel_date = os.date("*t")
	travel_date.day = travel_date.day + 1
	travel_date = os.date("%Y-%m-%d", os.time(travel_date))
	local body = json.encode({
		startingPlace = route[start_id],
		endPlace = route[end_id],
		departureTime = travel_date
	})
	return wrk.format(method.POST, url, headers, body)
end

-- start_booking:
-- GET /client_ticket_book.html
local function start_booking()
	if #trips == 0 then
		error("missing blob")
	end

	local url = "/client_ticket_book.html"
	local trip = trips[math.random(#trips)]
	local seats = {
		{
			type = 2,
			price = trip.priceForConfortClass
		},
		{
			type = 3,
			price = trip.priceForEconomyClass
		}
	}
	local seat = seats[math.random(2)]
	local travel_date = os.date("*t")
	travel_date.day = travel_date.day + 1
	travel_date = os.date("%Y-%m-%d", os.time(travel_date))

	url = encode_url_args(
		url,
		{
			tripId = trip.tripId.type .. trip.tripId.number,
			from = trip.startingStation,
			to = trip.terminalStation,
			seatType = seat.type,
			seat_price = seat.price,
			date = travel_date
		}
	)
	return wrk.format(method.GET, url)
end

-- get_assurance_types:
-- GET /api/v1/assuranceservice/assurances/types
local function get_assurance_types()
	if (#logins_data == 0) then
		error("missing blob")
	end

	local url = "/api/v1/assuranceservice/assurances/types"
	local headers = {
		Authorization = "Bearer " .. logins_data[math.random(#logins_data)].token
	}
	return wrk.format(method.GET, url, headers)
end

-- get_foods:
-- GET /api/v1/foodservice/foods/
local function get_foods()
	if #logins_data == 0 then
		error("missing blob")
	end
	if #in_booking_trip == 0 then
		error("missing blob")
	end

	local trip = in_booking_trip[math.random(#in_booking_trip)]
	local url = "/api/v1/foodservice/foods/" .. trip.date .. "/" .. trip.from .. "/" .. trip.to .. "/" .. trip.tripId
	local headers = {
		Authorization = "Bearer " .. logins_data[math.random(#logins_data)].token
	}
	return wrk.format(method.GET, url, headers)
end

-- select_contact:
-- GET /api/v1/contactservice/contacts/account/
local function select_contact()
	if #logins_data == 0 then
		error("missing blob")
	end

	local login_data = logins_data[math.random(#logins_data)]

	local url = "/api/v1/contactservice/contacts/account/" .. login_data.userId
	local headers = {
		Authorization = "Bearer " .. login_data.token
	}
	-- local body = ""
	return wrk.format(method.GET, url, headers)
end

-- create_contact
-- POST /api/v1/contactservice/contacts
local function create_contact()
	if #logins_data == 0 then
		error("missing blob")
	end

	local login_data = logins_data[math.random(#logins_data)]

	local url = "/api/v1/contactservice/contacts"
	local headers = {
		['Content-Type'] = "application/json",
		Authorization = "Bearer " .. login_data.token
	}
	local body = json.encode({
		name = login_data.userId,
		accountId = login_data.userId,
		documentType = "1",
		documentNumber = login_data.userId,
		phoneNumber = "123456"
	})
	return wrk.format(method.POST, url, headers, body)
end

-- finish_booking
-- POST /api/v1/preserveservice/preserve
-- POST /api/v1/preserveotherservice/preserveOther
local function finish_booking()
	if #logins_data_contact == 0 then
		error("missing blob")
	end
	if #in_booking_trip == 0 then
		error("missing blob")
	end

	local ldc = logins_data_contact[math.random(#logins_data_contact)]
	local trip = in_booking_trip[math.random(#in_booking_trip)]
	local seats = {
		{
			type = "2",
			price = trip.priceForConfortClass
		},
		{
			type = "3",
			price = trip.priceForEconomyClass
		}
	}
	local seat = seats[math.random(2)]
	local travel_date = os.date("*t")
	travel_date.day = travel_date.day + 1
	travel_date = os.date("%Y-%m-%d", os.time(travel_date))
	
	-- that's how the app js choose the url...
	local url = ""
	local tripType = trip.tripId:sub(1,1)
	if (tripType == "G" or tripType == "D") then
		url = "/api/v1/preserveservice/preserve"
	else
		url = "/api/v1/preserveotherservice/preserveOther"
	end

	local headers = {
		['Content-Type'] = "application/json",
		Authorization = "Bearer " .. ldc.token
	}

	local body = json.encode({
		accountId = ldc.userId,
		contactsId = ldc.contact.id,
		tripId = trip.tripId,
		-- seatType = trip.seatType,
		date = trip.date,
		from = trip.from:gsub("%%20", " "),
		to = trip.to:gsub("%%20", " "),
		-- assurance = "0",
		-- foodType = 1,
		-- stationName = "",
		-- storeName = "",
		-- foodName = "Bone Soup",
		-- foodPrice = 2.5
	})
	return wrk.format(method.POST, url, headers, body)
end

-- select_order
-- POST /api/v1/orderservice/order/refresh
local function select_order()
	if #logins_data == 0 then
		error("missing blob")
	end
	local ld = logins_data[math.random(#logins_data)]

	local urls = {
		"/api/v1/orderservice/order/refresh"--,
		-- "/api/v1/orderOtherService/orderOther/refresh"
	}
	local url = urls[math.random(#urls)]
	local headers = {
		['Content-Type'] = "application/json",
		Authorization = "Bearer " .. ld.token
	}
	local body = json.encode({
		loginId = ld.userId
	})
	return wrk.format(method.POST, url, headers, body)
end

-- pay
-- POST /api/v1/inside_pay_service/inside_payment
local function pay()
	if #logins_data == 0 then
		error("missing blob")
	end
	if (#unpaid_orders == 0) then
		return math.random() < 0.5 and select_order() or finish_booking()
	end
	
	local ld = logins_data[math.random(#logins_data)]
	local order = table.remove(unpaid_orders, math.random(#unpaid_orders))
	local url = "/api/v1/inside_pay_service/inside_payment"
	local headers = {
		['Content-Type'] = "application/json",
		Authorization = "Bearer " .. ld.token
	}
	local body = json.encode({
		orderId = order.id,
		tripId = order.trainNumber
	})
	return wrk.format(method.POST, url, headers, body)
end

-- GET /api/v1/executeservice/execute/collected/<order_id>
local function collect()
	if #logins_data == 0 then
		error("missing blob")
	end
	if (#paid_orders == 0) then
		return math.random() < 0.5 and select_order() or pay()
	end
	
	local ld = logins_data[math.random(#logins_data)]
	local order = table.remove(paid_orders, math.random(#paid_orders))

	local url = "/api/v1/executeservice/execute/collected/" .. order.id
	local headers = {
		Authorization = "Bearer " .. ld.token
	}
	return wrk.format(method.GET, url, headers)
end

-- GET /api/v1/executeservice/execute/execute/<order_id>
local function enter_station()
	if #logins_data == 0 then
		error("missing blob")
	end
	if (#collected_orders == 0) then
		return math.random() < 0.5 and select_order() or collect()
	end
	
	local ld = logins_data[math.random(#logins_data)]
	local order = table.remove(collected_orders, math.random(#collected_orders))

	local url = "/api/v1/executeservice/execute/execute/" .. order.id
	local headers = {
		Authorization = "Bearer " .. ld.token
	}
	return wrk.format(method.GET, url, headers)
end

-- get_consigns
-- GET /api/v1/consignservice/consigns/order/
local function get_consigns()
	local url = ""
	local headers = {}
	local body = ""
	return wrk.format(method.GET, url, headers, body)
end

-- confirm_consign
-- PUT /api/v1/consignservice/consigns
local function confirm_consign()
	local url = ""
	local headers = {}
	local body = ""
	return wrk.format(method.GET, url, headers, body)
end


-- responses handling function

local function response(status, request, headers, body)

	if (request:find("POST /api/v1/users/login", 1, true) and status == 200) then
		json_response = json.decode(body)
		if json_response.status == 1 and json_response.data then
			table.insert(logins_data, json_response.data)
		end
	end

	if (request:find("POST /api/v1/travel%d?service/trips/left") and status == 200) then
		json_response = json.decode(body)
		if json_response.status == 1 then
			for _, value in ipairs(json_response.data) do
				table.insert(trips, value)
			end
		end
	end

	if (request:find("GET /client_ticket_book.html", 1, true) and status == 200) then
		local _, _, args = request:find("client_ticket_book%.html%?([^%s]*).*")
		local trip = {}
		for k, v in args:gmatch("([^&=]+)=([^&]+)") do
			trip[k] = v
		end
		table.insert(in_booking_trip, trip)
		-- dump(trip)
	end

	
	if (request:find("GET /api/v1/contactservice/contacts/account/", 1, true) and status == 200) then
		json_response = json.decode(body)
		if json_response.status == 1 and json_response.data and #json_response.data > 0  then
			local contact = json_response.data[1]
			for _, ld in ipairs(logins_data) do
				if (ld.userId == contact.accountId) then
					ld.contact = contact
					table.insert(logins_data_contact, ld)
					break
				end
			end
		end
	end

	if ((request:find("POST /api/v1/orderservice/order/refresh", 1, true) or request:find("POST /api/v1/orderOtherService/orderOther/refresh", 1, true) )and status == 200) then
		json_response = json.decode(body)
		if json_response.status == 1 and json_response.data then

			local function insert_if_unknown(t, order)
				local unknown_order = true
				for _, value in pairs(t) do
					if value.id == order.id then
						unknown_order = false
						break
					end
				end
				if unknown_order then
					-- print("\n INSERT \n")
					table.insert(t, order)
				end
			end

			-- 0: not paid
			-- 1: Paid & Not Collected
			-- 2: Collected
			-- 3: Cancel & Rebook
			-- 4: Cancel
			-- 5: Refunded
			-- 6: Used
			for _, order in ipairs(json_response.data) do
				if order.status == 0 then
					insert_if_unknown(unpaid_orders, order)
				elseif order.status == 1 then
					insert_if_unknown(paid_orders, order)
				elseif order.status == 2 then
					insert_if_unknown(collected_orders, order)
				end
			end
		end

		-- print("unpaid_orders: ", #unpaid_orders)
		-- print("paid_orders: ", #paid_orders)
		-- print("collected_orders: ", #collected_orders)
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
	home = home, -- the function itself
	login = login, -- the function itself
	search_ticket = search_ticket, -- the function itself
	get_assurance_types = get_assurance_types, -- the function itself
	get_foods = get_foods, -- the function itself
	select_contact = select_contact, -- the function itself
	create_contact = create_contact, -- the function itself
	start_booking = start_booking,
	finish_booking = finish_booking, -- the function itself
	select_order = select_order, -- the function itself
	pay = pay, -- the function itself
	collect = collect, -- the function itself
	enter_station = enter_station, -- the function itself
	response = response
}