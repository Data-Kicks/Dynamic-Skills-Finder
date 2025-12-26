#' @title Scouting Search UI Module
#' @description A Shiny module that provides a user interface for scouting search functionality.
#'
#' @param id A character string that serves as the namespace for the module.
#'
#' @return A Shiny UI element for the scouting search module.
#'
#' @import shiny
#' @importFrom bslib card card_body card_footer card_header
#' @importFrom dplyr filter pull
#' @importFrom shinyWidgets pickerInput pickerOptions
#' @importFrom shinyjs useShinyjs
#'
#' @export
mod_scouting_search_ui <- function(id) {
  ns <- shiny::NS(id)

  seasons <- player_aggregates_data |>
    pull(season_name) |>
    unique() |>
    sort(decreasing = FALSE)

  competitions <- player_aggregates_data |>
    pull(competition_name) |>
    unique() |>
    sort()

  teams <- player_aggregates_data |>
    pull(team_shortname) |>
    unique() |>
    sort()

  positions <- player_aggregates_data |>
    mutate(
      positions = strsplit(as.character(positions), split = ", ")
    ) |>
    pull(positions) |>
    unlist() |>
    unique() |>
    sort()

  max_age <- player_aggregates_data |>
    pull(age) |>
    max(na.rm = TRUE)

  max_matches_played <- player_aggregates_data |>
    pull(matches_played) |>
    max(na.rm = TRUE)

  max_matches_started <- player_aggregates_data |>
    pull(starts) |>
    max(na.rm = TRUE)

  max_minutes_played <- player_aggregates_data |>
    pull(minutes_played) |>
    max(na.rm = TRUE)

  shiny::tagList(
    useShinyjs(),
    shiny::fluidRow(
      shiny::column(
        width = 3,
        card(
          id = ns("filters_card"),
          card_header(
            "Filters"
          ),
          card_body(
            shiny::fluidRow(
              shiny::column(
                width = 6,
                id = ns("filters_left_column"),
                shiny::tags$h5(
                  "Player Info",
                  class = "text-center",
                  style = "color:darkgrey;",
                ),
                pickerInput(
                  inputId = ns("season_select"),
                  label = "Season",
                  choices = seasons,
                  selected = seasons,
                  options = pickerOptions(
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No season selected",
                    countSelectedText = "{0} seasons selected"
                  ),
                  multiple = TRUE
                ),
                pickerInput(
                  inputId = ns("competition_select"),
                  label = "Competition",
                  choices = competitions,
                  selected = competitions,
                  options = pickerOptions(
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No competition selected",
                    countSelectedText = "{0} competitions selected"
                  ),
                  multiple = TRUE
                ),
                pickerInput(
                  inputId = ns("team_select"),
                  label = "Team",
                  choices = teams,
                  selected = teams,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search...",
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No team selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} teams selected"
                  ),
                  multiple = TRUE
                ),
                shiny::textInput(
                  inputId = ns("player_name_input"),
                  label = "Player name",
                  placeholder = "Type player name..."
                ),
                pickerInput(
                  inputId = ns("position_select"),
                  label = "Position",
                  choices = positions,
                  selected = positions,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search...",
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No position selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} positions selected"
                  ),
                  multiple = TRUE
                ),
                shiny::sliderInput(
                  inputId = ns("age_select"),
                  label = "Age",
                  min = 0,
                  max = max_age,
                  value = c(0, max_age),
                  step = 1
                ),
                shiny::sliderInput(
                  inputId = ns("matches_played_select"),
                  label = "Matches played",
                  min = 0,
                  max = max_matches_played,
                  value = c(0, max_matches_played),
                  step = 1
                ),
                shiny::sliderInput(
                  inputId = ns("matches_started_select"),
                  label = "Matches started",
                  min = 0,
                  max = max_matches_started,
                  value = c(0, max_matches_started),
                  step = 1
                ),
                shiny::sliderInput(
                  inputId = ns("minutes_played_select"),
                  label = "Minutes",
                  min = 0,
                  max = max_minutes_played,
                  value = c(0, max_minutes_played),
                  step = 45
                )
              ),
              shiny::column(
                width = 6,
                id = ns("filters_right_column"),
                shiny::tags$h5(
                  "Player metrics",
                  class = "text-center",
                  style = "color:darkgrey;",
                ),
                shiny::uiOutput(ns("custom_selects_output")),
                shiny::actionLink(
                  inputId = ns("add_metric_filter_input"),
                  label = "Add filter..."
                )
              )
            )
          ),
          card_footer(
            shiny::fluidRow(
              shiny::column(
                width = 3,
                shiny::actionButton(
                  inputId = ns("apply_filters_button"),
                  label = "Apply",
                  width = "100%"
                ),
                offset = 9
              )
            )
          ),
        )
      ),
      shiny::column(
        width = 9,
        card(
          card_header(
            "Results"
          ),
          card_body(
            shiny::textOutput(ns("no_results_label")),
            shiny::uiOutput(ns("results_ui"))
          )
        )
      )
    )
  )
}
