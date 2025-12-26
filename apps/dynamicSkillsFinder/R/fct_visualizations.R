# Pitch rectangles coords
pitch_rects <- data.frame(
  zone = c(
    "pitch_perimeter",
    "defending_box",
    "attacking_box",
    "defending_goal_area",
    "attacking_goal_area",
    "defending_goal",
    "attacking_goal"
  ),
  xmin = c(-52.5, -52.5, 36, -52.5, 47, -54.94, 52.5),
  ymin = c(-34, -20.16, -20.16, -9.16, -9.16, -3.66, -3.66),
  xmax = c(52.5, -36, 52.5, -47, 52.5, -52.5, 54.94),
  ymax = c(34, 20.16, 20.16, 9.16, 9.16, 3.66, 3.66)
)

# Pitch points coords
pitch_points <- data.frame(
  zone = c("left_penalty", "center", "right_penalty"),
  x = c(-41.5, 0, 41.5),
  y = c(0, 0, 0)
)

# Pitch centre circle coords
pitch_centre_circle <- data.frame(
  x0 = 0,
  y0 = 0,
  r = 9.15
)

# Pitch halfway-line coords
halfway_line <- data.frame(
  x = 0,
  y = -34,
  xend = 0,
  yend = 34
)

# Pitch curves coords
pitch_curves <- data.frame(
  curve = c(
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
    "defending_d",
    "atacking_d"
  ),
  x = c(-52.5, 51.5, -51.5, 52.5, -36, 36),
  y = c(33, 34, -34, -33, -7.3, 7.3),
  xend = c(-51.5, 52.5, -52.5, 51.5, -36, 36),
  yend = c(34, 33, -33, -34, 7.3, -7.3)
)

# Pitch zone rects coords
zones_rects <- data.frame(
  zone = c(
    "LW1",
    "LW2",
    "LW3",
    "LW4",
    "LW5",
    "LW6",
    "LHS1",
    "LHS2",
    "LHS3",
    "LHS4",
    "LHS5",
    "LHS6",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "C6",
    "RHS1",
    "RHS2",
    "RHS3",
    "RHS4",
    "RHS5",
    "RHS6",
    "RW1",
    "RW2",
    "RW3",
    "RW4",
    "RW5",
    "RW6"
  ),
  xmax = c(
    -36,
    -17.5,
    0,
    17.5,
    36,
    52.5,
    -36,
    -17.5,
    0,
    17.5,
    36,
    52.5,
    -36,
    -17.5,
    0,
    17.5,
    36,
    52.5,
    -36,
    -17.5,
    0,
    17.5,
    36,
    52.5,
    -36,
    -17.5,
    0,
    17.5,
    36,
    52.5
  ),
  xmin = c(
    -52.5,
    -36,
    -17.5,
    0,
    17.5,
    36,
    -52.5,
    -36,
    -17.5,
    0,
    17.5,
    36,
    -52.5,
    -36,
    -17.5,
    0,
    17.5,
    36,
    -52.5,
    -36,
    -17.5,
    0,
    17.5,
    36,
    -52.5,
    -36,
    -17.5,
    0,
    17.5,
    36
  ),
  ymax = c(
    34,
    34,
    34,
    34,
    34,
    34,
    20.16,
    20.16,
    20.16,
    20.16,
    20.16,
    20.16,
    9.16,
    9.16,
    9.16,
    9.16,
    9.16,
    9.16,
    -9.16,
    -9.16,
    -9.16,
    -9.16,
    -9.16,
    -9.16,
    -20.16,
    -20.16,
    -20.16,
    -20.16,
    -20.16,
    -20.16
  ),
  ymin = c(
    20.16,
    20.16,
    20.16,
    20.16,
    20.16,
    20.16,
    9.16,
    9.16,
    9.16,
    9.16,
    9.16,
    9.16,
    -9.16,
    -9.16,
    -9.16,
    -9.16,
    -9.16,
    -9.16,
    -20.16,
    -20.16,
    -20.16,
    -20.16,
    -20.16,
    -20.16,
    -34,
    -34,
    -34,
    -34,
    -34,
    -34
  ),
  center_x = c(
    -44.25,
    -26.75,
    -8.75,
    8.75,
    26.75,
    44.25,
    -44.25,
    -26.75,
    -8.75,
    8.75,
    26.75,
    44.25,
    -44.25,
    -26.75,
    -8.75,
    8.75,
    26.75,
    44.25,
    -44.25,
    -26.75,
    -8.75,
    8.75,
    26.75,
    44.25,
    -44.25,
    -26.75,
    -8.75,
    8.75,
    26.75,
    44.25
  ),
  center_y = c(
    27.08,
    27.08,
    27.08,
    27.08,
    27.08,
    27.08,
    14.66,
    14.66,
    14.66,
    14.66,
    14.66,
    14.66,
    0,
    0,
    0,
    0,
    0,
    0,
    -14.66,
    -14.66,
    -14.66,
    -14.66,
    -14.66,
    -14.66,
    -27.08,
    -27.08,
    -27.08,
    -27.08,
    -27.08,
    -27.08
  )
)


