#' @title Comparison Module Server
#' @description Shiny module server function for comparing players or teams based on selected metrics.
#'
#' @param id A character string specifying the module ID.
#' @param type A character string specifying the type of comparison: "player" or "team". Default is "player".
#'
#' @return A Shiny server function for the comparison module.
#'
#' @import shiny
#' @importFrom dplyr collect filter first group_by mutate pull select slice summarise
#' @importFrom shinyWidgets updatePickerInput
#' @importFrom ggiraph geom_rect_interactive girafe opts_hover opts_selection opts_toolbar renderGirafe
#'
#' @export
mod_compare_server <- function(id, type = "player") {
  shiny::moduleServer(id, function(input, output, session) {
    ns <- session$ns

    filtered_comparison_data <- shiny::reactiveVal(data.frame())
    is_app_start <- shiny::reactiveVal(TRUE)

    if (type == "player") {
      comparison_data <- player_aggregates_data
      metrics <- sort(names(player_agg_metric_columns))
    } else if (type == "team") {
      comparison_data <- team_aggregates_data
      metrics <- sort(names(team_agg_metric_columns))
    }

    output$minutes_played_ui <- shiny::renderUI({
      if (type == "player") {
        positions <- comparison_data |>
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

        max_age <- comparison_data |>
          filter(
            season_name %in% input$season_select,
            competition_name %in% input$competition_select,
            team_shortname %in% input$team_select
          ) |>
          pull(age) |>
          max(na.rm = TRUE)

        max_minute <- comparison_data |>
          filter(
            season_name %in% input$season_select,
            competition_name %in% input$competition_select,
            team_shortname %in% input$team_select
          ) |>
          pull(minutes_played) |>
          max(na.rm = TRUE)

        shiny::tagList(
          shinyWidgets::pickerInput(
            inputId = ns("position_select"),
            label = "Positions",
            choices = shiny::req(positions),
            selected = shiny::req(positions),
            options = pickerOptions(
              liveSearch = TRUE,
              liveSearchNormalize = TRUE,
              liveSearchPlaceholder = "Search...",
              actionsBox = TRUE,
              selectedTextFormat = "count > 1",
              noneSelectedText = paste0("No position selected"),
              selectAllText = "All",
              deselectAllText = "None",
              countSelectedText = paste0("{0} positions selected")
            ),
            multiple = TRUE
          ),
          shiny::sliderInput(
            inputId = ns("age_input"),
            label = "Age",
            min = 0,
            max = shiny::req(max_age),
            value = c(0, shiny::req(max_age)),
            step = 1
          ),
          shiny::sliderInput(
            inputId = ns("minutes_played_input"),
            label = "Minutes played",
            min = 0,
            max = shiny::req(max_minute),
            value = c(0, shiny::req(max_minute)),
            step = 45
          )
        )
      }
    })

    shiny::observe({
      competitions <- comparison_data |>
        filter(season_name %in% input$season_select) |>
        pull(competition_name) |>
        unique() |>
        sort()

      updatePickerInput(
        session = session,
        inputId = "competition_select",
        choices = shiny::req(competitions),
        selected = first(shiny::req(competitions))
      )
    })

    shiny::observe({
      teams <- comparison_data |>
        filter(
          season_name %in% input$season_select,
          competition_name %in% input$competition_select
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

    if (type == "player") {
      shiny::observe({
        players <- comparison_data |>
          filter(
            season_name %in% input$season_select,
            competition_name %in% input$competition_select,
            team_shortname %in% input$team_select
          ) |>
          pull(player_name) |>
          unique() |>
          sort()

        updatePickerInput(
          session = session,
          inputId = "highlight_players_select",
          choices = shiny::req(players),
          selected = c()
        )
      })
    }

    shiny::observeEvent(input$apply_filters_button, {
      is_app_start(FALSE)

      if (type == "player") {
        aggregates_data <- player_aggregates_data
      } else if (type == "team") {
        aggregates_data <- team_aggregates_data
      }

      filtered_comparison_data(
        filter_aggregates(
          data = aggregates_data,
          seasons = input$season_select,
          competitions = input$competition_select,
          teams = input$team_select,
          position_list = input$position_select,
          age_range = input$age_input,
          minutes_played_range = input$minutes_played_input
        )
      )
    })

    output$no_results_label <- shiny::renderText({
      if (nrow(filtered_comparison_data()) == 0) {
        if (is_app_start()) {
          "Adjust your filters and press 'Apply' to see results."
        } else {
          "No results found applying the selected filters. Please, adjust your filters and try again."
        }
      }
    })

    output$comparison_scatter_plot <- renderGirafe({
      if (nrow(filtered_comparison_data()) > 0) {
        plot <- draw_scatter_plot(
          data = filtered_comparison_data() |> collect(),
          x_metric = shiny::isolate(input$x_axis_metric_select),
          y_metric = shiny::isolate(input$y_axis_metric_select),
          size_metric = shiny::isolate(input$size_metric_select),
          label_outliers = shiny::isolate(input$label_outliers_input),
          invert_x_axis = shiny::isolate(input$invert_x_axis_input),
          invert_y_axis = shiny::isolate(input$invert_y_axis_input),
          type = type
        )

        girafe(
          ggobj = plot,
          width_svg = 12,
          height_svg = 10,
          options = list(
            opts_selection(
              css = "fill:#f99c31ff; stroke:#a55901ff;"
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
              pngname = "dynamic_events_scatter_plot"
            )
          )
        )
      }
    })
  })
}
