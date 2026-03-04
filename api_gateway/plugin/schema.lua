local typedefs = require "kong.db.schema.typedefs"

return {
  name = "jwt-to-header",
  fields = {
    {
      config = {
        type = "record",
        fields = {
          { strip_claims = { type = "string", required = true, default = "false" } },
          { token_required = { type = "string", required = true, default = "true" } },
        },
      },
    },
  },
}