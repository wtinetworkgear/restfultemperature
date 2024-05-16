-- Ensure you have luasec for HTTPS support.
-- Install lua-cjson or download json.lua.
-- luarocks install luasec
-- luarocks install lua-cjson

local https = require("ssl.https")
local ltn12 = require("ltn12")
local cjson = require("cjson")  -- You can also use 'json.lua' if preferred
local mime = require 'mime'


-- Address of the WTI device
URI       = "https://"
SITE_NAME = "rest.wti.com"

-- put in the username and password to your WTI device here
BASE_PATH = "/api/v2/status/temperature"
-- BASE_PATH = "/api/v2/token/status/temperature" -- (Used when Token access is required)
-- Define the URL for the API request
local url = URI .. SITE_NAME .. BASE_PATH

local USERNAME = "rest"
local PASSWORD = "restfulpassword"
local credentials = mime.b64(USERNAME .. ":" .. PASSWORD)

-- Set up the headers (if needed)
local headers = {
--    ["X-WTI-API-KEY"] = "usertokenfromWTIdevice", -- (Used when Token access is required)
    ["Authorization"] = "Basic " .. credentials,
    ["Content-Type"] = "application/json"
}

-- Response table to capture the response body
local response_body = {}

-- Make the HTTPS request
print("HTTP request: ", url)
local res, code, response_headers, status = https.request{
    url = url,
    method = "GET",  -- Assuming a GET request based on the endpoint documentation
    headers = headers,
    sink = ltn12.sink.table(response_body)
}

-- Check if the request was successful
if code == 200 then
    -- Combine the response body parts
    local response_str = table.concat(response_body)
    -- Parse the JSON response
    local response_json = cjson.decode(response_str)
    -- print("Parsed JSON Response: ", response_json)
    -- Access specific parts of the response if needed
    -- For example, if the JSON response has a 'temperature' field:
    print("Unit Time:   ", response_json.timestamp)
    print("Temperature: ", response_json.temperature, response_json.format)
else
    print("HTTP request failed with code: ", code)
end
