fn main() {
    println!("{}", rom2dec("MMMIM"));
}

fn legend(numeral: &str) -> Option<u32> {
    match numeral {
        "I" => Some(1),
        "V" => Some(5),
        "X" => Some(10),
        "L" => Some(50),
        "C" => Some(100),
        "D" => Some(500),
        "M" => Some(1000),
        _ => None
    }
}

fn rom2dec(numerals: &str) -> u32 {
    let mut total: u32 = 0;
    let mut prev_dval: u32 = 0;

    for numeral_digit in numerals.chars() {
        let dval: u32 = legend(&String::from(numeral_digit)).unwrap();
        if prev_dval <= dval {
            total += dval;
        } else {
            total -= dval;
        }
        prev_dval = dval;
    }
    
    return total;
}
