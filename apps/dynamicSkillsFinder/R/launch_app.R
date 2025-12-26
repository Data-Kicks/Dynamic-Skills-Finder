#' @title Launch the Shiny Application
#' @description This function launches the Dynamic Skills Finder Shiny application.
#' It sets up the UI and server components and starts the app with specified options.
#'
#' @import shiny
#'
#' @export
launch_app <- function(options = list()) {
  shiny::shinyApp(
    ui = ui,
    server = server,
    options = options
  )
}
