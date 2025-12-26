#' @title Server logic for the Shiny application
#' @description This function defines the main server logic of the Dynamic Skills Finder Shiny application.
#' It integrates various modules for tactical and scouting functionalities.
#'
#' @param input Shiny input object
#' @param output Shiny output object
#' @param session Shiny session object

server <- function(input, output, session) {
  mod_tactical_find_server("tactical_find")
  mod_compare_server(
    "tactical_compare",
    type = "team"
  )
  mod_scouting_search_server("scouting_search")
  mod_compare_server(
    "scouting_compare",
    type = "player"
  )
}