#' @title Draw football pitch
#' @description This function creates a football pitch visualization using ggplot2.
#'
#' @param ggobject A ggplot2 object to add the pitch to. Default is a new ggplot2 object.
#' @param lines_color Color of the pitch lines. Default is "black".
#' @param pitch_color Color of the pitch background. Default is NA (transparent).
#' @param lines_width Width of the pitch lines. Default is 0.5.
#' @param zones Logical value indicating whether to draw pitch zones. Default is FALSE.
#' @param zones_lines_color Color of the zone lines. Default is "#99999950".
#' @param arrow Logical value indicating whether to draw an arrow indicating direction of play. Default is TRUE.
#' @param half_only Logical value indicating whether to draw only half of the pitch. Default is FALSE.
#' @param flip Logical value indicating whether to flip the pitch orientation. Default is FALSE.
#'
#' @return A ggplot2 object representing the football pitch.
#'
#' @import ggplot2
#' @importFrom ggforce geom_circle
#' @importFrom ggiraph geom_rect_interactive
#'
#' @export
draw_football_pitch <- function(
  ggobject = ggplot2::ggplot(),
  lines_color = "black",
  pitch_color = NA,
  lines_width = 0.5,
  zones = F,
  zones_lines_color = "#99999950",
  arrow = T,
  half_only = F,
  flip = F
) {
  pitch <- ggobject +
    # Pitch rectangles
    ggplot2::geom_rect(
      data = pitch_rects[-c(6, 7), ],
      mapping = ggplot2::aes(
        xmin = xmin,
        ymin = ymin,
        xmax = xmax,
        ymax = ymax
      ),
      color = lines_color,
      fill = pitch_color,
      linewidth = lines_width
    ) +
    # Goals
    ggplot2::geom_rect(
      data = pitch_rects[c(6, 7), ],
      mapping = ggplot2::aes(
        xmin = xmin,
        ymin = ymin,
        xmax = xmax,
        ymax = ymax
      ),
      color = lines_color,
      fill = NA,
      linewidth = lines_width
    ) +
    # Centre circle
    ggforce::geom_circle(
      data = pitch_centre_circle,
      mapping = ggplot2::aes(
        x0 = x0,
        y0 = y0,
        r = r
      ),
      color = lines_color,
      fill = pitch_color,
      linewidth = lines_width
    ) +
    # Halfway line
    ggplot2::geom_segment(
      data = halfway_line,
      mapping = ggplot2::aes(
        x = x,
        y = y,
        xend = xend,
        yend = yend
      ),
      color = lines_color,
      linewidth = lines_width
    ) +
    # Center and penalty spots
    ggplot2::geom_point(
      data = pitch_points,
      mapping = ggplot2::aes(
        x = x,
        y = y
      ),
      color = lines_color,
      fill = lines_color,
      size = lines_width
    ) +
    # Corner and D arcs
    ggplot2::geom_curve(
      data = pitch_curves,
      mapping = ggplot2::aes(
        x = x,
        y = y,
        xend = xend,
        yend = yend
      ),
      color = lines_color,
      linewidth = lines_width
    ) +
    ggplot2::theme_void() +
    ggplot2::theme(
      text = ggplot2::element_text(
        family = "Lexend"
      ),
      plot.background = ggplot2::element_rect(
        color = pitch_color,
        fill = pitch_color
      )
    )

  if (zones) {
    pitch <- pitch +
      geom_rect_interactive(
        data = zones_rects,
        mapping = ggplot2::aes(
          xmin = xmin,
          ymin = ymin,
          xmax = xmax,
          ymax = ymax,
          data_id = zone
        ),
        color = zones_lines_color,
        fill = NA
      )
  }

  if (arrow & !half_only) {
    pitch <- pitch +
      ggplot2::geom_segment(
        ggplot2::aes(x = -10, y = -35.9, xend = 10, yend = -35.9),
        colour = lines_color,
        linewidth = lines_width,
        arrow = ggplot2::arrow(
          length = ggplot2::unit(lines_width / 2, "cm"),
          type = "closed"
        )
      )
  }

  if (half_only) {
    pitch <- pitch +
      ggplot2::xlim(-0.1, 57.5) +
      ggplot2::ylim(-40, 39)
  }

  if (flip) {
    pitch <- pitch +
      ggplot2::coord_flip()
  } else {
    pitch <- pitch +
      ggplot2::xlim(-58.5, 57.5) +
      ggplot2::ylim(-40, 39) +
      ggplot2::coord_fixed()
  }

  return(pitch)
}


