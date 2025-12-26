#' @title Player Info UI Module
#' @description Shiny module for displaying player information and a pizza plot.
#'
#' @param id Module ID.
#' @param data Data frame containing player information.
#'
#' @return Shiny UI elements for the player info module.
#'
#' @import shiny
#' @importFrom dplyr pull
#' @importFrom ggiraph girafeOutput
#' @importFrom shinycssloaders withSpinner
#'
#' @export
mod_player_info_ui <- function(id, data) {
  ns <- shiny::NS(id)

  shiny::tagList(
    shiny::fluidRow(
      shiny::tags$div(
        id = ns("player_title_div"),
        class = "text-center",
        shiny::tags$h3(
          data |> pull(player_name)
        )
      )
    ),
    shiny::fluidRow(
      shiny::column(
        width = 6,
        shiny::tags$div(
          id = ns("player_info_div"),
          class = "text-center",
          shiny::br(),
          shiny::fluidRow(
            id = ns("player_info_row1"),
            shiny::column(
              width = 4,
              shiny::tags$h4(
                "Season",
              ),
              shiny::tags$h5(
                data |> pull(season_name),
              )
            ),
            shiny::column(
              width = 4,
              shiny::tags$h4(
                "Competition",
              ),
              shiny::tags$h5(
                data |> pull(competition_name),
              )
            ),
            shiny::column(
              width = 4,
              shiny::tags$h4(
                "Team",
              ),
              shiny::tags$h5(
                data |> pull(team_shortname),
              )
            )
          ),
          shiny::tags$br(),
          shiny::fluidRow(
            id = ns("player_info_row2"),
            shiny::column(
              width = 4,
              shiny::tags$h4(
                "Position",
              ),
              shiny::tags$h5(
                data |> pull(positions),
              )
            ),
            shiny::column(
              width = 4,
              shiny::tags$h4(
                "Age",
              ),
              shiny::tags$h5(
                data |> pull(age),
              )
            )
          ),
          shiny::tags$br(),
          shiny::fluidRow(
            id = ns("player_info_row3"),
            shiny::column(
              width = 4,
              shiny::tags$h4(
                "Minutes played",
              ),
              shiny::tags$h5(
                data |> pull(minutes_played),
              )
            ),
            shiny::column(
              width = 4,
              shiny::tags$h4(
                "Matches played",
              ),
              shiny::tags$h5(
                data |> pull(matches_played),
              )
            ),
            shiny::column(
              width = 4,
              shiny::tags$h4(
                "Matches started",
              ),
              shiny::tags$h5(
                data |> pull(starts),
              )
            )
          )
        )
      ),
      shiny::column(
        width = 6,
        shiny::br(),
        shiny::textOutput(
          ns("no_results_label")
        ),
        withSpinner(
          girafeOutput(
            ns("player_pizzaplot_output"),
            width = "100%"
          ),
          color = "#00a82f",
          type = 7
        )
      )
    )
  )
}
