import numpy as np


class KMeansClustering:

    def _find_closest_centroids(self, x, centroids):
        idx = np.zeros(x.shape[0], dtype=int)
        for i in range(x.shape[0]):
            distance = []
            for j in range(centroids.shape[0]):
                norm_ij = np.linalg.norm(x[i] - centroids[j])
                distance.append(norm_ij)
            idx[i] = np.argmin(distance)
        return idx

    def _compute_centroids(self, x, idx, k):
        m, n = x.shape
        centroids = np.zeros((k, n))
        for k in range(k):
            points = x[idx == k]
            centroids[k] = np.mean(points, axis=0)
        return centroids

    def run_kmeans(self, x, initial_centroids, max_iters=10):
        m, n = x.shape
        K = initial_centroids.shape[0]
        centroids = initial_centroids
        idx = np.zeros(m)
        for i in range(max_iters):
            print("K-Means iteration %d/%d" % (i, max_iters - 1))
            idx = self._find_closest_centroids(x, centroids)
            centroids = self._compute_centroids(x, idx, K)
        return centroids, idx

    def kmeans_init_centroids(self, x, k):
        randidx = np.random.permutation(x.shape[0])
        centroids = x[randidx[:k]]
        return centroids
