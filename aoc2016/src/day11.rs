#![allow(dead_code)]

use bit_iter::*;
use itertools::Itertools;
use std::collections::HashSet;
use std::fmt;

// The first floor contains a promethium generator and a promethium-compatible microchip.
// The second floor contains a cobalt generator, a curium generator, a ruthenium generator, and a plutonium generator.
// The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, a ruthenium-compatible microchip, and a plutonium-compatible microchip.
// The fourth floor contains nothing relevant.

#[derive(Debug, Hash, Clone, Copy, PartialEq, Eq)]
enum Floor {
    First,
    Second,
    Third,
    Fourth,
}

impl Floor {
    fn from_index(index: usize) -> Self {
        match index {
            0 => Floor::First,
            1 => Floor::Second,
            2 => Floor::Third,
            3 => Floor::Fourth,
            _ => panic!("invalid floor index"),
        }
    }

    fn possible_moves(&self) -> Vec<Floor> {
        match self {
            Floor::First => vec![Floor::Second],
            Floor::Second => vec![Floor::First, Floor::Third],
            Floor::Third => vec![Floor::Second, Floor::Fourth],
            Floor::Fourth => vec![Floor::Third],
        }
    }

    fn index(&self) -> usize {
        match self {
            Floor::First => 0,
            Floor::Second => 1,
            Floor::Third => 2,
            Floor::Fourth => 3,
        }
    }
}

// first byte encode for microchip presence, second byte encodes for generator presence
#[derive(Hash, Clone, Copy, PartialEq, Eq)]
struct FloorState(u8, u8);

impl FloorState {
    fn add_microchip(self, microchip: u8) -> Self {
        FloorState(self.0 | 1 << microchip, self.1)
    }

    fn add_generator(self, generator: u8) -> Self {
        FloorState(self.0, self.1 | 1 << generator)
    }

    fn remove_microchip(self, microchip: u8) -> Self {
        FloorState(self.0 & !(1 << microchip), self.1)
    }

    fn remove_generator(self, generator: u8) -> Self {
        FloorState(self.0, self.1 & !(1 << generator))
    }

    fn has_microchip(self, microchip: u8) -> bool {
        (self.0 & (1 << microchip)) != 0
    }

    fn has_generator(self, generator: u8) -> bool {
        (self.1 & (1 << generator)) != 0
    }

    fn is_consistent(&self) -> bool {
        // chip may not at be at the same floor as a generator unless it with its own

        // test for "alone" chips
        if (self.0 & !self.1) != 0 {
            // then there should be no generator
            if self.1 != 0 {
                return false;
            }
        }

        true
    }
}

impl fmt::Debug for FloorState {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "M")?;
        BitIter::from(self.0)
            .rev()
            .for_each(|i| write!(f, "{i}").unwrap());

        write!(f, "|G")?;
        BitIter::from(self.1)
            .rev()
            .for_each(|i| write!(f, "{i}").unwrap());

        Ok(())
    }
}

#[derive(Hash, Clone, Copy, PartialEq, Eq)]
struct State<const N: u8 = 5> {
    elevator: Floor,
    floors: [FloorState; 4],
}

impl<const N: u8> fmt::Debug for State<N> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let elev = self.elevator.index();
        write!(f, "E{elev}")?;
        write!(f, "|M")?;
        for i in 0..N {
            let fl = self.floor_from_microchip(i);
            write!(f, "{fl}")?;
        }

        write!(f, "|G")?;
        for i in 0..N {
            let fl = self.floor_from_generator(i);
            write!(f, "{fl}")?;
        }

        Ok(())
    }
}

type Digest = (Floor, [(u8, u8); 4]);

impl<const N: u8> State<N> {
    fn floor_from_microchip(&self, microchip: u8) -> usize {
        for (i, floor) in self.floors.iter().enumerate() {
            if floor.has_microchip(microchip) {
                return i;
            }
        }
        unreachable!("microchip not found");
    }

    fn floor_from_generator(&self, generator: u8) -> usize {
        for (i, floor) in self.floors.iter().enumerate() {
            if floor.has_generator(generator) {
                return i;
            }
        }
        unreachable!("microchip not found");
    }

    fn is_consistent(&self) -> bool {
        for floor in &self.floors {
            if !floor.is_consistent() {
                return false;
            }
        }

        // test that no two floors have the same microchip and generator
        #[cfg(debug_assertions)]
        for (i, f1) in self.floors.iter().enumerate() {
            for f2 in self.floors[i + 1..].iter() {
                assert_eq!(f1.0 & f2.0, 0);
                assert_eq!(f1.1 & f2.1, 0);
            }
        }

        true
    }

    fn digest(&self) -> Digest {
        // the key insight is that we dont need to know *which* type of pair is on floors, we can
        // just count them
        // saving digests instead of states reduces the state space so much that it cuts down part_2
        // from ~22s to ~42ms.
        let mut digest: Digest = (self.elevator, [(0u8, 0u8); 4]);

        for (i, floor) in self.floors.iter().enumerate() {
            digest.1[i].0 = floor.0.count_ones() as u8;
            digest.1[i].1 = floor.1.count_ones() as u8;
        }

        digest
    }

