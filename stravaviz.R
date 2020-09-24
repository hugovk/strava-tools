# First: install the packages
# $ R
# install.packages(c("devtools", "gtools", "mapproj", "tidyverse"))
# devtools::install_github("marcusvolz/strava")
# Or:
# devtools::install_github("marcusvolz/strava", ref="4b15bef416955415759361ac10e227ca07c3fde6")
# Or:
# devtools::install_github("hugovk/strava", ref="no-ele")
# Or:
# install.packages("/Users/hugo/github/strava", repos = NULL, type="source")

# Then run this script like: Rscript stravaviz.R

# Load the libraries
library(gtools)
library(strava)
library(tidyverse)

print('Process the data')
data <- process_data("activities")

print('Plot activities as small multiples')
p1 <- plot_facets(data)
ggsave("plots/facets-all.png", p1, width = 20, height = 20, units = "cm")

print('Plot activity map')

p2_hki <- plot_map(data, lon_min = 24.807278, lon_max = 25.087382, lat_min = 60.144413, lat_max = 60.221064) # Helsinki centre
p2_h <- plot_map(data, lon_min = 24.8312, lon_max = 25.2022, lat_min = 60.1301, lat_max = 60.2893) # Helsinki
p2_h2 <- plot_map(data, lon_min = 24.4993, lon_max = 25.2022, lat_min = 60.1301, lat_max = 60.2893) # Helsinki but Espoo's lon_min
p2_he <- plot_map(data, lon_min = 24.4993, lon_max = 25.2545, lat_min = 59.9011, lat_max = 60.3639) # Helsinki/Espoo
p2_hev <- plot_map(data, lon_min = 24.4993, lon_max = 25.2545, lat_min = 59.9011, lat_max = 60.401375) # Helsinki/Espoo/Vantaa
p2 <- plot_map(data, lon_min = 22.65, lon_max = 26.65, lat_min = 59.61, lat_max = 60.84) # Uusimaa

ggsave("plots/map-all-hki.png", p2_hki, width = 20, height = 15, units = "cm", dpi = 600)
ggsave("plots/map-all-helsinki.png", p2_h, width = 20, height = 15, units = "cm", dpi = 600)
ggsave("plots/map-all-helsinki2.png", p2_h2, width = 20, height = 15, units = "cm", dpi = 600)
ggsave("plots/map-all-helsinki-espoo.png", p2_he, width = 20, height = 15, units = "cm", dpi = 600)
ggsave("plots/map-all-helsinki-espoo-vantaa.png", p2_hev, width = 20, height = 15, units = "cm", dpi = 600)
ggsave("plots/map-all-uusimaa.png", p2, width = 20, height = 15, units = "cm", dpi = 600)


print('Plot elevation profiles')
p3 <- plot_elevations(data)
ggsave("plots/elevations-all.png", p3, width = 20, height = 20, units = "cm")
