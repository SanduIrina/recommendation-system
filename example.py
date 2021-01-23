import sys
sys.path.append('collab-filtering/')
from predict import *

# # Example: work with individual songs
# load_data("collab-filtering/data/") # path should point to the data folder located under collab-filtering
# ## update_recommendations(user_id, song_id, rating, mode) -> for individual songs it should be 'song_name'
# ## You can call update_recommendations multiple times and all changes will take effect when you call if with the last parameter set to True. That's when the model is being retrained
# update_recommendations("b80344d063b5ccb3212f76538f3d9e43d87dca9e", 'All My Friends', 10, 'song_name', True)
# # This is how you get recommendations for a user
# print(get_predictions_for_user('b80344d063b5ccb3212f76538f3d9e43d87dca9e', 'song_name'))

# # Example: work with clusters
# load_data("collab-filtering/data/")
# ## update_recommendations(user_id, song_id, rating, mode) -> for clusters mode should be 'cluster_id'
# ## You can call update_recommendations multiple times and all changes will take effect when you call if with the last parameter set to True. That's when the model is being retrained
# update_recommendations("b80344d063b5ccb3212f76538f3d9e43d87dca9e", 'All My Friends', 10, 'cluster_id', True)
# # This is how you get recommendations for a user
# print(get_predictions_for_user('b80344d063b5ccb3212f76538f3d9e43d87dca9e', 'cluster_id'))