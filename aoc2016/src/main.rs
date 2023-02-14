mod day1;
mod day10;
mod day11;
mod day12;
mod day13;
mod day14;
mod day15;
mod day16;
mod day17;
mod day2;
mod day3;
mod day4;
mod day5;
mod day6;
mod day7;
mod day8;
mod day9;

aoc_main::main! {
    year 2016;
    day1 : generator => part_1, part_2;
    day2 : generator => part_1, part_2;
    day3 : generator => part_1, part_2;
    day4 : generator => part_1, part_2;
    day5 : generator => part_1, part_2, part_2_thread;
    day6 : generator => part_1, part_2;
    day7 : generator => part_1, part_2;
    day8 : generator => part_1, part_2;
    day9 : generator => part_1, part_2;
    day10 : generator => part_1, part_2;
    day11 => part_1, part_2;
    day12 : generator => part_1, part_2;
    day13 => part_1, part_2;
    day14 => part_1, part_2;
    day15 : generator => part_1, part_2;
    day16 : generator => part_1, part_2;
    day17 => part_1, part_2;
}