#' @title Draw dynamic events arrows on football pitch
#' @description This function adds dynamic event arrows to a football pitch visualization using ggplot2.
#'
#' @param ggobject A ggplot2 object representing the football pitch. Default is a new ggplot2 object.
#' @param data A data frame containing dynamic event data.
#' @param tracking_plot Logical value indicating whether to use tracking data for the plot. Default is FALSE.
#'
#' @return A ggplot2 object representing the football pitch with dynamic event arrows.
#'
#' @import ggplot2
#' @importFrom ggiraph geom_segment_interactive
#' @importFrom ggtext element_markdown
#' @importFrom ggnewscale new_scale_color
#'
#' @export
draw_dynamic_events_arrows <- function(
  ggobject = ggplot2::ggplot(),
  data,
  tracking_plot = FALSE
) {
  insights_type <- first(req(data$event_type))

  if (nrow(data) > 1) {
    data$id <- rownames(data)
  } else {
    data$id <- ""
  }

  if (insights_type == "off_ball_run") {
    data$tooltip <- paste0(
      ifelse(nrow(data) > 1, "ID: ", ""),
      data$id,
      ifelse(nrow(data) > 1, "\n", ""),
      "Match: ",
      data$match_name,
      "\n",
      "Player: ",
      data$player_name,
      "\n",
      "Number: ",
      data$player_number,
      "\n",
      "Position: ",
      data$player_position,
      "\n",
      "Event subtype: ",
      data$event_subtype,
      "\n",
      "Game state: ",
      data$game_state,
      "\n",
      "Phase type: ",
      data$team_in_possession_phase_type,
      "\n",
      "Received: ",
      data$received,
      "\n",
      "xThreat: ",
      round(data$xthreat, 2),
      "\n",
      "xPass Completion: ",
      round(data$xpass_completion, 2),
      "\n",
      "Passing option score: ",
      round(data$passing_option_score, 2)
    )

    if (tracking_plot) {
      plot <- ggobject +
        new_scale_color() +
        geom_segment_interactive(
          data = data,
          mapping = ggplot2::aes(
            x = x_start_tracking,
            y = y_start_tracking,
            xend = x_end_tracking,
            yend = y_end_tracking,
            color = targeted,
            tooltip = tooltip,
            data_id = id
          ),
          linewidth = 0.7,
          arrow = ggplot2::arrow(
            length = ggplot2::unit(0.08, "inches"),
            type = "closed"
          )
        ) +
        ggplot2::labs(
          title = "Selected off-ball run start frame"
        )
    } else {
      plot <- ggobject +
        geom_segment_interactive(
          data = data,
          mapping = ggplot2::aes(
            x = x_start,
            y = y_start,
            xend = x_end,
            yend = y_end,
            color = targeted,
            tooltip = tooltip,
            data_id = id
          ),
          linewidth = 0.7,
          arrow = ggplot2::arrow(
            length = ggplot2::unit(0.08, "inches"),
            type = "closed"
          )
        ) +
        ggplot2::labs(
          title = "Off-ball <span style = 'color: #138d35ff;'>targeted</span> and <span style = 'color: #f99c31ff;'>non-targeted</span> runs"
        )
    }

    plot <- plot +
      ggplot2::scale_color_manual(
        values = c(
          "TRUE" = "#138d35ff",
          "FALSE" = "#f99c31ff"
        )
      )
  } else {
    data$tooltip <- paste0(
      ifelse(nrow(data) > 1, "ID: ", ""),
      data$id,
      ifelse(nrow(data) > 1, "\n", ""),
      "Match: ",
      data$match_name,
      "\n",
      "Player: ",
      data$player_name,
      "\n",
      "Number: ",
      data$player_number,
      "\n",
      "Position: ",
      data$player_position,
      "\n",
      "Event subtype: ",
      data$event_subtype,
      "\n",
      "Game state: ",
      data$game_state,
      "\n",
      "Phase type: ",
      data$team_out_of_possession_phase_type
    )

    if (tracking_plot) {
      plot <- ggobject +
        geom_segment_interactive(
          data = data,
          mapping = ggplot2::aes(
            x = x_start_tracking,
            y = y_start_tracking,
            xend = x_end_tracking,
            yend = y_end_tracking,
            tooltip = tooltip,
            data_id = id
          ),
          color = "#138d35ff",
          linewidth = 0.7,
          arrow = ggplot2::arrow(
            length = ggplot2::unit(0.08, "inches"),
            type = "closed"
          )
        ) +
        ggplot2::labs(
          title = "Selected on-ball engagement event start frame"
        )
    } else {
      plot <- ggobject +
        geom_segment_interactive(
          data = data,
          mapping = ggplot2::aes(
            x = x_start,
            y = y_start,
            xend = x_end,
            yend = y_end,
            tooltip = tooltip,
            data_id = id
          ),
          color = "#138d35ff",
          linewidth = 0.7,
          arrow = ggplot2::arrow(
            length = ggplot2::unit(0.08, "inches"),
            type = "closed"
          )
        ) +
        ggplot2::labs(
          title = "On-Ball Engagement events"
        )
    }
  }

  plot <- plot +
    ggplot2::theme_void() +
    ggplot2::theme(
      text = ggplot2::element_text(
        family = "Lexend"
      ),
      plot.title = element_markdown(
        hjust = 0.5,
        size = 16,
        margin = ggplot2::margin(0, 0, -10, 0)
      )
    ) +
    ggplot2::guides(
      color = "none"
    )

  return(plot)
}


