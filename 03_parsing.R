library(tidyverse)
library(rvest)
library(here)

parse_table <- function(node) {
  
  # scraping table ----------------------------------------------------------
  
  # structure without well defined css classes:
  # <table><tr><td> <a href="link_to_doc"></a> </td></tr><tr> text <td></td></tr></table>
  # problem: 
  # rvest::html_table() catches just html_text(), but the links are stored in href-attribute
  # solution: 
  # xml-parser that loops over <tr>-child-nodes (=td), in order to get links to documents
  #
  # fortlaufende nummer für row, um reihenfolge zu speichern
  
  map_df(1:length(node), function(i) {
    
    # get data of left column in table 
    left_col <- xml_children(node[[i]])[1] %>% xml_find_all(., "a") 
    # check if content and get link
    if(length(left_col) > 0) {
      left_col <- xml_attr(left_col, "href")
    } else {
      left_col = NA
    }
    # get data of right column in table 
    right_col <- xml_children(node[[i]])[2] %>%  xml_text(.) %>% trimws()
    
    tibble(link = left_col, raw_text=right_col, seq = i)
  })
}


# load html pages ---------------------------------------------------------
dir <- here::here("input", "html", "beratungsstand")
files <- list.files(dir)
 


df <- map_df(files, function(file) {
  page <- file.path(dir, file) %>% read_html(encoding = "utf-8")
  parse_table(html_nodes(page, "tr")) %>%
    mutate(id = str_remove(file, ".html"))
})



# Extract meta data -------------------------------------------------------

regex_date <- "[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}"
regex_drucksache <- "[0-9]{2}\\/[0-9]{1,6}"


## besser: durch URL suchen
land <- c("Baden-Württemberg", 
          "Bayern", 
          "Berlin",
          "Bremen",
          "Brandenburg",
          "Hamburg",
          "Hessen",
          "Mecklenburg-Vorpommern",
          "Nordrhein-Westfalen",
          "Niedersachsen",
          "Rheinland-Pfalz",
          "Saarland",
          "Sachsen", 
          "Sachsen-Anhalt",
          "Schleswig-Holstein",
          "Thüringen")

partei <- c("AfD",
            "CDU",
            "CSU",
            "Bündnis 90\\/Die Grünen",
            "ie Grünen",
            "90\\/GRÜNE",
            "90\\/Grüne",
            "FDP",
            "Freie Wähler",
            "FW",
            "Die Linke",
            "Linke",
            "Linkspartei",
            "Piraten",
            "SPD",
            "SSW",
            "SSV")

type <- c("Schriftliche Anfrage",
          "Mündliche Anfrage",
          "Antrag",
          "Antwort",
          "Bericht",
          "Beschlussempfehlung",
          "Debatte",
          "Gesetzgebung",
          "Rechtsverordnung",
          "Verordnung",
          "Vorschrift",
          "Verwaltungsvorschrift",
          "Richtlinie",
          "Wahl",
          "Bestellung",
          "Nachfrage",
          "Protokoll",
          "Ausschussprotokoll",
          "Beschluss des Plenums",
          "Beratungsphase",
          "Aktuelle Stunde",
          "Anfrage",
          "Haushaltsplan",
          "Öffentlicher Haushalt",
          "Entschließungsantrag",
          "Erste Beratung",
          "Plenarprotokoll",
          "Unterrichtung",
          "Einsetzung einer Enquetekommission",
          "Änderungsantrag")
# get data with regex -----------------------------------------------------


lookup_laender <- read_csv(here::here("input", "lookup_laender_ps.csv"))

df <- df %>% mutate(date = str_extract(raw_text, regex_date),
                    drucksache = str_extract(raw_text, regex_drucksache),
                    # todo: fall, wenn NA --> aus anderer row übernehmen - am besten da, wo auch eine Drucksache drin ist?
                    #land = str_extract(raw_text, paste(land, collapse = "|")),
                    
                    partei = str_extract(raw_text, paste(partei, collapse = "|")),
                    type = str_extract(raw_text, paste(type, collapse = "|")),
                    
                    # educated guess whats the title and desc, and drucksachen
                    meta = ifelse(is.na(date) & seq == 1, "title", 
                                  ifelse(is.na(date) & seq == 2, "desc", "drucksache")),
                    # ps_id = parlamentsspiegel_id
                    ps_id = str_remove(str_extract(id, "[A-Z]+_"), "_")
                    ) %>%
  left_join(lookup_laender, by = "ps_id")


write_tsv(df, here::here("input", "data", "df.csv"))
