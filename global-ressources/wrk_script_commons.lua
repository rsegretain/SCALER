json = require "ressources.wrk3_scripts.json"

method = {
	GET = "GET",
	POST = "POST",
	PUT = "PUT"
}

print_debug = false

total_repartition = 0
requests_functions = {}
stats = {}

math.randomseed(os.time())

function init (args)
	-- parse the custom args
	if (args and #args > 0) then
		for _, arg in ipairs(args) do
			if(arg:find("debug", 1, true)) then
				print_debug = true
			end

			if(arg:find("stats", 1, true)) then
				print_stats = true
			end
		end
	end

	for _, value in ipairs(requests_functions) do
		total_repartition = total_repartition + value.repartition
	end

	if (init_data and type(init_data) == "function") then
		init_data()
	end
end


function request()
	local request = nil
	local draw = math.random() * total_repartition
	local acc = 0
	for _, value in ipairs(requests_functions) do
		acc = acc + value.repartition
		if draw < acc then
			-- print(value.name)
			request = value.func()
			if (print_stats) then
				if (stats[value.name]) then
					stats[value.name] = stats[value.name] + 1
				else
					stats[value.name] = 1
				end
			end
			break
		end
	end

	if print_debug then
		print("--------\n", request, "\n--------")
	end
	return request
end

-- ########### START OF GLOBAL CONTEXT ###########
-- Those functions are called in the global lua context, different from threads' lua contexts

local threads = {}

-- called once per thread, before running
setup = function(thread)
	-- save the access to thread's data for after
	table.insert(threads, thread)
end

-- called once, after running
done = function (summary, latency, requests)

	if (save_data and type(save_data) == "function") then
		save_data(threads)
	end


	print('-----------------------------------------------------------------------')
	print_stats = threads[1]:get("print_stats")
	if (print_stats) then
		local total_stats = {}
		local total_rqsts = 0
		
		-- fetch the data from each thread context
		for _, thread in ipairs(threads) do
			local thread_stats = thread:get("stats")
			total_repartition = thread:get("total_repartition")
			for k, v in pairs(thread_stats) do
				total_rqsts = total_rqsts + v
				if (total_stats[k]) then
					total_stats[k] = total_stats[k] + v
				else
					total_stats[k] = v
				end
			end
			print_stats = thread:get("print_stats")
		end

		print("\n\t\tCount\t%\trepartition")
		for k, v in pairs(total_stats) do
			local pct = math.floor((v / total_rqsts) * 10000)/10000
			local rep = math.floor(total_repartition * pct * 100) / 100
			print("\n".. k .. ":\n\t", v .. "\t" .. pct * 100 .. "%\t" .. rep)
		end
	end
end

-- ########### END OF GLOBAL CONTEXT ###########

function encode_url_args(base_url, args)
	local url = base_url
	local first = true
	local sep = '?'
	for key, value in pairs(args) do
		url_value = tostring(value):gsub(" ", "%%20")
		url = url .. sep .. key .. '=' .. url_value
		if first then
			sep = '&'
			first = false
		end
	end
	return url
end

function tablelength(t)
  local count = 0
  for _ in pairs(t) do count = count + 1 end
  return count
end


function dump(t, indent)
	if not indent then
		indent = ""
	end
	for k, v in pairs(t) do
		if type(v) == "table" then
			print(indent .. k .. "=")
			dump(v, indent .. "\t")
		elseif type(v) == "string" then
			print(indent .. k .. "= \"" .. v .. "\"")
		else
			print(indent .. k .. "= " .. tostring(v))
		end
	end
end

function save_table(t, filename)
	if not type(t) == "table" then
		error("not a table : " .. filename)
	end
	if tablelength(t) == 0 then
		print("table empty, nothing to save : " .. filename)
		return
	end

	filename = (filename or "table") .. ".json"
	local file = io.open(filename, "w")

	if not file then
		error("can't open file " .. filename)
	end

	local ret, error_msg = file:write(json.encode(t))
	if not ret then
		file:close()
		error(error_msg)
	else
		file:flush()
		file:close()
	end

	print("saved table : " .. filename)
end

function load_table(filename)
	filename = (filename or "table") .. ".json"
	local file = io.open(filename, "r")

	if not file then
		print("No file, returning empty table : " .. filename)
		return {}
	end

	local t = json.decode(file:read("a"))
	file:close()

	print("loaded table : " .. filename)
	return t
end