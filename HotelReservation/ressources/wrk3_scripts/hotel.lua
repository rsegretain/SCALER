-- Keep that at the start of the script
require("ressources.wrk3_scripts.wrk_script_commons")

-- Global variables/functions

local function get_user()
	local id = math.random(0, 500)
	local username = "Cornell_" .. tostring(id)
	local password = ""
	for i = 0, 9, 1 do 
		password = password .. tostring(id)
	end
	return username, password
end

local function get_lat_lon()
	return 38.0235 + (math.random(0, 481) - 240.5)/1000.0, -122.095 + (math.random(0, 325) - 157.0)/1000.0
end

-- Requests functions

local function search_hotel() 
	local in_date = math.random(9, 23)
	local out_date = math.random(in_date + 1, 24)
  
	local in_date_str = tostring(in_date)
	if in_date <= 9 then
	  in_date_str = "2015-04-0" .. in_date_str 
	else
	  in_date_str = "2015-04-" .. in_date_str
	end
  
	local out_date_str = tostring(out_date)
	if out_date <= 9 then
	  out_date_str = "2015-04-0" .. out_date_str 
	else
	  out_date_str = "2015-04-" .. out_date_str
	end
  
	local lat, lon = get_lat_lon()

	local path = "/hotels?inDate=" .. in_date_str .. 
	  "&outDate=" .. out_date_str .. "&lat=" .. tostring(lat) .. "&lon=" .. tostring(lon)
  
	local headers = {}
	-- headers["Content-Type"] = "application/x-www-form-urlencoded"
	return wrk.format(method.GET, path, headers, nil)
  end
  

local function recommend()
	local coin = math.random()
	local req_param = ""
	if coin < 0.33 then
	  req_param = "dis"
	elseif coin < 0.66 then
	  req_param = "rate"
	else
	  req_param = "price"
	end
  
	local lat, lon = get_lat_lon()
  
	local path = "/recommendations?require=" .. req_param .. 
	  "&lat=" .. tostring(lat) .. "&lon=" .. tostring(lon)
	local headers = {}
	-- headers["Content-Type"] = "application/x-www-form-urlencoded"
	return wrk.format(method.GET, path, headers, nil)
  end

local function reserve()
	local in_date = math.random(9, 23)
	local out_date = in_date + math.random(1, 5)
  
	local in_date_str = tostring(in_date)
	if in_date <= 9 then
	  in_date_str = "2015-04-0" .. in_date_str 
	else
	  in_date_str = "2015-04-" .. in_date_str
	end
  
	local out_date_str = tostring(out_date)
	if out_date <= 9 then
	  out_date_str = "2015-04-0" .. out_date_str 
	else
	  out_date_str = "2015-04-" .. out_date_str
	end
  
	local hotel_id = tostring(math.random(1, 80))
	local username, password = get_user()
	local cust_name = username
  
	local num_room = "1"

	local lat, lon = get_lat_lon()
  
	local path = "/reservation?inDate=" .. in_date_str .. 
	  "&outDate=" .. out_date_str .. "&lat=" .. tostring(lat) .. "&lon=" .. tostring(lon) ..
	  "&hotelId=" .. hotel_id .. "&customerName=" .. cust_name .. "&username=" .. username ..
	  "&password=" .. password .. "&number=" .. num_room
	local headers = {}
	-- headers["Content-Type"] = "application/x-www-form-urlencoded"
	return wrk.format(method.POST, path, headers, nil)
  end

local function user_login()
	local username, password = get_user()
	local path = "/user?username=" .. username .. "&password=" .. password
	local headers = {}
	-- headers["Content-Type"] = "application/x-www-form-urlencoded"
	return wrk.format(method.POST, path, headers, nil)
end

-- responses handling function

local function response(status, request, headers, body)
	if (print_debug) then
        print("########")
		print(request)
        print("STATUS: ", status)
        for k, v in pairs(headers) do
            if (k == "set-cookie") then
                print(k)
                for k1, v1 in pairs(v) do
                    print("\t", k1, v1)
                end
            else
                print(k, v)
            end
        end
        print("########")
    end
end


return {
	user_login = user_login,
	recommend = recommend,
	search_hotel = search_hotel,
	reserve = reserve,
	response = response
}
