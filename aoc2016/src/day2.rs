fn map(digit: i64, dir: char) -> i64 {
    match digit {
        1 => match dir {
            'D' => 4,
            'R' => 2,
            _ => 1,
        },
        2 => match dir {
            'D' => 5,
            'L' => 1,
            'R' => 3,
            _ => 2,
        },
        3 => match dir {
            'D' => 6,
            'L' => 2,
            _ => 3,
        },
        4 => match dir {
            'U' => 1,
            'D' => 7,
            'R' => 5,
            _ => 4,
        },
        5 => match dir {
            'U' => 2,
            'D' => 8,
            'L' => 4,
            'R' => 6,
            _ => unreachable!(),
        },
        6 => match dir {
            'U' => 3,
            'D' => 9,
            'L' => 5,
            _ => 6,
        },
        7 => match dir {
            'U' => 4,
            'R' => 8,
            _ => 7,
        },
        8 => match dir {
            'U' => 5,
            'L' => 7,
            'R' => 9,
            _ => 8,
        },
        9 => match dir {
            'U' => 6,
            'L' => 8,
            _ => 9,
        },
        _ => unreachable!(),
    }
}

fn map2(digit: char, dir: char) -> char {
    match digit {
        '1' => match dir {
            'D' => '3',
            _ => '1',
        },
        '2' => match dir {
            'D' => '6',
            'R' => '3',
            _ => '2',
        },
        '3' => match dir {
            'U' => '1',
            'D' => '7',
            'L' => '2',
            'R' => '4',
            _ => unreachable!(),
        },
        '4' => match dir {
            'D' => '8',
            'L' => '3',
            _ => '4',
        },
        '5' => match dir {
            'R' => '6',
            _ => '5',
        },
        '6' => match dir {
            'U' => '2',
            'D' => 'A',
            'L' => '5',
            'R' => '7',
            _ => unreachable!(),
        },
        '7' => match dir {
            'U' => '3',
            'D' => 'B',
            'L' => '6',
            'R' => '8',
            _ => unreachable!(),
        },
        '8' => match dir {
            'U' => '4',
            'D' => 'C',
            'L' => '7',
            'R' => '9',
            _ => unreachable!(),
        },
        '9' => match dir {
            'L' => '8',
            _ => '9',
        },
        'A' => match dir {
            'U' => '6',
            'R' => 'B',
            _ => 'A',
        },
        'B' => match dir {
            'U' => '7',
            'D' => 'D',
            'L' => 'A',
            'R' => 'C',
            _ => unreachable!(),
        },
        'C' => match dir {
            'U' => '8',
            'L' => 'B',
            _ => 'C',
        },
        'D' => match dir {
            'U' => 'B',
            _ => 'D',
        },
        _ => unreachable!(),
    }
}

pub fn generator(input: &str) -> Vec<String> {
    input.lines().map(|s| s.to_string()).collect()
}

pub fn part_1(input: &[String]) -> String {
    let mut cur = 5;
    let mut result = String::new();
    for line in input {
        for c in line.chars() {
            cur = map(cur, c);
        }
        result.push_str(&cur.to_string());
    }
    result
}

pub fn part_2(input: &[String]) -> String {
    let mut cur = '5';
    let mut result = String::new();
    for line in input {
        for c in line.chars() {
            cur = map2(cur, c);
        }
        result.push(cur)
    }
    result
}
