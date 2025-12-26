#' @title Comparison Module UI
#' @description A Shiny module UI function for comparing players or teams based on selected metrics.
#'
#' @param id A character string specifying the module ID.
#' @param type A character string specifying the type of comparison: "player" or "team". Default is "player".
#'
#' @return A Shiny UI element for the comparison module.
#'
#' @import shiny
#' @importFrom bslib card card_header card_body card_footer
#' @importFrom dplyr filter first pull
#' @importFrom shinyWidgets pickerInput pickerOptions
#' @importFrom ggiraph girafeOutput
#' @importFrom shinycssloaders withSpinner
#'
#' @export
mod_compare_ui <- function(id, type = "player") {
  ns <- shiny::NS(id)

  if (type == "player") {
    comparison_data <- player_aggregates_data
    metrics <- sort(names(player_agg_metric_columns))
  } else if (type == "team") {
    comparison_data <- team_aggregates_data
    metrics <- sort(names(team_agg_metric_columns))
  }

  seasons <- comparison_data |>
    pull(season_name) |>
    unique() |>
    sort(decreasing = FALSE)

  competitions <- comparison_data |>
    pull(competition_name) |>
    unique() |>
    sort()

  teams <- comparison_data |>
    pull(team_shortname) |>
    unique() |>
    sort()

  shiny::tagList(
    shiny::tags$head(tags$script(
      src = "https://code.jquery.com/ui/1.13.0/jquery-ui.js"
    )),
    shiny::fluidRow(
      shiny::column(
        width = 3,
        card(
          card_header(
            "Options"
          ),
          card_body(
            shiny::fluidRow(
              shiny::column(
                width = 6,
                id = ns("filters_left_column"),
                shiny::tags$h5(
                  "Filters",
                  class = "text-center",
                  style = "color:darkgrey;",
                ),
                pickerInput(
                  inputId = ns("season_select"),
                  label = "Seasons",
                  choices = seasons,
                  selected = seasons,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No season selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} seasons selected"
                  ),
                  multiple = TRUE
                ),
                pickerInput(
                  inputId = ns("competition_select"),
                  label = "Competitions",
                  choices = competitions,
                  selected = competitions,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No competition selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} competitions selected"
                  ),
                  multiple = TRUE
                ),
                pickerInput(
                  inputId = ns("team_select"),
                  label = "Teams",
                  choices = teams,
                  selected = teams,
                  options = pickerOptions(
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search...",
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No team selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} teams selected"
                  ),
                  multiple = TRUE
                ),
                shiny::uiOutput(ns("minutes_played_ui")),
              ),
              shiny::column(
                width = 6,
                id = ns("filters_right_column"),
                shiny::tags$h5(
                  "Plot parameters",
                  class = "text-center",
                  style = "color:darkgrey;",
                ),
                pickerInput(
                  inputId = ns("x_axis_metric_select"),
                  label = "x-Axis metric",
                  choices = metrics,
                  selected = first(metrics),
                  options = pickerOptions(
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search..."
                  )
                ),
                pickerInput(
                  inputId = ns("y_axis_metric_select"),
                  label = "y-Axis metric",
                  choices = metrics,
                  selected = first(metrics),
                  options = pickerOptions(
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search..."
                  )
                ),
                pickerInput(
                  inputId = ns("size_metric_select"),
                  label = "Point size metric",
                  choices = c("None", metrics),
                  selected = "None",
                  options = pickerOptions(
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search..."
                  )
                ),
                shiny::checkboxInput(
                  inputId = ns("label_outliers_input"),
                  label = paste0("Label outstanding ", type, "s"),
                  value = FALSE
                ),
                shiny::checkboxInput(
                  inputId = ns("invert_x_axis_input"),
                  label = "Invert x-Axis",
                  value = FALSE
                ),
                shiny::checkboxInput(
                  inputId = ns("invert_y_axis_input"),
                  label = "Invert y-Axis",
                  value = FALSE
                )
              )
            )
          ),
          card_footer(
            shiny::fluidRow(
              shiny::column(
                width = 4,
                shiny::actionButton(
                  inputId = ns("apply_filters_button"),
                  label = "Apply",
                  width = "100%"
                ),
                offset = 8
              )
            )
          )
        )
      ),
      shiny::column(
        width = 9,
        card(
          id = ns("results_card"),
          card_header(
            "Results"
          ),
          card_body(
            shiny::textOutput(ns("no_results_label")),
            withSpinner(
              girafeOutput(ns("comparison_scatter_plot")),
              color = "#00a82f",
              type = 7
            )
          )
        )
      )
    )
  )
}
