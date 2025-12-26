#' @title Player Info Server Module
#' @description A Shiny module server function to display player information
#' and a pizza plot based on selected metrics.
#'
#' @param id A character string specifying the module ID.
#' @param data A data frame containing player statistics.
#' @param player_row An integer specifying the row of the player to display.
#'
#' @return A Shiny module server function.
#'
#' @import shiny
#' @importFrom dplyr collect first filter pull select
#' @importFrom DT datatable
#' @importFrom ggiraph girafe opts_hover opts_selection opts_toolbar renderGirafe
#'
#' @export
mod_player_info_server <- function(id, data, player_row) {
  shiny::moduleServer(id, function(input, output, session) {
    ns <- session$ns

    if (
      length(
        setdiff(
          names(data |> select(-player_id)),
          names(player_agg_info_columns)
        )
      ) >
        0
    ) {
      players_prct_data <- calculate_percentiles(
        data |>
          select(
            setdiff(
              names(data),
              names(player_agg_info_columns)
            )
          )
      )
    } else {
      players_prct_data <- data.frame()
    }

    output$no_results_label <- shiny::renderText({
      if (nrow(players_prct_data) == 0) {
        return("Select metrics in filter panel to see player plot")
      }
    })

    output$player_pizzaplot_output <- renderGirafe({
      if (nrow(players_prct_data) > 0) {
        plot <- draw_pizza_plot(
          players_prct_data |>
            filter(player_id == player_row) |>
            select(-c(player_id, player_id_prct))
        )

        girafe(
          ggobj = plot,
          width_svg = 10,
          height_svg = 10,
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
              pngname = "player_dynamic_events_plot"
            )
          )
        )
      }
    })
  })
}
