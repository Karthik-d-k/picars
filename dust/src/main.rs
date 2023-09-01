use std::{thread, time::Duration};

use anyhow::{Context, Result};

use drishti::{
    depth::Ultrasonic,
    eyes::{capture, cv_example},
};
use vahana::{
    drive::{Motors, Servo},
    init_i2c,
};

fn main() -> Result<()> {
    let image_path = "image.jpg";
    capture("1000", image_path);
    cv_example(image_path)?;

    let rst_pin = dust::recet_mcu().expect("MCU RESET UNSUCCESSFULL [BEGIN]");
    println!("MCU RESET SUCCESSFULLY WITH PIN [{rst_pin}] [BEGIN]");
    let _i2c = init_i2c().expect("I2C INITIALIZATION FAILED");

    // servo
    let mut camera_servo_pin1 = Servo::new(0).context("camera_servo_pin1 init failed")?; // P0
    let mut camera_servo_pin2 = Servo::new(1).context("camera_servo_pin2 init failed")?; // P1
    let mut dir_servo_pin = Servo::new(2).context("dir_servo_pin init failed")?; // P2

    camera_servo_pin1.angle(20.0)?;
    camera_servo_pin2.angle(-20.0)?;
    dir_servo_pin.angle(10.0)?;

    // motors
    let mut motors = Motors::new().context("motors init failed")?;
    motors.speed(0.0, 0.0);
    println!("MOTORS STARTED.......................................");
    motors.forward(50.0);
    thread::sleep(Duration::from_secs(1));
    motors.stop();
    println!("MOTORS STOPPED.......................................");

    // ultrasonic
    let trig_pin = 27; // D2 (robot-hat)
    let echo_pin = 22; // D3 (robot-hat)

    let mut ultrasonic = Ultrasonic::new(trig_pin, echo_pin)?;

    for _ in 0..5 {
        let distance = ultrasonic.read();
        println!("Distance: {} cm", distance);
        // Sleep for 60 milliseconds (as per DATASHEET) --> FIX ME: consider ultrasonic.read() timing into account
        thread::sleep(Duration::from_millis(60));
    }

    let rst_pin = dust::recet_mcu().expect("MCU RESET UNSUCCESSFULL [END]");
    println!("MCU RESET SUCCESSFULLY WITH PIN [{rst_pin}] [END]");

    Ok(())
}