#' @title Draw tracking data for players and ball on football pitch
#' @description This function adds tracking data for players and the ball to a football pitch visualization using ggplot2.
#'
#' @param ggobject A ggplot2 object representing the football pitch. Default is a new ggplot2 object.
#' @param data A data frame containing tracking data for players and the ball.
#'
#' @return A ggplot2 object representing the football pitch with tracking data for players and the ball.
#'
#' @import ggplot2
#' @importFrom ggiraph geom_point_interactive
#' @importFrom dplyr first mutate pull
#' @importFrom scales label_wrap
#' @importFrom ggnewscale new_scale_color new_scale_fill
#'
#' @export
draw_tracking_data_players_and_ball <- function(
  ggobject = ggplot2::ggplot(),
  data
) {
  if (nrow(data) > 1) {
    data$id <- rownames(data)
  } else {
    data$id <- ""
  }

  data <- data |>
    mutate(
      tooltip = ifelse(
        group != "ball",
        paste0(
          "Team: ",
          data$team_shortname,
          "\n",
          "Player: ",
          data$player_name,
          "\n",
          "Number: ",
          data$player_number,
          "\n",
          "Position: ",
          data$position_acronym,
          "\n",
          "Has possession: ",
          data$has_possession
        ),
        "Ball"
      )
    )

  plot <- ggobject +
    new_scale_color() +
    new_scale_fill() +
    geom_point_interactive(
      data = data,
      mapping = ggplot2::aes(
        x = x,
        y = y,
        fill = group,
        size = group,
        color = group,
        tooltip = tooltip,
        data_id = id
      ),
      pch = 21,
      stroke = 0.7
    ) +
    ggplot2::scale_color_manual(
      values = c(
        "home team" = "#000000",
        "away team" = "#000000",
        "ball" = "#d83006ff"
      ),
      breaks = c(
        "home team",
        "away team",
        "ball"
      ),
      labels = c(
        "home team" = "Home Team",
        "away team" = "Away Team",
        "ball" = "Ball"
      )
    ) +
    ggplot2::scale_fill_manual(
      values = c(
        "home team" = data[
          data$group == "home team" &
            !is.null(data$team_jersey_color) &
            data$team_jersey_color != "",
        ] |>
          pull(team_jersey_color) |>
          first(),
        "away team" = data[
          data$group == "away team" &
            !is.null(data$team_jersey_color) &
            data$team_jersey_color != "",
        ] |>
          pull(team_jersey_color) |>
          first(),
        "ball" = "#ffffffff"
      ),
      breaks = c(
        "home team",
        "away team",
        "ball"
      ),
      labels = c(
        "home team" = "Home Team",
        "away team" = "Away Team",
        "ball" = "Ball"
      )
    ) +
    ggplot2::scale_size_manual(
      values = c(
        "home team" = 4,
        "away team" = 4,
        "ball" = 3
      )
    ) +
    ggplot2::theme(
      text = ggplot2::element_text(
        family = "Lexend"
      ),
      legend.text = ggplot2::element_text(
        size = 12,
      ),
      legend.position = "bottom",
      legend.margin = ggplot2::margin(t = -30)
    ) +
    ggplot2::guides(
      size = "none",
      color = ggplot2::guide_legend(override.aes = list(size = 3), title = ""),
      fill = ggplot2::guide_legend(override.aes = list(size = 3), title = "")
    )

  return(plot)
}


