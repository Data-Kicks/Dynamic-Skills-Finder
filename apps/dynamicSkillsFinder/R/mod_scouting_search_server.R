#' @title Scouting Search Server Module
#' @description A Shiny module that provides server-side functionality for scouting search.
#'
#' @param id A character string that serves as the namespace for the module.
#'
#' @return Server-side logic for the scouting search module.
#'
#' @import shiny
#' @importFrom dplyr across collect filter first mutate pull select slice where
#' @importFrom shinyWidgets pickerInput pickerOptions updatePickerInput
#' @importFrom ggiraph geom_rect_interactive girafe opts_hover opts_selection opts_toolbar renderGirafe
#' @importFrom DT datatable DTOutput formatStyle renderDT styleInterval
#' @importFrom shinyjs hide show
#' @importFrom grDevices colorRampPalette
#' @importFrom stringr str_split
#' @importFrom shinycssloaders withSpinner
#'
#' @export
mod_scouting_search_server <- function(id) {
  shiny::moduleServer(id, function(input, output, session) {
    ns <- session$ns

    filtered_player_aggregates_data <- shiny::reactiveVal(data.frame())
    is_app_start <- shiny::reactiveVal(TRUE)
    last_player_id <- shiny::reactiveVal(NULL)
    new_metrics <- shiny::reactiveVal(c())
    new_metrics_colnames <- shiny::reactiveVal(c())
    custom_selects_cont <- shiny::reactiveVal(0)
    custom_selects_list <- shiny::reactiveValues()
    custom_selects_values <- shiny::reactiveValues()

    # Filters card logic -----------------------------------------------------
    shiny::observe({
      positions <- player_aggregates_data |>
        filter(
          season_name %in% input$season_select,
          competition_name %in% input$competition_select,
          team_shortname %in% input$team_select
        ) |>
        mutate(
          positions = strsplit(as.character(positions), split = ", ")
        ) |>
        pull(positions) |>
        unlist() |>
        unique() |>
        sort()

      max_age <- player_aggregates_data |>
        filter(
          season_name %in% input$season_select,
          competition_name %in% input$competition_select,
          team_shortname %in% input$team_select
        ) |>
        pull(age) |>
        max(na.rm = TRUE)

      max_matches_played <- player_aggregates_data |>
        filter(
          season_name %in% input$season_select,
          competition_name %in% input$competition_select,
          team_shortname %in% input$team_select
        ) |>
        pull(matches_played) |>
        max(na.rm = TRUE)

      max_matches_started <- player_aggregates_data |>
        filter(
          season_name %in% input$season_select,
          competition_name %in% input$competition_select,
          team_shortname %in% input$team_select
        ) |>
        pull(starts) |>
        max(na.rm = TRUE)

      max_minutes_played <- player_aggregates_data |>
        filter(
          season_name %in% input$season_select,
          competition_name %in% input$competition_select,
          team_shortname %in% input$team_select
        ) |>
        pull(minutes_played) |>
        max(na.rm = TRUE)

      updatePickerInput(
        session = session,
        inputId = "position_select",
        choices = shiny::req(positions),
        selected = shiny::req(positions)
      )

      updateSliderInput(
        session = session,
        inputId = "age_select",
        max = shiny::req(max_age),
        value = c(0, shiny::req(max_age))
      )

      updateSliderInput(
        session = session,
        inputId = "minutes_played_select",
        max = shiny::req(max_minutes_played),
        value = c(0, shiny::req(max_minutes_played))
      )
    })

    shiny::observe({
      competitions <- player_aggregates_data |>
        filter(season_name == input$season_select) |>
        pull(competition_name) |>
        unique() |>
        sort()

      updatePickerInput(
        session = session,
        inputId = "competition_select",
        choices = shiny::req(competitions),
        selected = shiny::req(competitions)
      )
    })

    shiny::observe({
      teams <- player_aggregates_data |>
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
        choices = shiny::req(teams),
        selected = shiny::req(teams)
      )
    })

    shiny::observeEvent(input$add_metric_filter_input, {
      custom_selects_cont(custom_selects_cont() + 1)

      select_id <- paste0("custom_select_", custom_selects_cont())
      slider_id <- paste0("custom_slider_", custom_selects_cont())
      remove_id <- paste0("remove_", custom_selects_cont())
      container_id <- paste0("container_", custom_selects_cont())

      filter_choices <- sort(
        setdiff(
          names(player_aggregates_data[, 15:ncol(player_aggregates_data)]),
          unlist(
            shiny::reactiveValuesToList(custom_selects_list),
            use.names = F
          )
        )
      )

      if (length(filter_choices) == 1) {
        hide("add_metric_filter_input")
      } else {
        show("add_metric_filter_input")
      }

      for (i in 1:length(shiny::reactiveValuesToList(custom_selects_list))) {
        slider_values <- input[[paste0("custom_slider_", i)]]

        shiny::updateSliderInput(
          session = session,
          inputId = paste0("custom_slider_", i),
          label = input[[paste0("custom_select_", i)]],
          value = slider_values
        )

        hide(paste0("custom_select_", i))
      }

      shiny::insertUI(
        selector = paste0("#", ns("custom_selects_output")),

        ui = shiny::tags$div(
          id = ns(container_id),
          shiny::actionLink(
            inputId = ns(remove_id),
            label = "x",
            class = "dynamic-link"
          ),
          pickerInput(
            inputId = ns(select_id),
            label = "",
            choices = filter_choices,
            options = pickerOptions(liveSearch = T, liveSearchNormalize = T),
            selected = filter_choices[1]
          ),
          shiny::uiOutput(ns(paste0(slider_id, "_output")))
        )
      )

      output[[paste0(slider_id, "_output")]] <- shiny::renderUI({
        col_name <- input[[select_id]]

        step_value <- if (
          class(player_aggregates_data |> pull(col_name)) == "integer"
        ) {
          1
        } else {
          0.1
        }
        min_value = round(
          as.numeric(min(
            player_aggregates_data |> pull(col_name),
            na.rm = T
          )),
          2
        )
        max_value = round(
          as.numeric(max(
            player_aggregates_data |> pull(col_name),
            na.rm = T
          )),
          2
        )
        custom_selects_list[[as.character(custom_selects_cont())]] <- col_name
        custom_selects_values[[as.character(custom_selects_cont())]] <- c(
          min_value,
          max_value
        )

        shiny::sliderInput(
          inputId = ns(slider_id),
          label = "",
          min = min_value,
          max = max_value,
          value = c(min_value, max_value),
          step = step_value
        )
      })

      shiny::observeEvent(input[[slider_id]], {
        custom_selects_values[[str_split(container_id, "_")[[1]][2]]] <- c(
          input[[slider_id]][1],
          input[[slider_id]][2]
        )
      })

      shiny::observeEvent(input[[select_id]], {
        col_name <- input[[select_id]]

        step_value <- if (
          class(player_aggregates_data |> pull(col_name)) == "integer"
        ) {
          1
        } else {
          0.1
        }
        min_value = round(
          as.numeric(min(
            player_aggregates_data |> pull(col_name),
            na.rm = T
          )),
          2
        )
        max_value = round(
          as.numeric(max(
            player_aggregates_data |> pull(col_name),
            na.rm = T
          )),
          2
        )

        if (!is.null(col_name)) {
          shiny::updateSliderInput(
            session = session,
            slider_id,
            min = min_value,
            max = max_value,
            value = c(min_value, max_value),
            step = step_value
          )

          custom_selects_list[[as.character(custom_selects_cont())]] <- col_name
          custom_selects_values[[as.character(custom_selects_cont())]] <- c(
            min_value,
            max_value
          )
        }
      })

      shiny::observeEvent(input[[remove_id]], {
        shiny::removeUI(selector = paste0("#", ns(container_id)))

        custom_selects_list[[str_split(container_id, "_")[[1]][2]]] <- NULL
        custom_selects_values[[str_split(container_id, "_")[[1]][2]]] <- NULL

        show("add_metric_filter_input")
      })
    })

    shiny::observeEvent(input$apply_filters_button, {
      is_app_start(FALSE)

      filtered_player_aggregates_data(
        filter_aggregates(
          data = player_aggregates_data,
          seasons = input$season_select,
          competitions = input$competition_select,
          teams = input$team_select,
          player_names = input$player_name_input,
          position_list = input$position_select,
          age_range = input$age_select,
          matches_played_range = input$matches_played_select,
          matches_started_range = input$matches_started_select,
          minutes_played_range = input$minutes_played_select,
          custom_filter_metrics = unlist(
            shiny::reactiveValuesToList(custom_selects_list),
            use.names = F
          ),
          custom_filter_values = unlist(
            shiny::reactiveValuesToList(custom_selects_values),
            use.names = F
          )
        )
      )
    })

    output$no_results_label <- shiny::renderText({
      if (nrow(filtered_player_aggregates_data()) == 0) {
        if (is_app_start()) {
          "Adjust your filters and press 'Apply' to see results."
        } else {
          "No results found applying the selected filters. Please, adjust your filters and try again."
        }
      }
    })

    output$results_ui <- shiny::renderUI({
      if (nrow(filtered_player_aggregates_data()) > 0) {
        shiny::tagList(
          withSpinner(
            DTOutput(ns("filtered_player_aggregates_table")),
            color = "#00a82f",
            type = 7,
            proxy.height = "653px"
          ),
          shiny::checkboxInput(
            inputId = ns("show_basic_info_input"),
            label = "Show player basic info",
            value = TRUE
          ),
          shiny::uiOutput(ns("download_filtered_players_ui"))
        )
      }
    })
    output$filtered_player_aggregates_table <- renderDT(
      {
        if (nrow(filtered_player_aggregates_data()) > 0) {
          if (input$show_basic_info_input) {
            info_columns <- names(player_agg_info_columns)
            info_names <- unname(unlist(player_agg_info_columns))
          } else {
            info_columns <- setdiff(
              names(player_agg_info_columns),
              names(player_agg_basic_info_columns)
            )
            info_names <- setdiff(
              unname(unlist(player_agg_info_columns)),
              unname(unlist(player_agg_basic_info_columns))
            )
          }

          table_data <- filtered_player_aggregates_data() |>
            select(
              info_columns,
              unlist(
                shiny::isolate(shiny::reactiveValuesToList(
                  custom_selects_list
                )),
                use.names = F
              )
            ) |>
            collect()

          table <- datatable(
            data = table_data |> mutate(across(where(is.numeric), round, 2)),
            fillContainer = TRUE,
            options = list(
              scrollY = "71vh",
              searching = FALSE,
              paging = FALSE,
              info = FALSE,
              ordering = TRUE,
              columnDefs = list(list(
                className = "dt-center",
                targets = "_all"
              ))
            ),
            width = "100%",
            selection = "single",
            colnames = c(
              info_names,
              unname(unlist(
                player_agg_metric_columns[unlist(
                  shiny::isolate(shiny::reactiveValuesToList(
                    custom_selects_list
                  )),
                  use.names = F
                )]
              ))
            ),
            rownames = TRUE,
            escape = ncol(table_data) - 1
          ) |>
            formatStyle(
              "player_name",
              backgroundColor = "#eaf12013",
              fontWeight = 'bold'
            )

          if (input$show_basic_info_input) {
            table <- table |>
              formatStyle(
                names(player_agg_basic_info_columns),
                backgroundColor = "#f1a82011"
              ) |>
              formatStyle(
                c("positions", "age"),
                backgroundColor = "#eaf12013"
              )
          }

          tabla_num <- table_data[sapply(table_data, is.numeric)]

          if ("age" %in% names(tabla_num)) {
            table_names <- names(tabla_num |> select(-age))
          } else {
            table_names <- names(tabla_num)
          }

          for (col in table_names) {
            if (is.numeric(tabla_num[[col]])) {
              brks <- quantile(
                tabla_num[[col]],
                probs = seq(0.10, 0.90, 0.10),
                na.rm = TRUE
              )

              if (player_agg_metric_types[col] == "OBR") {
                clrs <- colorRampPalette(c("#fbfbfb", "#5db873"))(
                  length(brks) + 1
                )
              } else if (player_agg_metric_types[col] == "OBE") {
                clrs <- colorRampPalette(c("#fbfbfb", "#f99c31ff"))(
                  length(brks) + 1
                )
              } else if (player_agg_metric_types[col] == "OBEv") {
                clrs <- colorRampPalette(c("#fbfbfb", "#31c4f9ff"))(
                  length(brks) + 1
                )
              } else {
                clrs <- colorRampPalette(c("#fbfbfb", "#6c87d8ff"))(
                  length(brks) + 1
                )
              }

              table <- formatStyle(
                table,
                col,
                backgroundColor = styleInterval(brks, clrs)
              )
            }
          }

          table
        } else {
          hide("results_div")
        }
      }
    )

    shiny::observeEvent(input$filtered_player_aggregates_table_rows_selected, {
      if (!is.null(input$filtered_player_aggregates_table_rows_selected)) {
        last_player_id(input$filtered_player_aggregates_table_rows_selected)

        mod_player_info_server(
          "player_info",
          filter_aggregates(
            data = player_aggregates_data,
            seasons = input$season_select,
            competitions = input$competition_select,
            teams = input$team_select,
            position_list = input$position_select,
            minutes_played_range = input$minutes_played_select,
          ) |>
            select(
              player_id,
              names(player_agg_info_columns),
              unlist(
                shiny::reactiveValuesToList(custom_selects_list),
                use.names = F
              )
            ) |>
            collect(),
          filtered_player_aggregates_data() |>
            select(
              player_id
            ) |>
            collect() |>
            slice(input$filtered_player_aggregates_table_rows_selected) |>
            pull(player_id)
        )

        shiny::showModal(
          shiny::tagList(
            shiny::div(
              id = ns("player_info_modal_container"),
              shiny::modalDialog(
                id = ns("player_info_modal"),
                title = "Player info",
                size = "xl",
                easyClose = T,
                footer = shiny::tagList(
                  shiny::modalButton("Close")
                ),
                mod_player_info_ui(
                  ns("player_info"),
                  filtered_player_aggregates_data() |>
                    select(
                      player_id,
                      names(player_agg_info_columns)
                    ) |>
                    collect() |>
                    slice(
                      input$filtered_player_aggregates_table_rows_selected
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
        )
      }
    })

    shiny::observeEvent(input$player_info_button, {
      if (!is.null(input$filtered_player_aggregates_table_rows_selected)) {
        last_player_id(input$filtered_player_aggregates_table_rows_selected)
      }
    })

    output$download_filtered_players_ui <- renderUI({
      if (nrow(filtered_player_aggregates_data()) > 0) {
        shiny::downloadLink(
          ns("download_filtered_players_data"),
          "Download as CSV..."
        )
      }
    })

    output$download_filtered_players_data <- shiny::downloadHandler(
      filename = function() {
        paste0(
          "players_data_",
          gsub(" ", "_", tolower(Sys.Date())),
          ".csv"
        )
      },
      content = function(file) {
        write.csv(
          filtered_player_aggregates_data() |>
            select(
              names(player_agg_info_columns),
              unlist(
                shiny::isolate(shiny::reactiveValuesToList(
                  custom_selects_list
                )),
                use.names = F
              )
            ) |>
            collect(),
          file,
          row.names = FALSE
        )
      }
    )
  })
}
