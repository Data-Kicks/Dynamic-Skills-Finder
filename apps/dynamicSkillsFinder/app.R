if (!interactive()) {
  sink(stderr(), type = "output")
  tryCatch(
    expr = {
      library(dynamicSkillsFinder)
    },
    error = function(e) {
      pkgload::load_all()
    }
  )
} else {
  pkgload::load_all()
}

launch_app(options = list(test.mode = FALSE))