#' @title Draw dynamic events heatmap on football pitch
#' @description This function adds a heatmap of dynamic events to a football pitch visualization using ggplot2.
#'
#' @param ggobject A ggplot2 object representing the football pitch. Default is a new ggplot2 object.
#' @param data A data frame containing dynamic event data aggregated by pitch zones.
#' @param events_type The type of events to visualize, either "Attacking (OBR)" or other types.
#'
#' @return A ggplot2 object representing the football pitch with a dynamic events heatmap.
#'
#' @import ggplot2
#' @importFrom ggiraph geom_rect_interactive
#' @importFrom dplyr collect left_join
#' @importFrom ggtext element_markdown
#' @importFrom ggnewscale new_scale_fill
#'
#' @export
draw_dynamic_events_heatmap <- function(
  ggobject = ggplot2::ggplot(),
  data,
  events_type
) {
  data <- data |>
    left_join(zones_rects, by = "zone") |>
    collect()

  if (events_type == "Attacking (OBR)") {
    plot_title <- "<span style = 'color: #138d35ff;'>Total</span> of off-ball runs"

    data$tooltip <- paste0(
      paste0(
        "Total: ",
        data$total,
        "\n",
        "Targeted: ",
        data$targeted,
        "\n",
        "Received: ",
        data$received
      )
    )
  } else {
    plot_title <- "<span style = 'color: #138d35ff;'>Total</span> of on-ball engagement events"

    data$tooltip <- paste0(
      paste0(
        "Total: ",
        data$total
      )
    )
  }

  plot <- ggobject +
    new_scale_fill() +
    geom_rect_interactive(
      data = data,
      mapping = ggplot2::aes(
        xmin = xmin,
        xmax = xmax,
        ymin = ymin,
        ymax = ymax,
        fill = total,
        tooltip = tooltip
      ),
      alpha = 0.7
    ) +
    ggplot2::scale_fill_gradient(
      low = "#e2fedba6",
      high = "#187432"
    ) +
    ggplot2::labs(
      title = plot_title
    ) +
    ggplot2::theme_void() +
    ggplot2::theme(
      text = ggplot2::element_text(
        family = "Lexend"
      ),
      plot.title = element_markdown(
        hjust = 0.5,
        size = 16,
        margin = ggplot2::margin(0, 0, -10, 0)
      )
    ) +
    ggplot2::guides(
      fill = "none"
    )

  return(plot)
}


