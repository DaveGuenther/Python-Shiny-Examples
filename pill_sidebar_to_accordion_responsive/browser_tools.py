from shiny import ui

def get_browser_res():
    """
    This function should be called at the beginning of a shiny app.  It will store the browser resolution as a tuple (width, height) into a variable accessible as input.dimension().
    """
    return ui.tags.head(
        ui.tags.script(
            """
                var dimension = [0, 0];
                $(document).on("shiny:connected", function(e) {
                    dimension[0] = window.innerWidth;
                    dimension[1] = window.innerHeight;
                    Shiny.onInputChange("dimension", dimension);
                });
                $(window).resize(function(e) {
                    dimension[0] = window.innerWidth;
                    dimension[1] = window.innerHeight;
                    Shiny.onInputChange("dimension", dimension);
                });
            
            """
        ),
    )
