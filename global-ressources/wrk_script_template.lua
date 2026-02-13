-- Keep that at the start of the script
-- point to a link you must create, the actual file is in global-ressources
require("ressources.wrk3_scripts.wrk_script_commons")

-- Global variables / functions

-- Requests functions

local function myfunction()
	local url = "/endpoint"
	local headers = {}
	local body = ""
	return wrk.format(method.GET, url, headers, body)
end


-- responses handling function

function response(status, request, headers, body)
    if (print_debug) then
        print("########")
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

-- Keep the following at the end of the script

--[[
	For each request function, add a subtable in 'requests_functions' like :
	{
		name = "myfunctionname", -- the name to display for this function
		func = myfunction, -- the function itself
		repartition = 1, -- the repartition value
	}
]]

requests_functions = {
	{
		name = "myfunctionname", -- the name to display for this function
		func = myfunction, -- the function itself
		repartition = 1, -- the repartition value
	}
}