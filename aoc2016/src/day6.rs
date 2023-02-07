use std::collections::HashMap;

pub fn generator(input: &str) -> Vec<String> {
    input.lines().map(|s| s.to_string()).collect()
}

pub fn part_1(input: &[String]) -> String {
    let size = input[0].len();
    let mut bins: Vec<HashMap<_, _>> = Vec::new();

    for _ in 0..size {
        bins.push(HashMap::<char, usize>::new());
    }

    for line in input {
        for (i, c) in line.chars().enumerate() {
            *bins[i].entry(c).or_default() += 1;
        }
    }

    bins.iter()
        .map(|bin| bin.iter().max_by_key(|item| item.1).unwrap())
        .map(|item| item.0)
        .collect()
}

pub fn part_2(input: &[String]) -> String {
    let size = input[0].len();
    let mut bins: Vec<HashMap<_, _>> = Vec::new();

    for _ in 0..size {
        bins.push(HashMap::<char, usize>::new());
    }

    for line in input {
        for (i, c) in line.chars().enumerate() {
            *bins[i].entry(c).or_default() += 1;
        }
    }

    bins.iter()
        .map(|bin| bin.iter().min_by_key(|item| item.1).unwrap())
        .map(|item| item.0)
        .collect()
}
