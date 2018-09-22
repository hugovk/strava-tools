# First: install the packages
# $ R
# install.packages(c("devtools", "mapproj", "tidyverse"))
# devtools::install_github("marcusvolz/strava")
# Or:
# devtools::install_github("marcusvolz/strava", ref="4b15bef416955415759361ac10e227ca07c3fde6")
# Or:
# devtools::install_github("hugovk/strava", ref="no-ele")

# Then run this script like: Rscript stravaviz.R

# Load the libraries
library(strava)
library(tidyverse)

print('Process the data')
data <- process_data("activities")

print('Plot activities as small multiples')
p1 <- plot_facets(data)
ggsave("plots/facets-all.png", p1, width = 20, height = 20, units = "cm")

print('Plot activity map')

# p2 <- plot_map(data, lon_min = 24.8312, lon_max = 25.2022, lat_min = 60.1301, lat_max = 60.2893) # Helsinki
# p2 <- plot_map(data, lon_min = 24.4993, lon_max = 25.2022, lat_min = 60.1301, lat_max = 60.2893) # Helsinki but Espoo's lon_min
# p2 <- plot_map(data, lon_min = 24.4993, lon_max = 25.2545, lat_min = 59.9011, lat_max = 60.3639) # Helsinki/Espoo
# p2 <- plot_map(data, lon_min = 24.4993, lon_max = 25.2545, lat_min = 59.9011, lat_max = 60.401375) # Helsinki/Espoo/Vantaa
p2 <- plot_map(data, lon_min = 22.65, lon_max = 26.65, lat_min = 59.61, lat_max = 60.84) # Uusimaa

ggsave("plots/map-all.png", p2, width = 20, height = 15, units = "cm", dpi = 600)

print('Plot elevation profiles')
p3 <- plot_elevations(data)
ggsave("plots/elevations-all.png", p3, width = 20, height = 20, units = "cm")
