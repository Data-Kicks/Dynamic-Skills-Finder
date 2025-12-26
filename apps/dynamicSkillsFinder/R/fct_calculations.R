#' @title Filter Dynamic Events
#' @description Filters dynamic event data based on various criteria.
#'
#' @param data The dynamic event data to be filtered.
#' @param insight_type Type of insight ("Attacking (OBR)" or other).
#' @param subevents Vector of subevent types to filter by.
#' @param seasons Vector of season names to filter by.
#' @param competitions Vector of competition names to filter by.
#' @param teams Vector of team shortnames to filter by.
#' @param home_away Vector indicating home or away teams to filter by.
#' @param match_longnames Vector of match longnames to filter by.
#' @param periods Vector of period names to filter by.
#' @param minute_range Numeric vector of length 2 indicating the minute range to filter by.
#' @param gamestates Vector of game states to filter by.
#' @param gamephases Vector of game phases to filter by.
#' @param possession_players Vector of player names in possession to filter by.
#' @param possession_positions Vector of player positions in possession to filter by.
#' @param possession_zones Vector of zones for player in possession to filter by.
#' @param event_players Vector of event player names to filter by.
#' @param event_positions Vector of event player positions to filter by.
#' @param event_zones Vector of event zones to filter by.
#' @param event_from_to Logical indicating whether to filter by start zone (TRUE) or end zone (FALSE).
#'
#' @return Filtered dynamic event data.
#'
#' @importFrom dplyr filter
#'
#' @export
filter_dynamic_events <- function(
  data,
  insight_type,
  subevents = NULL,
  seasons = NULL,
  competitions = NULL,
  teams = NULL,
  home_away = NULL,
  match_longnames = NULL,
  periods = NULL,
  minute_range = NULL,
  gamestates = NULL,
  gamephases = NULL,
  possession_players = NULL,
  possession_positions = NULL,
  possession_zones = NULL,
  event_players = NULL,
  event_positions = NULL,
  event_zones = NULL,
  event_from_to = TRUE
) {
  if (insight_type == "Attacking (OBR)") {
    filtered_data <- data |>
      filter(
        event_type == "off_ball_run"
      )
  } else {
    filtered_data <- data |>
      filter(
        event_type == "on_ball_engagement"
      )
  }
  if (!is.null(subevents)) {
    filtered_data <- filtered_data |>
      filter(
        event_subtype %in% subevents
      )
  }
  if (!is.null(seasons)) {
    filtered_data <- filtered_data |>
      filter(
        season_name == seasons
      )
  }
  if (!is.null(competitions)) {
    filtered_data <- filtered_data |>
      filter(
        competition_name == competitions
      )
  }
  if (!is.null(teams)) {
    filtered_data <- filtered_data |>
      filter(
        team_shortname == teams
      )
  }
  if (!is.null(home_away)) {
    filtered_data <- filtered_data |>
      filter(
        group %in% home_away
      )
  }
  if (!is.null(match_longnames)) {
    filtered_data <- filtered_data |>
      filter(
        match_longname %in% match_longnames
      )
  }
  if (!is.null(periods)) {
    filtered_data <- filtered_data |>
      filter(
        period_name %in% periods
      )
  }
  if (!is.null(minute_range)) {
    filtered_data <- filtered_data |>
      filter(
        minute_start >= minute_range[1],
        minute_end <= minute_range[2]
      )
  }
  if (!is.null(gamestates)) {
    filtered_data <- filtered_data |>
      filter(
        game_state %in% gamestates
      )
  }
  if (!is.null(gamephases)) {
    if (insight_type == "Attacking (OBR)") {
      filtered_data <- filtered_data |>
        filter(
          team_in_possession_phase_type %in% gamephases
        )
    } else {
      filtered_data <- filtered_data |>
        filter(
          team_out_of_possession_phase_type %in% gamephases
        )
    }
  }
  if (!is.null(possession_players)) {
    filtered_data <- filtered_data |>
      filter(
        player_in_possession_name %in% possession_players
      )
  }
  if (!is.null(possession_positions)) {
    filtered_data <- filtered_data |>
      filter(
        player_in_possession_position %in% possession_positions
      )
  }
  if (!is.null(possession_zones)) {
    filtered_data <- filtered_data |>
      filter(
        player_in_possession_zone_start %in%
          possession_zones |
          player_in_possession_zone_end %in% possession_zones
      )
  }
  if (!is.null(event_players)) {
    filtered_data <- filtered_data |>
      filter(
        player_name %in% event_players
      )
  }
  if (!is.null(event_positions)) {
    filtered_data <- filtered_data |>
      filter(
        player_position %in% event_positions
      )
  }
  if (!is.null(event_zones)) {
    if (event_from_to) {
      filtered_data <- filtered_data |>
        filter(
          zone_start %in% event_zones
        )
      return(filtered_data)
    } else {
      filtered_data <- filtered_data |>
        filter(
          zone_end %in% event_zones
        )
    }
  }

  return(filtered_data)
}


