use itertools::Itertools;

fn next_row(row: &str) -> String {
    ['.']
        .into_iter()
        .chain(row.chars())
        .chain(['.'].into_iter())
        .tuple_windows()
        .map(|(a, _, b)| if a == b { '.' } else { '^' })
        .collect()
}

fn count_safe_tiles(row: &str) -> usize {
    row.chars().filter(|c| *c == '.').count()
}

fn count_all_safe_tiles(row: &str, n: usize) -> usize {
    let mut row = row.to_string();
    let mut cnt = count_safe_tiles(&row);
    for _ in 0..n - 1 {
        row = next_row(&row);
        cnt += count_safe_tiles(&row);
    }
    cnt
}

pub fn part_1(input: &str) -> usize {
    count_all_safe_tiles(input, 40)
}

pub fn part_2(input: &str) -> usize {
    count_all_safe_tiles(input, 400000)
}
