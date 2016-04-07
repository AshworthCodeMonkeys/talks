
library(shinyngs)

# An list of objects extending SummarizedExperiment containing:
#
# - 1 or more 'experiments' with different features (genes, transcripts)
# - Each experiment containing one or more expression matrices

data("zhangneurons")

# Build the RNA-seq app

app <- prepareApp('rnaseq', zhangneurons)

# Send the app to Shiny

shiny::shinyApp(ui = app$ui, server = app$server)