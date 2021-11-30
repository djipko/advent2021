use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let data = fs::read_to_string("input")?;
    let lines = data.split("\n");
    Ok(())
}