    fn possible_moves(&self) -> Vec<Self> {
        // at each step, one can move the elevator up or down by one floor
        // the elevator may contain either a chip or a generator, or both of the same type
        // the departure floor must be consistent after elevator departs
        // the destination floor must be consistent after elevator arrives
        //
        // pseudo code:
        // for each item in source floor
        //   if item may not be moved from source floor
        //     continue
        //
        //   for each possible destination floor
        //     if item may not be moved to destination floor
        //       continue
        //
        //     save move
        //
        // for each

        let mut moves = vec![];

        let source_floor = self.floors[self.elevator.index()];
        let dest_floors_idx = self.elevator.possible_moves();

        // possibly things to move
        let possible_moves: Vec<(Vec<u8>, Vec<u8>)> = (0..N)
            .map(|a| (vec![a], vec![]))
            .chain((0..N).map(|a| (vec![], vec![a])))
            .chain((0..N).map(|a| (vec![a], vec![a])))
            .chain((0..N).combinations(2).map(|a| (a, vec![])))
            .chain((0..N).combinations(2).map(|a| (vec![], a)))
            .collect();

        for (microchips, generators) in possible_moves {
            // check that all items may be moved from source floor
            if !microchips.iter().all(|m| source_floor.has_microchip(*m)) {
                continue;
            }
            if !generators.iter().all(|g| source_floor.has_generator(*g)) {
                continue;
            }

            // remove items from the source floor
            let mut new_source_floor = source_floor;
            for microchip in microchips.iter() {
                new_source_floor = new_source_floor.remove_microchip(*microchip);
            }
            for generator in generators.iter() {
                new_source_floor = new_source_floor.remove_generator(*generator);
            }

            // check that the source floor is consistent
            if !new_source_floor.is_consistent() {
                continue;
            }

            for dest_floor_idx in dest_floors_idx.iter() {
                let dest_floor = self.floors[*dest_floor_idx as usize];
                let mut new_dest_floor = dest_floor;
                for microchip in microchips.iter() {
                    new_dest_floor = new_dest_floor.add_microchip(*microchip);
                }
                for generator in generators.iter() {
                    new_dest_floor = new_dest_floor.add_generator(*generator);
                }
                if !new_dest_floor.is_consistent() {
                    continue;
                }

                // valid move, save corresponding state
                let mut new_state = *self;
                new_state.floors[self.elevator.index()] = new_source_floor;
                new_state.floors[dest_floor_idx.index()] = new_dest_floor;
                new_state.elevator = *dest_floor_idx;

                moves.push(new_state);
            }
        }

        moves
    }
}

const INITIAL_STATE: State = State {
    elevator: Floor::First,
    floors: [
        FloorState(0b00001, 0b00001),
        FloorState(0b00000, 0b11110),
        FloorState(0b11110, 0b00000),
        FloorState(0b00000, 0b00000),
    ],
};

const FINAL_STATE: State = State {
    elevator: Floor::Fourth,
    floors: [
        FloorState(0b00000, 0b00000),
        FloorState(0b00000, 0b00000),
        FloorState(0b00000, 0b00000),
        FloorState(0b11111, 0b11111),
    ],
};

const INITIAL_STATE_PART2: State<7> = State {
    elevator: Floor::First,
    floors: [
        FloorState(0b1100001, 0b1100001),
        FloorState(0b0000000, 0b0011110),
        FloorState(0b0011110, 0b0000000),
        FloorState(0b0000000, 0b0000000),
    ],
};

const FINAL_STATE_PART2: State<7> = State {
    elevator: Floor::Fourth,
    floors: [
        FloorState(0b0000000, 0b0000000),
        FloorState(0b0000000, 0b0000000),
        FloorState(0b0000000, 0b0000000),
        FloorState(0b1111111, 0b1111111),
    ],
};

fn count_steps<const N: u8>(initial_state: &State<N>, final_state: &State<N>) -> i64 {
    let mut moves = vec![*initial_state];
    let mut visited = HashSet::new();
    visited.insert(initial_state.digest());

    let mut steps = 0;

    loop {
        let mut new_moves = vec![];

        if moves.is_empty() {
            println!("No more moves to consider");
            return 0;
        }

        for state in moves {
            //println!("Considering state {state:?}");
            if state == *final_state {
                return steps;
            }

            let possible_moves = state.possible_moves();
            //println!("  Considering {} possible moves", possible_moves.len());
            for new_state in possible_moves {
                if !visited.contains(&new_state.digest()) {
                    //println!("  Found new state {new_state:?}");
                    visited.insert(new_state.digest());
                    new_moves.push(new_state);
                }
            }
        }

        moves = new_moves;
        steps += 1;

        // println!(
        //     "Step {steps}: considering {} moves, visited {} states",
        //     moves.len(),
        //     visited.len()
        // );
    }
}

pub fn part_1(_input: &str) -> i64 {
    count_steps(&INITIAL_STATE, &FINAL_STATE)
}

pub fn part_2(_input: &str) -> i64 {
    count_steps(&INITIAL_STATE_PART2, &FINAL_STATE_PART2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let initial_state: State<2> = State {
            elevator: Floor::First,
            floors: [
                FloorState(0b11, 0b00),
                FloorState(0b00, 0b10),
                FloorState(0b00, 0b01),
                FloorState(0b00, 0b00),
            ],
        };

        let final_state: State<2> = State {
            elevator: Floor::Fourth,
            floors: [
                FloorState(0b00, 0b00),
                FloorState(0b00, 0b00),
                FloorState(0b00, 0b00),
                FloorState(0b11, 0b11),
            ],
        };

        assert_eq!(count_steps(&initial_state, &final_state), 11);
    }
}
