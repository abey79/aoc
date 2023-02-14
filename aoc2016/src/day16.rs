// "dumb" solution runs in 88ms, why bother with the optimization? :)

use itertools::Itertools;

pub fn generator(input: &str) -> Vec<bool> {
    input
        .chars()
        .map(|c| match c {
            '0' => false,
            '1' => true,
            _ => panic!("Invalid input"),
        })
        .collect()
}

pub fn solution(input: &[bool], disk_size: usize) -> String {
    let mut data = input.to_vec();

    while data.len() < disk_size {
        let mut new_data = data.clone();
        new_data.reverse();
        new_data = new_data.iter().map(|b| !b).collect();
        data.push(false);
        data.extend(new_data);
    }

    data.truncate(disk_size);
    loop {
        let new_data: Vec<_> = data.chunks(2).map(|chunk| chunk[0] == chunk[1]).collect();

        if new_data.len() % 2 == 1 {
            return new_data.iter().map(|b| if *b { '1' } else { '0' }).join("");
        } else {
            data = new_data;
        }
    }
}

pub fn part_1(input: &[bool]) -> String {
    solution(input, 272)
}

pub fn part_2(input: &[bool]) -> String {
    solution(input, 35651584)
}
