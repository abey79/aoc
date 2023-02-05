use itertools::Itertools;

pub fn generator(input: &str) -> Vec<i64> {
    input
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect()
}

pub fn part_1(input: &[i64]) -> i64 {
    let mut cnt = 0;
    for i in 0..input.len() / 3 {
        let a = input[i * 3];
        let b = input[i * 3 + 1];
        let c = input[i * 3 + 2];

        if (a + b > c) && (a + c > b) && (b + c > a) {
            cnt += 1;
        }
    }

    cnt
}

pub fn part_2(input: &[i64]) -> i64 {
    let mut cnt = 0;

    for off in 0..3 {
        for i in 0..input.len() / 9 {
            let a = input[i * 9 + off];
            let b = input[i * 9 + 3 + off];
            let c = input[i * 9 + 6 + off];

            if (a + b > c) && (a + c > b) && (b + c > a) {
                cnt += 1;
            }
        }
    }

    cnt
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input = generator("5 10 25");
        assert_eq!(part_1(&input), 0);
    }
}
