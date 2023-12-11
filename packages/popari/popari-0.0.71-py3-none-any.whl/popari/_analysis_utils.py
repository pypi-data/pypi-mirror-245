import numpy as np
from multiprocess import Pool

from popari.util import spatial_wasserstein

def _all_pairs_spatial_wasserstein(dataset,
                        spatial_key: str = 'spatial',
                        embeddings_truth_key: str = 'ground_truth_X',
                        embeddings_pred_key: str = 'X',
                        weight_scaling_factor=int(1e4),
                        demand_scaling_factor=int(1e4),
                        num_processes: int = 16):
    """Compute all-pairs spatial Wasserstein distance.

    """
    
    spatial_coordinates = dataset.obsm[spatial_key]
    embeddings_truth = dataset.obsm[embeddings_truth_key]
    embeddings_pred = dataset.obsm[embeddings_pred_key]
    
    metric = lambda pair: spatial_wasserstein(spatial_coordinates, *pair)
    
    num_truth = embeddings_truth.shape[1]
    num_pred = embeddings_pred.shape[1]
            
    pairs = [[(truth, pred) for pred in embeddings_pred.T] for truth in embeddings_truth.T]
    pairs = np.array(pairs).reshape(-1, 2, len(spatial_coordinates))

    with Pool(processes=num_processes) as pool:
        results = pool.map(metric, pairs)
        
    distances = np.array(list(results)).reshape((num_truth, num_pred))
        
    return distances
