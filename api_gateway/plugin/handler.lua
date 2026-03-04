local jwt_decoder = require "kong.plugins.jwt.jwt_parser"

local JWT2Header = {
  PRIORITY = 900,
  VERSION = "2.0"
}

function JWT2Header:access(conf)
  local token = nil
  local auth_header = kong.request.get_header("Authorization")

  if auth_header then
    token = string.match(auth_header, "^[Bb]earer%s+(.+)$")
  end

  if not token then
    if conf.token_required == "true" then
      return kong.response.exit(401, { error = "No valid JWT token found in Authorization header" })
    else
      return
    end
  end

  local jwt, err = jwt_decoder:new(token)
  if err then
    kong.log.err("Failed to parse JWT: ", tostring(err))
    if conf.token_required == "true" then
      return kong.response.exit(401, { error = "Bad token format or invalid JSON" })
    end
    return
  end

  if jwt.claims then
    for claim, value in pairs(jwt.claims) do
      local val_type = type(value)
      
      if val_type == "string" or val_type == "number" or val_type == "boolean" then
        local header_name = "X-Kong-JWT-Claim-" .. claim
        kong.service.request.set_header(header_name, tostring(value))
      end
    end
  end
  if conf.strip_claims == "true" then
  end
end

return JWT2Header