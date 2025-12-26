#' @title Tactical Find UI
#' @description Shiny module for Tactical Find user interface.
#'
#' @param id Module ID.
#'
#' @return Shiny UI elements for Tactical Find.
#'
#' @import shiny
#' @importFrom bslib card card_header card_body card_footer
#' @importFrom dplyr filter first pull
#' @importFrom shinyWidgets pickerInput pickerOptions prettyToggle
#' @importFrom ggiraph girafeOutput
#' @importFrom shinycssloaders withSpinner
#'
#' @export
mod_tactical_find_ui <- function(id) {
  ns <- shiny::NS(id)

  seasons <- dynamic_events_data |>
    pull(season_name) |>
    unique() |>
    sort(decreasing = FALSE)

  competitions <- dynamic_events_data |>
    filter(season_name == first(seasons)) |>
    pull(competition_name) |>
    unique() |>
    sort()

  teams <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions)
    ) |>
    pull(team_shortname) |>
    unique() |>
    sort()

  matches <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions),
      team_shortname == first(teams)
    ) |>
    pull(match_longname) |>
    unique() |>
    sort()

  periods <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions),
      team_shortname == first(teams),
      match_longname %in% matches
    ) |>
    pull(period_name) |>
    unique() |>
    sort()

  max_minute <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions),
      team_shortname == first(teams),
      match_longname %in% matches
    ) |>
    pull(minute_start) |>
    max(na.rm = TRUE)

  game_states <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions),
      team_shortname == first(teams),
      match_longname %in% matches,
      event_type == "off_ball_run"
    ) |>
    pull(game_state) |>
    unique() |>
    sort()

  game_phases <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions),
      team_shortname == first(teams),
      match_longname %in% matches,
      event_type == "off_ball_run"
    ) |>
    pull(team_in_possession_phase_type) |>
    unique() |>
    sort()

  positions <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions),
      team_shortname == first(teams),
      match_longname %in% matches,
      event_type == "off_ball_run"
    ) |>
    pull(player_position) |>
    unique() |>
    sort()

  players <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions),
      team_shortname == first(teams),
      match_longname %in% matches,
      event_type == "off_ball_run"
    ) |>
    pull(player_name) |>
    unique() |>
    sort()

  event_subtypes <- dynamic_events_data |>
    filter(
      season_name == first(seasons),
      competition_name == first(competitions),
      team_shortname == first(teams),
      match_longname %in% matches,
      event_type == "off_ball_run"
    ) |>
    pull(event_subtype) |>
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
            "Filters"
          ),
          card_body(
            shiny::fluidRow(
              shiny::column(
                width = 6,
                shiny::radioButtons(
                  inputId = ns("insights_type"),
                  label = "Insights Type",
                  choices = c("Attacking (OBR)", "Defending (OBE)"),
                  selected = "Attacking (OBR)",
                  inline = TRUE
                )
              ),
              shiny::column(
                width = 6,
                pickerInput(
                  inputId = ns("event_subtype_select"),
                  label = "Event subtype",
                  choices = event_subtypes,
                  selected = event_subtypes,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No option selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} options selected"
                  ),
                  multiple = TRUE
                )
              )
            ),
            shiny::hr(),
            shiny::br(),
            shiny::fluidRow(
              shiny::column(
                width = 4,
                pickerInput(
                  inputId = ns("season_select"),
                  label = "Season",
                  choices = seasons,
                  selected = first(seasons)
                )
              ),
              shiny::column(
                width = 4,
                pickerInput(
                  inputId = ns("competition_select"),
                  label = "Competition",
                  choices = competitions,
                  selected = first(competitions)
                )
              ),
              shiny::column(
                width = 4,
                pickerInput(
                  inputId = ns("team_select"),
                  label = "Team",
                  choices = teams,
                  selected = first(teams),
                  options = pickerOptions(
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search..."
                  )
                )
              )
            ),
            shiny::hr(),
            shiny::br(),
            shiny::fluidRow(
              shiny::column(
                width = 6,
                pickerInput(
                  inputId = ns("home_away_select"),
                  label = "Home/Away",
                  choices = c("home", "away"),
                  selected = c("home", "away"),
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No option selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} options selected"
                  ),
                  multiple = TRUE
                )
              ),
              shiny::column(
                width = 6,
                pickerInput(
                  inputId = ns("match_select"),
                  label = "Matches",
                  choices = matches,
                  selected = matches,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search...",
                    noneSelectedText = "No match selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} matches selected"
                  ),
                  multiple = TRUE
                )
              )
            ),
            shiny::hr(),
            shiny::br(),
            shiny::fluidRow(
              shiny::column(
                width = 6,
                pickerInput(
                  inputId = ns("period_select"),
                  label = "Periods",
                  choices = periods,
                  selected = periods,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No period selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} periods selected"
                  ),
                  multiple = TRUE
                )
              ),
              shiny::column(
                width = 6,
                shiny::sliderInput(
                  inputId = ns("minute_select"),
                  label = "Minutes",
                  min = 0,
                  max = max_minute,
                  value = c(0, max_minute),
                  step = 1
                )
              )
            ),
            shiny::hr(),
            shiny::br(),
            shiny::fluidRow(
              shiny::column(
                width = 6,
                pickerInput(
                  inputId = ns("game_state_select"),
                  label = "Game State",
                  choices = game_states,
                  selected = game_states,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No option selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} option selected"
                  ),
                  multiple = TRUE
                )
              ),
              shiny::column(
                width = 6,
                pickerInput(
                  inputId = ns("game_phase_select"),
                  label = "Game Phase",
                  choices = game_phases,
                  selected = game_phases,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No option selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} option selected"
                  ),
                  multiple = TRUE
                )
              )
            ),
            shiny::hr(),
            shiny::br(),
            shiny::fluidRow(
              shiny::column(
                width = 6,
                pickerInput(
                  inputId = ns("possession_player_select"),
                  label = "Player in possession name",
                  choices = players,
                  selected = players,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No player selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} players selected",
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search..."
                  ),
                  multiple = TRUE
                ),
                pickerInput(
                  inputId = ns("possession_player_position_select"),
                  label = "Player in possession position",
                  choices = positions,
                  selected = positions,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 3",
                    noneSelectedText = "No position selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} positions selected"
                  ),
                  multiple = TRUE
                )
              ),
              shiny::column(
                width = 6,
                shiny::tags$label(
                  "Player in possession zones",
                  class = "control-label"
                ),
                withSpinner(
                  girafeOutput(
                    ns("possession_pitch"),
                    width = "100%"
                  ),
                  color = "#00a82f",
                  type = 7,
                  proxy.height = "175px"
                )
              )
            ),
            shiny::hr(),
            shiny::br(),
            shiny::fluidRow(
              shiny::column(
                width = 6,
                pickerInput(
                  inputId = ns("event_player_select"),
                  label = "Event player name",
                  choices = players,
                  selected = players,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 1",
                    noneSelectedText = "No player selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} players selected",
                    liveSearch = TRUE,
                    liveSearchNormalize = TRUE,
                    liveSearchPlaceholder = "Search..."
                  ),
                  multiple = TRUE
                ),
                pickerInput(
                  inputId = ns("Event_player_position_select"),
                  label = "Event player position",
                  choices = positions,
                  selected = positions,
                  options = pickerOptions(
                    actionsBox = TRUE,
                    selectedTextFormat = "count > 3",
                    noneSelectedText = "No position selected",
                    selectAllText = "All",
                    deselectAllText = "None",
                    countSelectedText = "{0} positions selected"
                  ),
                  multiple = TRUE
                )
              ),
              shiny::column(
                width = 6,
                shiny::tags$label(
                  "Event player zones",
                  class = "control-label"
                ),
                withSpinner(
                  girafeOutput(
                    ns("event_pitch"),
                    width = "100%"
                  ),
                  color = "#00a82f",
                  type = 7,
                  proxy.height = "175px"
                ),
                shiny::div(
                  id = ns("event_player_from_to_switch_div"),
                  prettyToggle(
                    inputId = ns("event_player_from_to_switch"),
                    value = TRUE,
                    label_on = "From",
                    label_off = "To"
                  )
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
          )
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
            shiny::fluidRow(
              shiny::column(
                width = 6,
                shiny::uiOutput(ns("filtered_dynamic_events_plot_ui")),
                shiny::uiOutput(ns("show_heatmap_ui"))
              ),
              shiny::column(
                width = 6,
                shiny::uiOutput(ns("filtered_dynamic_events_table_ui")),
                shiny::uiOutput(ns("download_filtered_dynamic_events_ui"))
              )
            )
          )
        )
      )
    )
  )
}
