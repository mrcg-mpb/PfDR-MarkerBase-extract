#!/usr/bin/env Rscript
# Validate one study's three files against the real STAVE package — the guardrail
# outside the agent. Args: <study.yaml> <surveys.csv> <counts.csv>.
#
# Prints exactly "OK" on success, or "STAVE_ERROR: <message>" on failure, and
# always exits 0 (the Python caller reads stdout and feeds any error back to the
# agent for repair). Requires STAVE (>=2.0.4) and variantstring (>=1.8.7) — these
# surface real validation messages (earlier versions could raise an empty error).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  cat("STAVE_ERROR: expected 3 args (study.yaml surveys.csv counts.csv)\n")
  quit(status = 0)
}

result <- tryCatch({
  if (!requireNamespace("STAVE", quietly = TRUE)) stop("STAVE package not installed")
  if (!requireNamespace("yaml", quietly = TRUE)) stop("yaml package not installed")
  suppressMessages(library(STAVE))

  # study.yaml is a single record -> a one-row data.frame (NULL -> NA).
  study_list <- yaml::read_yaml(args[1])
  study_cols <- c("study_id", "study_label", "description", "access_level",
                  "contributors", "reference", "reference_year", "PMID")
  study <- as.data.frame(
    lapply(study_cols, function(k) { v <- study_list[[k]]; if (is.null(v)) NA else v }),
    stringsAsFactors = FALSE)
  names(study) <- study_cols

  surveys <- read.csv(args[2], stringsAsFactors = FALSE, na.strings = c("", "NA"))
  counts  <- read.csv(args[3], stringsAsFactors = FALSE, na.strings = c("", "NA"))

  # Type coercions STAVE expects.
  for (col in c("collection_start", "collection_end", "collection_day")) {
    if (col %in% names(surveys)) surveys[[col]] <- as.Date(surveys[[col]])
  }
  surveys$latitude   <- as.numeric(surveys$latitude)
  surveys$longitude  <- as.numeric(surveys$longitude)
  counts$variant_num <- as.integer(counts$variant_num)
  counts$total_num   <- as.integer(counts$total_num)

  obj <- STAVE_object$new()
  obj$append_data(studies_dataframe = study,
                  surveys_dataframe = surveys,
                  counts_dataframe  = counts)
  "OK"
}, error = function(e) paste0("STAVE_ERROR: ", conditionMessage(e)))

cat(result, "\n", sep = "")
