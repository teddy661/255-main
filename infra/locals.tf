locals {
  instructors = [
    "winegarj@berkeley.edu",
    "mkarch@berkeley.edu",
    "ryan.mitchell@berkeley.edu",
    "viswanathan@berkeley.edu",
    "aford@berkeley.edu"
  ]
  students = [

  ]
  team_mapping = [
    {
      "team" : "tracer",
      "member" : "a47liu@berkeley.edu"
    },
    {
      "team" : "tracer",
      "member" : "lywu@berkeley.edu"
    },
    {
      "team" : "tracer",
      "member" : "judychen@berkeley.edu"
    },
    {
      "team" : "tracer",
      "member" : "jthsiao@berkeley.edu"
    },
    {
      "team" : "eglf",
      "member" : "sean.furuta@berkeley.edu"
    }
  ]
  team_names     = tolist(toset([for member in local.team_mapping : member.team]))
  team_members   = tolist(toset([for member in local.team_mapping : member.member]))
  team_role_list = toset([for member in local.team_mapping : "${member.team}--${member.member}"])
}

locals {
  email_to_id = { for user in data.azuread_users.users.users : user.mail => user.object_id if user.mail != "" }
}
