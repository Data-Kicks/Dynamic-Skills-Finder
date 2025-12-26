#' @title Event Video Module
#' @description A Shiny module to display dynamic event video and related information.
#' @param id Module ID.
#' @param data A data frame containing event information.
#'
#' @return A Shiny UI and server module for displaying event video and information.
#'
#' @import shiny
#' @importFrom dplyr pull
#'
#' @export
mod_event_video_ui <- function(id, data) {
  ns <- shiny::NS(id)

  shiny::tagList(
    shiny::fluidRow(
      shiny::column(
        width = 8,
        shiny::uiOutput(ns("video_ui_output")),
        shiny::actionButton(
          ns("video_reload_input"),
          label = "Reload",
          title = "Reload"
        )
      ),
      shiny::column(
        width = 4,
        shiny::tags$div(
          id = ns("event_info_div"),
          class = "text-center",
          shiny::tags$h4(
            "Match"
          ),
          shiny::tags$h5(
            data |> pull(match_longname)
          ),
          shiny::tags$br(),
          shiny::tags$h4(
            "Team"
          ),
          shiny::tags$h5(
            data |> pull(team_shortname)
          ),
          shiny::tags$br(),
          shiny::tags$h4(
            "Player"
          ),
          shiny::tags$h5(
            paste0(
              "#",
              data |> pull(player_number),
              " - ",
              data |> pull(player_name),
              " - ",
              data |> pull(player_position)
            )
          ),
          shiny::tags$br(),
          shiny::tags$h4(
            "Period"
          ),
          shiny::tags$h5(
            data |> pull(period)
          ),
          shiny::tags$br(),
          shiny::tags$h4(
            "Time"
          ),
          shiny::tags$h5(
            data |> pull(time_start)
          ),
          shiny::tags$br(),
          shiny::tags$h4(
            "Game state"
          ),
          shiny::tags$h5(
            data |> pull(game_state)
          ),
          shiny::tags$br(),
          shiny::tags$h4(
            "Event subtype"
          ),
          shiny::tags$h5(
            data |> pull(event_subtype)
          ),
        )
      )
    )
  )
}


#' @title Event Video Module Server
#' @description Server logic for the Event Video Module.
#'
#' @param id Module ID.
#' @param data A data frame containing event information.
#'
#' @return Server logic for displaying dynamic event video and information.
#'
#' @import shiny
#' @importFrom dplyr pull
#'
#' @export
mod_event_video_server <- function(id, data) {
  shiny::moduleServer(id, function(input, output, session) {
    ns <- session$ns

    output$video_ui_output <- shiny::renderUI({
      shiny::tagList(
        shiny::tags$iframe(
          id = ns("dynamic_event_video"),
          src = paste0(
            "https://www.youtube.com/embed/",
            data |> pull(youtube_video_id),
            "&amp;start=",
            data |> pull(event_start_seconds),
            "&amp;end=",
            data |> pull(event_end_seconds),
            "&amp;controls=0&amp;autoplay=1&mute=1"
          ),
          width = "100%",
          height = "500"
        )
      )
    })

    observeEvent(input$video_reload_input, {
      output$video_ui_output <- shiny::renderUI({
        shiny::tagList(
          shiny::tags$iframe(
            id = ns("dynamic_event_video"),
            src = paste0(
              "https://www.youtube.com/embed/",
              data |> pull(youtube_video_id),
              "&amp;start=",
              data |> pull(event_start_seconds),
              "&amp;end=",
              data |> pull(event_end_seconds),
              "&amp;controls=0&amp;autoplay=1&mute=1"
            ),
            width = "100%",
            height = "500"
          )
        )
      })
    })
  })
}
