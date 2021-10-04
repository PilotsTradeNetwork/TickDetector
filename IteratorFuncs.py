import threading


# 5 min interval update thread
#   iterate over system list
#       remove entries marked for deletion
#       execute iteration step on each entry