#' @title Draw pizza plot for player aggregated metrics
#' @description This function creates a pizza plot to visualize player aggregated metrics and their percentiles.
#'
#' @param data A data frame containing player aggregated metrics and their percentiles.
#' @param caption_string A string for the plot caption. Default is a generic comparison caption.
#'
#' @return A ggplot2 object representing the pizza plot.
#'
#' @import ggplot2
#' @importFrom ggiraph geom_bar_interactive
#' @importFrom dplyr collect mutate select
#' @importFrom tidyr gather
#' @importFrom scales label_wrap
#'
#' @export
draw_pizza_plot <- function(
  data,
  caption_string = "Compared to players from the same season and competition\nFiltered by values of 'positions' and 'minutes played' from filters panel"
) {
  prct_data <- data |>
    select(ends_with("_prct")) |>
    gather(metric_prct, prct) |>
    collect()

  value_data <- data |>
    select(!ends_with("_prct")) |>
    gather(metric, value) |>
    mutate(metric_type = unlist(player_agg_metric_types[metric])) |>
    mutate(metric = unlist(player_agg_metric_columns[metric])) |>
    collect()

  final_data <- cbind(
    value_data,
    prct = prct_data$prct
  )

  final_data$tooltip <- c(paste0(
    final_data$metric,
    ": ",
    round(final_data$value, 2),
    "\n ",
    "Percentile",
    ": ",
    round(final_data$prct, 0)
  ))

  final_data$data_id <- rownames(final_data)

  plot <- ggplot2::ggplot(
    data = final_data,
  ) +
    ggplot2::geom_bar(
      ggplot2::aes(x = metric, y = 100),
      stat = "identity",
      width = 1,
      colour = "#797979",
      alpha = 0.1,
      show.legend = F
    ) +
    geom_bar_interactive(
      stat = "identity",
      width = 1,
      ggplot2::aes(
        x = metric,
        y = prct,
        fill = metric_type,
        tooltip = tooltip,
        data_id = data_id
      ),
      colour = "black",
      alpha = 0.7
    ) +
    ggplot2::coord_polar(clip = "off") +
    ggplot2::geom_hline(
      yintercept = 25,
      colour = "#565656",
      linetype = "longdash",
      alpha = 0.5
    ) +
    ggplot2::geom_hline(
      yintercept = 50,
      colour = "#565656",
      linetype = "longdash",
      alpha = 0.5
    ) +
    ggplot2::geom_hline(
      yintercept = 75,
      colour = "#565656",
      linetype = "longdash",
      alpha = 0.5
    ) +
    ggplot2::scale_fill_manual(
      values = c(
        "OBE" = "#f99c31ff",
        "OBR" = "#138d35ff",
        "OBEv" = "#40cfe49d"
      ),
      labels = c(
        "OBE" = "On-Ball Engagement Metric",
        "OBR" = "Off-Ball Run Metric",
        "OBEv" = "On-Ball Event Metric"
      )
    ) +
    ggplot2::scale_x_discrete(labels = label_wrap(9)) +
    ggplot2::scale_y_continuous(limits = c(-25, 100)) +
    ggplot2::labs(
      fill = "",
      caption = caption_string
    ) +
    ggplot2::theme_minimal() +
    ggplot2::theme(
      text = ggplot2::element_text(colour = "#131313", family = "Lexend"),
      plot.background = ggplot2::element_rect(fill = NA, color = NA),
      panel.background = ggplot2::element_rect(fill = NA, color = NA),
      legend.position = "bottom",
      legend.text = ggplot2::element_text(size = 16),
      legend.key.spacing.x = ggplot2::unit(1, "cm"),
      axis.title.y = ggplot2::element_blank(),
      axis.title.x = ggplot2::element_blank(),
      axis.text.y = ggplot2::element_blank(),
      axis.text.x = ggplot2::element_text(size = 16),
      plot.caption = ggplot2::element_text(
        hjust = 0.5,
        size = 18,
        margin = ggplot2::margin(t = 40)
      ),
      panel.grid.major = ggplot2::element_blank(),
      panel.grid.minor = ggplot2::element_blank(),
      plot.margin = ggplot2::margin(6, 6, 6, 6)
    )

  return(plot)
}


