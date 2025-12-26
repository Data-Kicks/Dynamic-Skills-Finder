#' @title Tactical Find Server Module
#' @description Shiny module server function for the Tactical Find feature.
#' This module handles filtering dynamic events data based on user inputs,
#' rendering interactive plots and tables, and managing video playback for selected events.
#'
#' @param id Module ID.
#'
#' @return Shiny module server function.
#'
#' @import shiny
#' @importFrom dplyr collect filter group_by mutate pull select slice summarise
#' @importFrom shinyWidgets updatePickerInput
#' @importFrom ggiraph geom_rect_interactive girafe opts_hover opts_selection opts_toolbar renderGirafe
#' @importFrom DT datatable DTOutput formatStyle renderDT
#' @importFrom stringr str_starts
#' @importFrom shinycssloaders withSpinner
#'
#' @export
mod_tactical_find_server <- function(id) {
  shiny::moduleServer(id, function(input, output, session) {
    ns <- session$ns

    filtered_dynamic_events_data <- shiny::reactiveVal(data.frame())
    is_app_start <- shiny::reactiveVal(TRUE)
    last_video_id <- shiny::reactiveVal(NULL)
    show_heatmap <- shiny::reactiveVal(FALSE)

    # Filters card logic -----------------------------------------------------
    shiny::observe(
      {
        if (input$insights_type == "Attacking (OBR)") {
          insight_type <- "off_ball_run"
        } else {
          insight_type <- "on_ball_engagement"
        }

        periods <- dynamic_events_data |>
          filter(
            season_name == input$season_select,
            competition_name == input$competition_select,
            team_shortname == input$team_select,
            match_longname %in% input$match_select
          ) |>
          pull(period_name) |>
          unique() |>
          sort()

        max_minute <- dynamic_events_data |>
          filter(
            season_name == input$season_select,
            competition_name == input$competition_select,
            team_shortname == input$team_select,
            match_longname %in% input$match_select
          ) |>
          pull(minute_start) |>
          max(na.rm = TRUE)

        game_states <- dynamic_events_data |>
          filter(
            season_name == input$season_select,
            competition_name == input$competition_select,
            team_shortname == input$team_select,
            match_longname %in% input$match_select,
            event_type == insight_type
          ) |>
          pull(game_state) |>
          unique() |>
          sort()

        game_phases <- dynamic_events_data |>
          filter(
            season_name == input$season_select,
            competition_name == input$competition_select,
            team_shortname == input$team_select,
            match_longname %in% input$match_select,
            event_type == insight_type
          ) |>
          pull(team_in_possession_phase_type) |>
          unique() |>
          sort()

        event_players <- dynamic_events_data |>
          filter(
            season_name == input$season_select,
            competition_name == input$competition_select,
            team_shortname == input$team_select,
            match_longname %in% input$match_select,
            event_type == insight_type
          ) |>
          pull(player_name) |>
          unique() |>
          sort()

        event_player_positions <- dynamic_events_data |>
          filter(
            season_name == input$season_select,
            competition_name == input$competition_select,
            team_shortname == input$team_select,
            match_longname %in% input$match_select,
            event_type == insight_type
          ) |>
          pull(player_position) |>
          unique() |>
          sort()

        if (insight_type == "on_ball_engagement") {
          game_phases <- dynamic_events_data |>
            filter(
              season_name == input$season_select,
              competition_name == input$competition_select,
              team_shortname == input$team_select,
              match_longname %in% input$match_select,
              event_type == insight_type
            ) |>
            pull(team_out_of_possession_phase_type) |>
            unique() |>
            sort()

          possession_players <- dynamic_events_data |>
            filter(
              season_name == input$season_select,
              competition_name == input$competition_select,
              team_shortname == input$team_select,
              match_longname %in% input$match_select,
              event_type == insight_type
            ) |>
            pull(player_in_possession_name) |>
            unique() |>
            sort()

          possession_player_positions <- dynamic_events_data |>
            filter(
              season_name == input$season_select,
              competition_name == input$competition_select,
              team_shortname == input$team_select,
              match_longname %in% input$match_select,
              event_type == insight_type
            ) |>
            pull(player_in_possession_position) |>
            unique() |>
            sort()
        } else {
          possession_players <- event_players
          possession_player_positions <- event_player_positions
        }

        event_subtypes <- dynamic_events_data |>
          filter(
            season_name == input$season_select,
            competition_name == input$competition_select,
            team_shortname == input$team_select,
            match_longname %in% input$match_select,
            event_type == insight_type
          ) |>
          pull(event_subtype) |>
          unique() |>
          sort()

        updatePickerInput(
          session = session,
          inputId = "period_select",
          choices = shiny::req(periods),
          selected = shiny::req(periods)
        )
        updateSliderInput(
          session = session,
          inputId = "minute_select",
          min = 0,
          max = shiny::req(max_minute),
          value = c(0, shiny::req(max_minute)),
          step = 1
        )
        updatePickerInput(
          session = session,
          inputId = "game_state_select",
          choices = shiny::req(game_states),
          selected = shiny::req(game_states)
        )
        updatePickerInput(
          session = session,
          inputId = "game_phase_select",
          choices = shiny::req(game_phases),
          selected = shiny::req(game_phases)
        )
        updatePickerInput(
          session = session,
          inputId = "possession_player_select",
          choices = shiny::req(possession_players),
          selected = shiny::req(possession_players)
        )
        updatePickerInput(
          session = session,
          inputId = "possession_player_position_select",
          choices = shiny::req(possession_player_positions),
          selected = shiny::req(possession_player_positions)
        )
        updatePickerInput(
          session = session,
          inputId = "event_player_select",
          choices = shiny::req(event_players),
          selected = shiny::req(event_players)
        )
        updatePickerInput(
          session = session,
          inputId = "Event_player_position_select",
          choices = shiny::req(event_player_positions),
          selected = shiny::req(event_player_positions)
        )
        updatePickerInput(
          session = session,
          inputId = "event_subtype_select",
          choices = shiny::req(event_subtypes),
          selected = shiny::req(event_subtypes)
        )
      }
    )

    shiny::observe({
      competitions <- dynamic_events_data |>
        filter(season_name == input$season_select) |>
        pull(competition_name) |>
        unique() |>
        sort()

      updatePickerInput(
        session = session,
        inputId = "competition_select",
        choices = shiny::req(competitions)
      )
    })

    shiny::observe({
      teams <- dynamic_events_data |>
        filter(
          season_name == input$season_select,
          competition_name == input$competition_select
        ) |>
        pull(team_shortname) |>
        unique() |>
        sort()

      updatePickerInput(
        session = session,
        inputId = "team_select",
        choices = shiny::req(teams)
      )
    })

    shiny::observe({
      matches <- dynamic_events_data |>
        filter(
          season_name == input$season_select,
          competition_name == input$competition_select,
          team_shortname == input$team_select,
          group %in% input$home_away_select
        ) |>
        pull(match_longname) |>
        unique() |>
        sort()

      updatePickerInput(
        session = session,
        inputId = "match_select",
        choices = shiny::req(matches),
        selected = shiny::req(matches)
      )
    })

    output$possession_pitch <- renderGirafe({
      girafe(
        ggobj = draw_football_pitch(pitch_color = "#fbfbfb", zones = TRUE),
        width_svg = 7,
        height_svg = 4.5,
        options = list(
          opts_hover(css = "fill:#57635d85;"),
          opts_selection(
            type = "multiple",
            only_shiny = FALSE,
            css = "fill:#00a8307c;"
          ),
          opts_toolbar(
            hidden = c(
              "lasso_select",
              "lasso_deselect",
              "zoom_onoff",
              "zoom_rect",
              "zoom_reset",
              "saveaspng"
            )
          )
        )
      )
    })

    output$event_pitch <- renderGirafe({
      girafe(
        ggobj = draw_football_pitch(pitch_color = "#fbfbfb", zones = TRUE),
        width_svg = 7,
        height_svg = 4.5,
        options = list(
          opts_hover(css = "fill:#57635d85;"),
          opts_selection(
            type = "multiple",
            only_shiny = FALSE,
            css = "fill:#00a8307c;"
          ),
          opts_toolbar(
            hidden = c(
              "lasso_select",
              "lasso_deselect",
              "zoom_onoff",
              "zoom_rect",
              "zoom_reset",
              "saveaspng"
            )
          )
        )
      )
    })

    shiny::observeEvent(input$apply_filters_button, {
      is_app_start(FALSE)

      filtered_dynamic_events_data(
        filter_dynamic_events(
          data = dynamic_events_data,
          insight_type = input$insights_type,
          subevents = input$event_subtype_select,
          seasons = input$season_select,
          competitions = input$competition_select,
          teams = input$team_select,
          home_away = input$home_away_select,
          match_longnames = input$match_select,
          periods = input$period_select,
          minute_range = input$minute_select,
          gamestates = input$game_state_select,
          gamephases = input$game_phase_select,
          possession_players = input$possession_player_select,
          possession_positions = input$possession_player_position_select,
          possession_zones = input$possession_pitch_selected,
          event_players = input$event_player_select,
          event_positions = input$Event_player_position_select,
          event_zones = input$event_pitch_selected,
          event_from_to = input$event_player_from_to_switch
        )
      )
    })

    # Results card logic -----------------------------------------------------
    create_table_buttons <- function(tbl) {
      function(i) {
        sprintf(
          paste0(
            '<button class="btn btn-default action-button shiny-bound-input" id="',
            ns("play_button"),
            '_%s_%d" type="button" onclick="%s">></button>'
          ),
          tbl,
          i,
          paste0(
            "Shiny.setInputValue('",
            ns("play_button"),
            "', this.id, {priority: 'event'});"
          )
        )
      }
    }

    output$no_results_label <- shiny::renderText({
      if (nrow(filtered_dynamic_events_data()) == 0) {
        if (is_app_start()) {
          "Adjust your filters and press 'Apply' to see results."
        } else {
          "No results found applying the selected filters. Please, adjust your filters and try again."
        }
      }
    })

    output$show_heatmap_ui <- shiny::renderUI({
      if (nrow(filtered_dynamic_events_data()) > 0) {
        if (length(input$filtered_dynamic_events_table_rows_selected) == 0) {
          shiny::tagList(
            shiny::checkboxInput(
              inputId = ns("show_heatmap_input"),
              label = "Show as heatmap",
              value = show_heatmap()
            )
          )
        }
      }
    })

    shiny::observeEvent(input$show_heatmap_input, {
      show_heatmap(input$show_heatmap_input)
    })

    output$filtered_dynamic_events_plot_ui <- shiny::renderUI({
      if (nrow(filtered_dynamic_events_data()) > 0) {
        shiny::tagList(
          withSpinner(
            girafeOutput(ns("filtered_dynamic_events_plot")),
            color = "#00a82f",
            type = 7,
            proxy.height = "650px"
          )
        )
      }
    })

    output$filtered_dynamic_events_plot <- renderGirafe({
      if (nrow(filtered_dynamic_events_data()) > 0) {
        if (length(input$filtered_dynamic_events_table_rows_selected) > 0) {
          events <- filtered_dynamic_events_data() |>
            collect() |>
            slice(input$filtered_dynamic_events_table_rows_selected)
        } else {
          events <- filtered_dynamic_events_data()
        }

        if (
          show_heatmap() &
            length(input$filtered_dynamic_events_table_rows_selected) == 0
        ) {
          if (isolate(input$event_player_from_to_switch)) {
            zone_col <- "zone_start"
          } else {
            zone_col <- "zone_end"
          }

          heatmap_data <- filtered_dynamic_events_data() |>
            select(
              .data[[zone_col]],
              targeted,
              received
            ) |>
            group_by(
              zone = .data[[zone_col]]
            ) |>
            summarise(
              total = n(),
              targeted = sum(targeted, na.rm = TRUE),
              received = sum(received, na.rm = TRUE),
              .groups = "drop"
            )

          heatmap_data <- heatmap_data |>
            filter(!str_starts(zone, "Out of pitch"))

          plot <- draw_football_pitch(
            lines_width = 0.4,
            lines_color = "#7d7d7dff",
            arrow = (length(
              input$filtered_dynamic_events_table_rows_selected
            ) ==
              0),
            zones = TRUE
          ) |>
            draw_dynamic_events_heatmap(
              heatmap_data,
              shiny::isolate(input$insights_type)
            )
        } else {
          plot <- draw_football_pitch(
            lines_width = 0.4,
            lines_color = "#7d7d7dff",
            arrow = (length(
              input$filtered_dynamic_events_table_rows_selected
            ) ==
              0)
          ) |>
            draw_dynamic_events_arrows(
              data = events |>
                select(
                  x_start,
                  y_start,
                  x_end,
                  y_end,
                  targeted,
                  received,
                  match_name,
                  team_shortname,
                  player_name,
                  player_number,
                  player_position,
                  event_type,
                  event_subtype,
                  game_state,
                  team_in_possession_phase_type,
                  team_out_of_possession_phase_type,
                  xthreat,
                  xpass_completion,
                  passing_option_score,
                  x_start_tracking,
                  y_start_tracking,
                  x_end_tracking,
                  y_end_tracking
                ) |>
                collect(),
              tracking_plot = (length(
                input$filtered_dynamic_events_table_rows_selected
              ) >
                0)
            )
        }

        if (length(input$filtered_dynamic_events_table_rows_selected) > 0) {
          tracking_sel <- filtered_dynamic_events_data() |>
            collect() |>
            slice(shiny::isolate(
              input$filtered_dynamic_events_table_rows_selected
            ))

          if (nrow(tracking_sel) > 0) {
            match_id_val <- tracking_sel |> pull(match_id)
            frame_val <- tracking_sel |> pull(frame_start)

            tracking_data_frame <- tracking_data |>
              filter(
                match_id %in% local(match_id_val),
                frame %in% local(frame_val)
              ) |>
              collect()

            plot <- plot |>
              draw_tracking_data_players_and_ball(
                data = tracking_data_frame
              )
          }
        }

        if (
          show_heatmap() &
            length(input$filtered_dynamic_events_table_rows_selected) == 0
        ) {
          girafe(
            ggobj = plot,
            width_svg = 10,
            height_svg = 7.5,
            options = list(
              opts_selection(type = "none"),
              opts_hover(css = "fill:none;"),
              opts_toolbar(
                hidden = c(
                  "lasso_select",
                  "lasso_deselect",
                  "zoom_onoff",
                  "zoom_rect",
                  "zoom_reset"
                ),
                pngname = "dynamic_events_heatmap"
              )
            )
          )
        } else {
          girafe(
            ggobj = plot,
            width_svg = 10,
            height_svg = 7.5,
            options = list(
              opts_selection(
                type = "none"
              ),
              opts_hover(css = "fill:#57635d85; stroke:#57635d85;"),
              opts_toolbar(
                hidden = c(
                  "lasso_select",
                  "lasso_deselect",
                  "zoom_onoff",
                  "zoom_rect",
                  "zoom_reset"
                ),
                pngname = "dynamic_events_pitch"
              )
            )
          )
        }
      }
    })

    output$filtered_dynamic_events_table_ui <- shiny::renderUI({
      if (nrow(filtered_dynamic_events_data()) > 0) {
        shiny::tagList(
          withSpinner(
            DTOutput(ns("filtered_dynamic_events_table")),
            color = "#00a82f",
            type = 7,
            proxy.height = "650px"
          )
        )
      }
    })

    output$filtered_dynamic_events_table <- renderDT(
      {
        if (nrow(filtered_dynamic_events_data()) > 0) {
          table_data <- filtered_dynamic_events_data() |>
            select(
              match_longname,
              period,
              time_start,
              player_number,
              player_name,
              player_position,
              event_subtype
            ) |>
            collect()
          table_data <- table_data |>
            cbind(
              Video = sapply(
                1:nrow(table_data),
                create_table_buttons("filtered_dynamic_events_table")
              ),
              stringsAsFactors = FALSE
            )

          datatable(
            data = table_data,
            class = 'cell-border stripe',
            fillContainer = TRUE,
            options = list(
              scrollY = "653px",
              searching = FALSE,
              paging = FALSE,
              info = FALSE,
              order = list(c(1, 'asc')),
              ordering = TRUE,
              columnDefs = list(
                list(className = "dt-center", targets = "_all")
              )
            ),
            width = "100%",
            selection = "single",
            colnames = c(
              "Match",
              "Period",
              "Time",
              "#",
              "Player",
              "Position",
              "Event subtype",
              "Video"
            ),
            rownames = TRUE,
            escape = ncol(table_data) - 1,
          ) |>
            formatStyle(
              c("match_longname", "period", "time_start"),
              backgroundColor = "#f1a82011"
            ) |>
            formatStyle(
              c("player_number", "player_name", "player_position"),
              backgroundColor = "#eaf12013"
            ) |>
            formatStyle(
              "event_subtype",
              backgroundColor = "#5db87412"
            )
        }
      }
    )

    output$download_filtered_dynamic_events_ui <- shiny::renderUI({
      if (nrow(filtered_dynamic_events_data()) > 0) {
        shiny::downloadLink(
          ns("download_filtered_dynamic_events_data"),
          "Download as CSV..."
        )
      }
    })

    output$download_filtered_dynamic_events_data <- shiny::downloadHandler(
      filename = function() {
        paste0(
          "dynamic_events_data_",
          gsub(" ", "_", tolower(Sys.Date())),
          ".csv"
        )
      },
      content = function(file) {
        write.csv(
          filtered_dynamic_events_data() |>
            select(
              match_longname,
              period,
              time_start,
              player_number,
              player_name,
              player_position,
              event_subtype
            ) |>
            collect(),
          file,
          row.names = FALSE
        )
      }
    )

    shiny::observeEvent(input$filtered_dynamic_events_table_rows_selected, {
      if (!is.null(input$filtered_dynamic_events_table_rows_selected)) {
        last_video_id(input$filtered_dynamic_events_table_rows_selected)
      }
    })

    shiny::observeEvent(input$play_button, {
      if (!is.null(input$filtered_dynamic_events_table_rows_selected)) {
        last_video_id(input$filtered_dynamic_events_table_rows_selected)
      }

      mod_event_video_server(
        "dynamic_event_video",
        filtered_dynamic_events_data() |>
          collect() |>
          slice(
            shiny::isolate(last_video_id())
          )
      )

      shiny::showModal(
        shiny::tagList(
          shiny::modalDialog(
            title = "Dynamic Event Video",
            size = "xl",
            easyClose = T,
            footer = shiny::tagList(
              shiny::modalButton("Close")
            ),
            mod_event_video_ui(
              ns("dynamic_event_video"),
              filtered_dynamic_events_data() |>
                collect() |>
                slice(
                  shiny::isolate(last_video_id())
                )
            ),
            shiny::tags$script(HTML(
              '$(".modal").draggable({
                      handle: ".modal-header"
                      });'
            ))
          )
        )
      )
    })
  })
}
