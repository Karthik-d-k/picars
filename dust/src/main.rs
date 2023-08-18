use std::{thread, time::Duration};

use anyhow::Result;

// use drishti::eyes::capture;
use drishti::depth::Ultrasonic;
// use vahana::drive::Motor;

fn main() -> Result<()> {
    // let image_path = "images/image.jpg";
    // capture("1000", image_path);
    // let mut motor = Motor::new().expect("Failed to initialize motor.");

    // // Example usage
    // motor.wheel(50, -1);

    // // Sleep for a while to observe the effect
    // sleep(Duration::from_secs(5));

    // // Turn off the motor
    // motor.wheel(0, -1);
    // Ok(())
    let rst_pin = dust::recet_mcu().expect("MCU RESET UNSUCCESSFULL");
    println!("MCU RESET SUCCESSFULLY WITH PIN [{rst_pin}]");

    let _i2c = dust::init_i2c().expect("I2C INITIALIZED SUCCESSFULLY");

    let iterations = 5;
    let trig_pin = 27; // D2 (robot-hat)
    let echo_pin = 22; // D3 (robot-hat)

    let mut ultrasonic = Ultrasonic::new(trig_pin, echo_pin)?;

    for _ in 0..iterations {
        let distance = ultrasonic.read();
        println!("Distance: {} cm", distance);
        // Sleep for 60 milliseconds (as per DATASHEET) --> FIX ME: consider ultrasonic.read() timing into account
        thread::sleep(Duration::from_millis(60));
    }

    Ok(())
}
