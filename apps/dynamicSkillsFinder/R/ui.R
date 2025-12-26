#' @title Main User Interface of the Dynamic Skills Finder Shiny App
#' @description This function defines the main user interface (UI) of the Dynamic Skills Finder Shiny application.
#' It sets up the navigation bar, themes, and integrates various modules for tactical and scouting functionalities.
#'
#' @import shiny
#' @importFrom bslib bs_theme css font_google page_navbar nav_panel nav_menu nav_item nav_spacer
#' @importFrom bsicons bs_icon

ui <- function() {
  addResourcePath(
    prefix = "www",
    directoryPath = system.file("www", package = "dynamicSkillsFinder")
  )
  shiny::tagList(
    page_navbar(
      id = "menubar",
      title = shiny::tagList(
        shiny::tags$img(
          id = "menubar-img",
          src = "www/images/dsf_logo_shortcut_circle.png",
          width = 40
        ),
        shiny::tags$span("DYNAMIC "),
        shiny::tags$span(
          "SKILLS",
          style = 'color: #33ff6a !important; font-weight: bolder !important;'
        ),
        shiny::tags$span(" FINDER"),
        shiny::tags$head(
          shiny::tags$link(
            rel = "shortcut icon",
            href = "www/images/dsf_logo_shortcut_circle.png"
          )
        ),
        shiny::tags$link(
          rel = "stylesheet",
          type = "text/css",
          href = "www/styles/style.css"
        )
      ),
      theme = bs_theme(
        base_font = font_google("Lexend"),
        heading_font = font_google("Lexend")
      ),
      shiny::div(
        id = "div-menubar-spacer1",
        nav_spacer()
      ),
      nav_panel(
        title = "Home",
        icon = bs_icon("house-door-fill"),
        style = css(
          background = "url('www/images/home_background_image.svg') no-repeat center center fixed",
          background_size = "cover"
        )
      ),
      nav_menu(
        title = "Tactical",
        nav_panel(
          title = "Find...",
          icon = bs_icon("search"),
          mod_tactical_find_ui("tactical_find")
        ),
        nav_panel(
          title = "Compare",
          icon = bs_icon("clipboard-data"),
          mod_compare_ui(
            "tactical_compare",
            type = "team"
          )
        )
      ),
      nav_menu(
        title = "Scouting",
        nav_panel(
          title = "Search...",
          icon = bs_icon("search"),
          mod_scouting_search_ui("scouting_search")
        ),
        nav_panel(
          title = "Compare",
          icon = bs_icon("person-lines-fill"),
          mod_compare_ui(
            "scouting_compare",
            type = "player"
          )
        )
      ),
      nav_spacer(),
      nav_menu(
        title = "Help",
        icon = bs_icon("question-lg"),
        align = "right",
        nav_panel(
          title = "User video guide",
          icon = bs_icon("info-circle"),
          mod_help_ui("help")
        ),
        nav_item(
          shiny::tags$a(
            "About the author...",
            href = "https://www.linkedin.com/in/obartolomep/",
            target = "_blank"
          )
        )
      )
    )
  )
}
