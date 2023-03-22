import random
import numpy as np
class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iterations (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, while 0.5 will lead to much faster decay.
            alpha (int or float): exponent on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        Example:
            ant_colony = AntColony(distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone * self.decay            
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path,_ in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1/ self.distances[move]

    def gen_path_dist(self,path):
      total_dist=0
      for ele in path:
          total_dist+=self.distances[ele]
      return total_dist

    def gen_all_paths(self):
      all_paths=[]
      for i in range(self.n_ants):
          path=self.gen_path(0)
          all_paths.append((path,self.gen_path_dist(path)))
      return all_paths

    def gen_path(self,start):
      path=[]
      visited=set()
      visited.add(start)
      prev=start
      for i in range(len(self.distances)-1):
          move=self.pick_move(self.pheromone[prev],self.distances[prev],visited)
          path.append((prev,move))
          prev=move
          visited.add(move)
      path.append((prev,start))
      return path

    def pick_move(self,phe,dist,vistied):
      phe=np.copy(phe)
      phe[list(vistied)]=0

      row=phe**self.alpha * ((1.0/dist)**self.beta)

      norm_row=row/row.sum()
      move=np.random.choice(self.all_inds ,p=norm_row)
      return move


def main():
    distances=np.array([[np.inf ,2 ,2 ,5 ,7],
                        [2 ,np.inf ,4 ,8 ,2],
                        [2 ,4 ,np.inf ,1 ,3],
                        [5 ,8 ,1 ,np.inf ,2],
                        [7 ,2 ,3 ,2,np.inf]])
    
    ant_colony=AntColony(distances,n_ants=10,n_best=3,n_iterations=1000,
                         decay=.95,alpha=1,beta=2)

    shortest_path=ant_colony.run()
    
    print("Shortest Path :{}".format(shortest_path))

if __name__=="__main__":
    main()