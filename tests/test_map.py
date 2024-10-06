from map import Map
from logger import Logger
logger = Logger()
main_map = Map(10, 10, logger)
main_map.generate_map()

main_map.print_map()
