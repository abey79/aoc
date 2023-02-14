use sorted_vec::SortedVec;
use std::cmp::Ordering;
use std::collections::{HashMap, VecDeque};

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
struct Loc {
    x: usize,
    y: usize,
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct State {
    loc: Loc,
    path: String,
}

impl State {
    fn new(x: usize, y: usize, path: &str) -> State {
        State {
            loc: Loc { x, y },
            path: path.to_string(),
        }
    }
    fn neighbors(&self) -> Vec<State> {
        let mut neighbors = Vec::new();

        let hash = format!("{:x}", md5::compute(self.path.as_bytes()));
        let door_open: Vec<_> = hash
            .chars()
            .take(4)
            .map(|c| c == 'b' || c == 'c' || c == 'd' || c == 'e' || c == 'f')
            .collect();

        for dir in &["U", "D", "L", "R"] {
            let (dx, dy) = match *dir {
                "U" => {
                    if self.loc.y == 0 || !door_open[0] {
                        continue;
                    } else {
                        (0, -1)
                    }
                }

                "D" => {
                    if self.loc.y == 3 || !door_open[1] {
                        continue;
                    } else {
                        (0, 1)
                    }
                }

                "L" => {
                    if self.loc.x == 0 || !door_open[2] {
                        continue;
                    } else {
                        (-1, 0)
                    }
                }

                "R" => {
                    if self.loc.x == 3 || !door_open[3] {
                        continue;
                    } else {
                        (1, 0)
                    }
                }

                _ => unreachable!(),
            };

            neighbors.push(State::new(
                (self.loc.x as isize + dx) as usize,
                (self.loc.y as isize + dy) as usize,
                (self.path.to_string() + dir).as_str(), // the String/str dance is not ideal here
            ));
        }

        neighbors
    }

    fn dist_to_origin(&self) -> usize {
        self.loc.x + self.loc.y
    }
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        // To use SortedVec, we want the lower cost to have the highest value, so it's at the end.

        // First, we prioritize the path with the fewest steps.
        other.path.len().cmp(&self.path.len()).then_with(|| {
            // If the paths are the same length, we prioritize the path that's further from the
            // origin.
            self.dist_to_origin().cmp(&other.dist_to_origin())
        })
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn a_star(start: State) -> Result<String, &'static str> {
    let mut boundary: SortedVec<_> = SortedVec::new();
    let mut visited: HashMap<State, String> = HashMap::new();

    visited.insert(start.clone(), start.path.clone());
    boundary.push(start);

    let goal = Loc { x: 3, y: 3 };

    while !boundary.is_empty() {
        let current = boundary.pop().unwrap();

        if current.loc == goal {
            return Ok(current.path);
        }

        let neighbors = current.neighbors();
        for new_state in neighbors {
            if !visited.contains_key(&new_state) || new_state.path.len() < current.path.len() {
                visited.insert(new_state.clone(), new_state.path.clone());
                boundary.push(new_state);
            }
        }
    }

    Err("No path found")
}

pub fn part_1(input: &str) -> String {
    a_star(State {
        loc: Loc { x: 0, y: 0 },
        path: input.to_string(),
    })
    .unwrap_or("not found".to_string())
}

fn a_star_rev(start: State) -> Result<String, &'static str> {
    // here we use djikstra instead of a*, so a deque works better
    let mut boundary = VecDeque::new();
    let mut visited: HashMap<State, String> = HashMap::new();

    visited.insert(start.clone(), start.path.clone());
    boundary.push_back(start);

    let goal = Loc { x: 3, y: 3 };

    while !boundary.is_empty() {
        // finish *only* if we dont have the choice
        if boundary.iter().all(|s| s.loc == goal) {
            return Ok(boundary
                .iter()
                .max_by_key(|s| s.path.len())
                .unwrap()
                .path
                .clone());
        }

        // avoid going to the goal if we have a choice
        let mut current = boundary.pop_front().unwrap();
        while current.loc == goal {
            boundary.push_back(current);
            current = boundary.pop_front().unwrap();
        }

        let neighbors = current.neighbors();
        for new_state in neighbors {
            if !visited.contains_key(&new_state) || new_state.path.len() > current.path.len() {
                visited.insert(new_state.clone(), new_state.path.clone());
                boundary.push_back(new_state);
            }
        }
    }

    Err("No path found")
}

pub fn part_2(input: &str) -> usize {
    a_star_rev(State {
        loc: Loc { x: 0, y: 0 },
        path: input.to_string(),
    })
    .unwrap_or("not found".to_string())
    .len()
        - input.len()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_neighbors() {
        let state = State::new(0, 0, "hijkl");
        let neighbors = state.neighbors();
        assert_eq!(neighbors, [State::new(0, 1, "hijklD")]);
    }

    #[test]
    fn test_a_star() {
        let path = a_star(State::new(0, 0, "ihgpwlah"));
        assert_eq!(path, Ok("ihgpwlahDDRRRD".to_string()));

        let path = a_star(State::new(0, 0, "hijkl"));
        assert_eq!(path, Err("No path found"));

        let path = a_star(State::new(0, 0, "kglvqrro"));
        assert_eq!(path, Ok("kglvqrroDDUDRLRRUDRD".to_string()));

        let path = a_star(State::new(0, 0, "ulqzkmiv"));
        assert_eq!(
            path,
            Ok("ulqzkmivDRURDRUDDLLDLUURRDULRLDUUDDDRR".to_string())
        );
    }

    #[test]
    fn test_a_star_rev() {
        let path = a_star_rev(State::new(0, 0, "ihgpwlah"));
        assert_eq!(path.unwrap().len() - 8, 370);

        let path = a_star_rev(State::new(0, 0, "ulqzkmiv"));
        assert_eq!(path.unwrap().len() - 8, 830);
    }
}
