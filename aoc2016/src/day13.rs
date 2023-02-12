use sorted_vec::ReverseSortedVec;
use std::cmp::{Ordering, Reverse};
use std::collections::{HashMap, HashSet};

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
struct Loc<const TX: usize, const TY: usize> {
    x: usize,
    y: usize,
}

impl<const TX: usize, const TY: usize> Loc<TX, TY> {
    fn dist(&self) -> usize {
        self.x.abs_diff(TX) + self.y.abs_diff(TY)
    }

    fn is_wall(&self, seed: usize) -> bool {
        let n =
            self.x * self.x + 3 * self.x + 2 * self.x * self.y + self.y + self.y * self.y + seed;
        n.count_ones() % 2 == 1
    }

    fn left(&self) -> Option<Loc<TX, TY>> {
        if self.x == 0 {
            None
        } else {
            Some(Loc {
                x: self.x - 1,
                y: self.y,
            })
        }
    }

    fn right(&self) -> Option<Loc<TX, TY>> {
        if self.x == TX {
            None
        } else {
            Some(Loc {
                x: self.x + 1,
                y: self.y,
            })
        }
    }

    fn up(&self) -> Option<Loc<TX, TY>> {
        if self.y == 0 {
            None
        } else {
            Some(Loc {
                x: self.x,
                y: self.y - 1,
            })
        }
    }

    fn down(&self) -> Option<Loc<TX, TY>> {
        if self.y == TY {
            None
        } else {
            Some(Loc {
                x: self.x,
                y: self.y + 1,
            })
        }
    }

    fn neighbors(&self, seed: usize) -> Vec<Loc<TX, TY>> {
        let mut neighbors = Vec::new();
        if let Some(l) = self.left() {
            if !l.is_wall(seed) {
                neighbors.push(l);
            }
        }
        if let Some(r) = self.right() {
            if !r.is_wall(seed) {
                neighbors.push(r);
            }
        }
        if let Some(u) = self.up() {
            if !u.is_wall(seed) {
                neighbors.push(u);
            }
        }
        if let Some(d) = self.down() {
            if !d.is_wall(seed) {
                neighbors.push(d);
            }
        }
        neighbors
    }
}

impl<const TX: usize, const TY: usize> PartialOrd<Self> for Loc<TX, TY> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        self.dist().partial_cmp(&other.dist())
    }
}

impl<const TX: usize, const TY: usize> Ord for Loc<TX, TY> {
    fn cmp(&self, other: &Self) -> Ordering {
        self.dist().cmp(&other.dist())
    }
}

fn a_star<const TX: usize, const TY: usize>(start: Loc<TX, TY>, seed: usize) -> usize {
    let mut boundary: ReverseSortedVec<Loc<TX, TY>> = ReverseSortedVec::new();
    let mut visited: HashMap<Loc<TX, TY>, usize> = HashMap::new();

    let dest = Loc { x: TX, y: TY };
    boundary.push(Reverse(start));
    visited.insert(start, 0);

    while !boundary.is_empty() {
        let current = boundary.pop().unwrap().0;
        let current_dist = visited[&current];

        if current == dest {
            return current_dist;
        }

        let neighbors = current.neighbors(seed);
        for neighbor in neighbors {
            let new_dist = current_dist + 1;
            if !visited.contains_key(&neighbor) || new_dist < visited[&neighbor] {
                visited.insert(neighbor, new_dist);
                boundary.push(Reverse(neighbor));
            }
        }
    }

    unreachable!();
}

pub fn part_1(input: &str) -> usize {
    let start = Loc::<1, 1> { x: 31, y: 39 };
    let seed = input.parse().unwrap();
    a_star(start, seed)
}

// "dont care" point
type Point = Loc<0, 0>;

fn reachable_area(start: Point, seed: usize, max_step: usize) -> usize {
    let mut visited: HashSet<Point> = HashSet::new();
    let mut boundary: Vec<Point> = vec![start];

    visited.insert(start);

    let mut step = 0;

    while step < max_step {
        step += 1;
        let mut new_boundary = Vec::new();

        for loc in boundary {
            for neighbor in loc.neighbors(seed) {
                if !visited.contains(&neighbor) {
                    visited.insert(neighbor);
                    new_boundary.push(neighbor);
                }
            }
        }

        boundary = new_boundary;
    }

    visited.len()
}

pub fn part_2(input: &str) -> usize {
    let seed = input.parse().unwrap();
    reachable_area(Point { x: 1, y: 1 }, seed, 50)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let start = Loc::<1, 1> { x: 7, y: 4 };
        let seed = 10;
        assert_eq!(a_star(start, seed), 11);
    }

    #[test]
    fn test_reachable_area() {
        let start = Point { x: 1, y: 1 };
        let seed = 10;
        assert_eq!(reachable_area(start, seed, 0), 1);
        assert_eq!(reachable_area(start, seed, 1), 3);
    }
}
