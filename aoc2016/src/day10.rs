use itertools::Itertools;
use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;

#[derive(Debug, Clone, Copy)]
pub enum Destination {
    Bot(usize),
    Output(usize),
}

impl Destination {
    fn from_str(s: &str) -> Self {
        let parts = s.split(' ').collect::<Vec<&str>>();
        match parts[0] {
            "bot" => Destination::Bot(parts[1].parse().unwrap()),
            "output" => Destination::Output(parts[1].parse().unwrap()),
            _ => panic!("Unknown destination"),
        }
    }
}

pub enum Instruction {
    Value(usize, usize),
    Give(usize, Destination, Destination),
}

lazy_static! {
    static ref VALUE_RE: Regex = Regex::new(r"^value (\d+) goes to bot (\d+)$").unwrap();
    static ref GIVE_RE: Regex =
        Regex::new(r"^bot (\d+) gives low to (\w+ \d+) and high to (\w+ \d+)$").unwrap();
}

impl Instruction {
    fn from_str(s: &str) -> Self {
        if let Some(caps) = VALUE_RE.captures(s) {
            Instruction::Value(caps[1].parse().unwrap(), caps[2].parse().unwrap())
        } else if let Some(caps) = GIVE_RE.captures(s) {
            Instruction::Give(
                caps[1].parse().unwrap(),
                Destination::from_str(&caps[2]),
                Destination::from_str(&caps[3]),
            )
        } else {
            panic!("Unknown instruction");
        }
    }
}

pub fn generator(input: &str) -> Vec<Instruction> {
    input.lines().map(Instruction::from_str).collect()
}

pub fn part_1(input: &[Instruction]) -> usize {
    let mut bots: HashMap<usize, Vec<usize>> = HashMap::new();
    let mut give_instructions: HashMap<usize, (Destination, Destination)> = HashMap::new();
    let mut outputs: HashMap<usize, usize> = HashMap::new();

    input.iter().for_each(|i| match i {
        Instruction::Value(value, bot_id) => {
            bots.entry(*bot_id).or_insert(vec![]).push(*value);
        }
        Instruction::Give(bot_id, low, high) => {
            give_instructions.insert(*bot_id, (*low, *high));
        }
    });

    loop {
        let (&bot_id, values) = bots.iter().find(|(_k, v)| v.len() == 2).unwrap();
        let (&low, &high) = values.iter().minmax().into_option().unwrap();

        bots.get_mut(&bot_id).unwrap().clear();

        if low == 17 && high == 61 {
            return bot_id;
        }

        let (low_dest, high_dest) = give_instructions.get(&bot_id).unwrap();

        for (val, dest) in [(low, low_dest), (high, high_dest)] {
            match dest {
                Destination::Bot(id) => {
                    bots.entry(*id).or_insert(vec![]).push(val);
                }
                Destination::Output(id) => {
                    assert!(outputs.get(id).is_none());
                    outputs.insert(*id, val);
                }
            }
        }
    }
}

pub fn part_2(input: &[Instruction]) -> usize {
    let mut bots: HashMap<usize, Vec<usize>> = HashMap::new();
    let mut give_instructions: HashMap<usize, (Destination, Destination)> = HashMap::new();
    let mut outputs: HashMap<usize, usize> = HashMap::new();

    input.iter().for_each(|i| match i {
        Instruction::Value(value, bot_id) => {
            bots.entry(*bot_id).or_insert(vec![]).push(*value);
        }
        Instruction::Give(bot_id, low, high) => {
            give_instructions.insert(*bot_id, (*low, *high));
        }
    });

    loop {
        let (&bot_id, values) = bots.iter().find(|(_k, v)| v.len() == 2).unwrap();
        let (&low, &high) = values.iter().minmax().into_option().unwrap();

        bots.get_mut(&bot_id).unwrap().clear();

        let (low_dest, high_dest) = give_instructions.get(&bot_id).unwrap();

        for (val, dest) in [(low, low_dest), (high, high_dest)] {
            match dest {
                Destination::Bot(id) => {
                    bots.entry(*id).or_insert(vec![]).push(val);
                }
                Destination::Output(id) => {
                    assert!(outputs.get(id).is_none());
                    outputs.insert(*id, val);

                    if let (Some(a), Some(b), Some(c)) =
                        (outputs.get(&0), outputs.get(&1), outputs.get(&2))
                    {
                        return a * b * c;
                    }
                }
            }
        }
    }
}