#' @title Filter Player Aggregates
#' @description Filters player aggregate data based on various criteria.
#' @param data The player aggregate data to be filtered.
#' @param seasons Vector of season names to filter by.
#' @param competitions Vector of competition names to filter by.
#' @param teams Vector of team shortnames to filter by.
#' @param player_names String of player names to filter by (partial match).
#' @param position_list Vector of player positions to filter by.
#' @param age_range Numeric vector of length 2 indicating the age range to filter by.
#' @param matches_played_range Numeric vector of length 2 indicating the matches played range to filter by.
#' @param matches_started_range Numeric vector of length 2 indicating the matches started range to filter by.
#' @param minutes_played_range Numeric vector of length 2 indicating the minutes played range to filter by.
#' @param custom_filter_metrics Vector of custom metric names to filter by.
#' @param custom_filter_values Numeric vector of custom filter values (min and max for each metric).
#'
#' @return Filtered player aggregate data.
#'
#' @importFrom dplyr collect filter mutate select
#' @importFrom stringr str_split
#' @importFrom arrow as_arrow_table
#' @importFrom stringi stri_trans_general
#' @export
filter_aggregates <- function(
  data,
  seasons = NULL,
  competitions = NULL,
  teams = NULL,
  player_names = NULL,
  position_list = NULL,
  age_range = NULL,
  matches_played_range = NULL,
  matches_started_range = NULL,
  minutes_played_range = NULL,
  custom_filter_metrics = c(),
  custom_filter_values = c()
) {
  filtered_data <- data

  if (!is.null(seasons)) {
    filtered_data <- filtered_data |>
      filter(
        season_name %in% seasons
      )
  }
  if (!is.null(competitions)) {
    filtered_data <- filtered_data |>
      filter(
        competition_name %in% competitions
      )
  }
  if (!is.null(teams)) {
    filtered_data <- filtered_data |>
      filter(
        team_shortname %in% teams
      )
  }
  if (!is.null(player_names)) {
    if (player_names != "") {
      filtered_data <- filtered_data |>
        collect() |>
        filter(
          grepl(
            stri_trans_general(tolower(player_names), "Latin-ASCII"),
            stri_trans_general(tolower(player_name), "Latin-ASCII")
          )
        ) |>
        as_arrow_table()
    }
  }
  if (!is.null(position_list)) {
    data_aux <- filtered_data |>
      collect() |>
      mutate(pos_list = str_split(positions, ", "))

    if (nrow(data_aux) > 0) {
      data_aux <- data_aux |>
        filter(sapply(pos_list, function(x) {
          any(grepl(
            paste0("\\b(", paste0(x, collapse = "|"), ")\\b"),
            position_list
          ))
        }))
    }
    filtered_data <- data_aux |>
      select(-pos_list) |>
      as_arrow_table()
  }
  if (!is.null(age_range)) {
    filtered_data <- filtered_data |>
      filter(
        age >= age_range[1],
        age <= age_range[2]
      )
  }
  if (!is.null(matches_played_range)) {
    filtered_data <- filtered_data |>
      filter(
        matches_played >= matches_played_range[1],
        matches_played <= matches_played_range[2]
      )
  }
  if (!is.null(matches_started_range)) {
    filtered_data <- filtered_data |>
      filter(
        starts >= matches_started_range[1],
        starts <= matches_started_range[2]
      )
  }
  if (!is.null(minutes_played_range)) {
    filtered_data <- filtered_data |>
      filter(
        minutes_played >= minutes_played_range[1],
        minutes_played <= minutes_played_range[2]
      )
  }
  if (length(custom_filter_metrics) > 0 & length(custom_filter_values) > 0) {
    data_aux <- filtered_data |>
      collect()

    value_cont <- 1
    for (i in 1:length(custom_filter_metrics)) {
      data_aux <- data_aux[
        data_aux[[custom_filter_metrics[i]]] >=
          custom_filter_values[value_cont] &
          data_aux[[custom_filter_metrics[i]]] <=
            custom_filter_values[value_cont + 1],
      ]
      value_cont <- value_cont + 2
    }

    filtered_data <- data_aux |>
      as_arrow_table()
  }

  return(filtered_data)
}

#' @export
calculate_percentiles <- function(data) {
  for (variable in names(data)) {
    if (is.numeric(data[[variable]])) {
      data <- data[order(data[[variable]]), ]
      data[[paste(variable, "_prct", sep = "")]] <-
        (rank(data[[variable]], na.last = "keep", ties.method = "max") - 1) /
        sum(!is.na(data[[variable]])) *
        100
    }
  }

  return(data)
}
