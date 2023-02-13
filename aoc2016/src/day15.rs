// arg... yet another occurrence of the chinese remainder theorem that I didn't recognize...

use regex::Regex;

pub fn generator(input: &str) -> Vec<(u64, u64)> {
    let re = Regex::new(r"^Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).$")
        .unwrap();
    input
        .lines()
        .enumerate()
        .map(|(i, s)| {
            let caps = re.captures(s).unwrap();
            let disc = caps.get(1).unwrap().as_str().parse().unwrap();
            let positions = caps.get(2).unwrap().as_str().parse().unwrap();
            let start = caps.get(3).unwrap().as_str().parse().unwrap();
            assert_eq!(i + 1, disc);
            (positions, start)
        })
        .collect()
}

pub fn solution(input: &[(u64, u64)], part2: bool) -> usize {
    let mut pos_count: Vec<_> = input.iter().map(|&(p, _)| p).collect();
    let mut cur_pos: Vec<_> = input.iter().map(|&(_, s)| s).collect();

    if part2 {
        pos_count.push(11);
        cur_pos.push(0);
    }

    let mut time = 0;

    for i in 0..cur_pos.len() {
        cur_pos[i] += (i + 1) as u64;
        cur_pos[i] %= pos_count[i]
    }

    loop {
        if cur_pos.iter().all(|&p| p == 0) {
            return time;
        }

        cur_pos
            .iter_mut()
            .zip(pos_count.iter())
            .for_each(|(p, &c)| {
                *p += 1;
                *p %= c;
            });

        time += 1;
    }
}

pub fn part_1(input: &[(u64, u64)]) -> usize {
    solution(input, false)
}

pub fn part_2(input: &[(u64, u64)]) -> usize {
    solution(input, true)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input = generator(
            "\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.",
        );

        assert_eq!(part_1(&input), 5);
    }
}
