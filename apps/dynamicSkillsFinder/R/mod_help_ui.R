#' @title Help UI Module
#' @description Shiny module for displaying help videos.
#'
#' @param id Module ID.
#'
#' @return Shiny UI elements for the help module.
#'
#' @import shiny
#'
#' @export
mod_help_ui <- function(id, data) {
  ns <- shiny::NS(id)

  shiny::tagList(
    shiny::fluidRow(
      shiny::column(
        width = 12,
        card(
          card_header(
            "Help videos"
          ),
          card_body(
            shiny::br(),
            shiny::fluidRow(
              shiny::column(
                width = 4,
                align = "center",
                shiny::h5(
                  "Tactical Analysis Module",
                  style = "color:darkgrey;"
                ),
                shiny::tags$iframe(
                  id = ns("tactical_analysis_video"),
                  src = "https://www.youtube.com/embed/p-fiLBkwYXM?si=E3FsX6Iav3cp9RTq",
                  width = "100%",
                  height = "450",
                  frameborder = "0",
                  allow = "accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
                  referrerpolicy = "strict-origin-when-cross-origin",
                  allowfullscreen = TRUE
                ),
                offset = 2
              ),
              shiny::column(
                width = 4,
                align = "center",
                shiny::h5("Player Scouting Module", style = "color:darkgrey;"),
                shiny::tags$iframe(
                  id = ns("player_scouting_video"),
                  src = "https://www.youtube.com/embed/4krPNHg3Owg?si=NMhgy_e7NsmMVv5c",
                  width = "100%",
                  height = "450",
                  frameborder = "0",
                  allow = "accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
                  referrerpolicy = "strict-origin-when-cross-origin",
                  allowfullscreen = TRUE
                )
              )
            ),
            shiny::br(),
            shiny::br(),
            shiny::fluidRow(
              shiny::column(
                width = 4,
                align = "center",
                shiny::h5("Comparison Tool", style = "color:darkgrey;"),
                shiny::tags$iframe(
                  id = ns("comparison_tool_video"),
                  src = "https://www.youtube.com/embed/6cPAljbV4So?si=JERxl9u-6b5FkNZn",
                  width = "100%",
                  height = "450",
                  frameborder = "0",
                  allow = "accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
                  referrerpolicy = "strict-origin-when-cross-origin",
                  allowfullscreen = TRUE
                ),
                offset = 4
              )
            )
          )
        )
      )
    )
  )
}