#' @title Draw scatter plot for player or team aggregated metrics
#'
#' @description This function creates a scatter plot to visualize the relationship between two aggregated metrics for players or teams.
#'
#' @param data A data frame containing player or team aggregated metrics.
#' @param x_metric The metric to be plotted on the x-axis.
#' @param y_metric The metric to be plotted on the y-axis.
#' @param size_metric The metric to determine the size of the points. Default is "None".
#' @param label_outliers Logical value indicating whether to label outliers. Default is FALSE.
#' @param invert_x_axis Logical value indicating whether to invert the x-axis. Default is FALSE.
#' @param invert_y_axis Logical value indicating whether to invert the y-axis. Default is FALSE.
#' @param type The type of data, either "player" or "team". Default is "player".
#'
#' @return A ggplot2 object representing the scatter plot.
#'
#' @import ggplot2
#' @importFrom ggiraph geom_point_interactive geom_segment_interactive
#' @importFrom ggrepel geom_text_repel
#'
#' @export
draw_scatter_plot <- function(
  data,
  x_metric = NULL,
  y_metric = NULL,
  size_metric = "None",
  label_outliers = FALSE,
  invert_x_axis = FALSE,
  invert_y_axis = FALSE,
  type = "player"
) {
  data$data_id <- rownames(data)

  if (type == "team") {
    x_label <- team_agg_metric_columns[x_metric]
    y_label <- team_agg_metric_columns[y_metric]

    data$tooltip <- paste0(
      "Season: ",
      data$season_name,
      "\n",
      "Competition: ",
      data$competition_name,
      "\n",
      "Team: ",
      data$team_shortname,
      "\n",
      x_label,
      ": ",
      round(data[[x_metric]], 2),
      "\n",
      y_label,
      ": ",
      round(data[[y_metric]], 2)
    )
  } else {
    x_label <- player_agg_metric_columns[x_metric]
    y_label <- player_agg_metric_columns[y_metric]

    data$tooltip <- paste0(
      "Season: ",
      data$season_name,
      "\n",
      "Competition: ",
      data$competition_name,
      "\n",
      "Team: ",
      data$team_shortname,
      "\n",
      "Player: ",
      data$player_name,
      "\n",
      "Position: ",
      data$positions,
      "\n",
      x_label,
      ": ",
      round(data[[x_metric]], 2),
      "\n",
      y_label,
      ": ",
      round(data[[y_metric]], 2)
    )
  }

  plot <- ggplot2::ggplot() +
    geom_segment_interactive(
      data = data,
      ggplot2::aes(
        x = mean(.data[[x_metric]], na.rm = TRUE),
        y = -Inf,
        xend = mean(.data[[x_metric]], na.rm = TRUE),
        yend = Inf
      ),
      linetype = "dashed",
      linewidth = 0.2,
      colour = "gray61",
      alpha = 0.5,
      tooltip = round(mean(data[[x_metric]], na.rm = TRUE), 2),
      data_id = "x_mean"
    ) +
    geom_segment_interactive(
      data = data,
      ggplot2::aes(
        x = -Inf,
        y = mean(.data[[y_metric]], na.rm = TRUE),
        xend = Inf,
        yend = mean(.data[[y_metric]], na.rm = TRUE)
      ),
      linetype = "dashed",
      linewidth = 0.2,
      colour = "gray61",
      alpha = 0.5,
      tooltip = round(mean(data[[y_metric]], na.rm = TRUE), 2),
      data_id = "y_mean"
    )

  if (!is.null(size_metric) & size_metric != "None") {
    size_label <- if (type == "team") {
      team_agg_metric_columns[size_metric]
    } else {
      player_agg_metric_columns[size_metric]
    }

    data$tooltip <- paste0(
      data$tooltip,
      "\n",
      size_label,
      ": ",
      round(data[[size_metric]], 2)
    )

    plot <- plot +
      geom_point_interactive(
        data = data,
        mapping = ggplot2::aes(
          x = .data[[x_metric]],
          y = .data[[y_metric]],
          size = .data[[size_metric]],
          tooltip = tooltip,
          data_id = data_id
        ),
        color = "#187432",
        fill = "#00a82f",
        pch = 21,
        stroke = 0.7,
        alpha = 0.7
      )
  } else {
    plot <- plot +
      geom_point_interactive(
        data = data,
        mapping = ggplot2::aes(
          x = .data[[x_metric]],
          y = .data[[y_metric]],
          tooltip = tooltip,
          data_id = data_id
        ),
        color = "#187432",
        fill = "#00a82f",
        size = 3,
        pch = 21,
        stroke = 0.7,
        alpha = 1
      )
  }

  plot <- plot +
    ggplot2::labs(
      x = x_label,
      y = y_label
    ) +
    ggplot2::theme(
      text = ggplot2::element_text(colour = "#131313", family = "Lexend"),
      plot.background = ggplot2::element_rect(fill = NA, color = NA),
      panel.background = ggplot2::element_rect(fill = NA, color = NA),
      axis.line = ggplot2::element_line(color = "black"),
      axis.title.y = ggplot2::element_text(
        size = 16,
        margin = ggplot2::margin(r = 10)
      ),
      axis.title.x = ggplot2::element_text(
        size = 16,
        margin = ggplot2::margin(t = 10)
      ),
      axis.text = ggplot2::element_text(size = 14),
      panel.grid.major = ggplot2::element_blank(),
      panel.grid.minor = ggplot2::element_blank(),
      plot.margin = ggplot2::margin(6, 6, 6, 6)
    )

  if (!is.null(size_metric) & size_metric != "None") {
    plot <- plot +
      ggplot2::guides(
        size = "none"
      )
  }

  if (label_outliers) {
    data$is_extreme <-
      data[[x_metric]] > quantile(data[[x_metric]], 0.95, na.rm = TRUE) |
      data[[x_metric]] < quantile(data[[x_metric]], 0.05, na.rm = TRUE) |
      data[[y_metric]] > quantile(data[[y_metric]], 0.95, na.rm = TRUE) |
      data[[y_metric]] < quantile(data[[y_metric]], 0.05, na.rm = TRUE)

    if (type == "player") {
      label_name <- "player_name"
    } else {
      label_name <- "team_shortname"
    }

    plot <- plot +
      geom_text_repel(
        data = subset(data, is_extreme),
        mapping = ggplot2::aes(
          x = .data[[x_metric]],
          y = .data[[y_metric]],
          label = paste0(.data[[label_name]], " - ", season_name)
        ),
        family = "Lexend"
      )
  }

  if (invert_x_axis) {
    plot <- plot +
      ggplot2::scale_x_reverse()
  }

  if (invert_y_axis) {
    plot <- plot +
      ggplot2::scale_y_reverse()
  }

  return(plot)
}
