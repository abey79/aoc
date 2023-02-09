use ndarray::prelude::*;

#[derive(Debug)]
pub enum Command {
    Rect(usize, usize),
    RotateRow { row: usize, steps: isize },
    RotateCol { col: usize, steps: isize },
}

impl Command {
    fn from_str(s: &str) -> Self {
        let parts = s.split(' ').collect::<Vec<&str>>();
        match parts[0] {
            "rect" => {
                let xy = parts[1].split('x').collect::<Vec<&str>>();
                Command::Rect(xy[0].parse().unwrap(), xy[1].parse().unwrap())
            }
            "rotate" => {
                let axis = parts[2].split('=').collect::<Vec<&str>>()[1]
                    .parse()
                    .unwrap();
                let steps = parts[4].parse().unwrap();

                match parts[1] {
                    "row" => Command::RotateRow { row: axis, steps },
                    "column" => Command::RotateCol { col: axis, steps },
                    _ => panic!("Unknown rotate axis"),
                }
            }
            _ => panic!("Unknown command"),
        }
    }
}

pub fn generator(input: &str) -> Vec<Command> {
    input.lines().map(Command::from_str).collect()
}

fn render_screen(input: &[Command]) -> Array2<bool> {
    let mut screen: Array2<bool> = Array::from_elem((50, 6), false);

    for cmd in input {
        match cmd {
            Command::Rect(x, y) => screen.slice_mut(s![0..*x, 0..*y]).fill(true),
            Command::RotateRow { row, steps } => {
                let last = screen.slice(s!(-steps.., *row)).to_owned();
                for i in (0..(50 - *steps as usize)).rev() {
                    screen[[i + *steps as usize, *row]] = screen[[i, *row]];
                }
                screen.slice_mut(s!(..*steps, *row)).assign(&last);
            }
            Command::RotateCol { col, steps } => {
                let last = screen.slice(s!(*col, -steps..)).to_owned();
                for i in (0..(6 - *steps as usize)).rev() {
                    screen[[*col, i + *steps as usize]] = screen[[*col, i]];
                }
                screen.slice_mut(s!(*col, ..*steps)).assign(&last);
            }
        }
    }

    screen
}

pub fn part_1(input: &[Command]) -> i64 {
    let screen = render_screen(input);
    screen.map(|b| if *b { 1 } else { 0 }).sum()
}

pub fn part_2(input: &[Command]) -> String {
    let screen = render_screen(input);
    for col in screen.columns() {
        for b in col.iter() {
            print!("{}", if *b { '#' } else { ' ' });
        }
        println!();
    }
    "see above".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rotate_row() {
        assert_eq!(
            part_1(&[Command::Rect(1, 6), Command::RotateRow { row: 3, steps: 3 }]),
            6
        );
    }
}
