use std::thread::sleep;
use std::{thread, time::Duration};

use anyhow::Result;
use rppal::gpio::Level;

use drishti::depth::Ultrasonic;
use drishti::eyes::capture;
use vahana::drive::Motor;
use vahana::drive::{init_i2c, scan_i2c};

fn main() -> Result<()> {
    // let image_path = "images/image.jpg";
    // capture("1000", image_path);
    let rst_pin = dust::recet_mcu().expect("MCU RESET UNSUCCESSFULL [BEGIN]");
    println!("MCU RESET SUCCESSFULLY WITH PIN [{rst_pin}] [BEGIN]");
    let i2c = init_i2c().expect("I2C INITIALIZATION FAILED");

    // i2c debug
    println!("{i2c:?}");
    println!("{:?}", i2c.capabilities());
    println!("I2c Addresses: {:?}", scan_i2c(i2c));
    /*
        let mut motor = Motor::new().expect("Failed to initialize motor.");
        println!("motors initialized successfully");

        motor.left_rear_pwm_pin.period(1000)?;
        motor.right_rear_pwm_pin.period(1000)?;
        motor.left_rear_pwm_pin.prescaler(10)?;
        motor.right_rear_pwm_pin.prescaler(10)?;

        println!("MOTORS STARTED.......................................");
        for iter in 0..10 {
            for i in (0..4095).step_by(10) {
                motor.left_rear_dir_pin.write(Level::High);
                let _ = motor.left_rear_pwm_pin.pulse_width(i);
                motor.right_rear_dir_pin.write(Level::Low);
                let _ = motor.right_rear_pwm_pin.pulse_width(i);
            }
            sleep(Duration::from_secs(2));
            println!("***************************************************");
            for i in (0..4095).rev().step_by(10) {
                motor.left_rear_dir_pin.write(Level::Low);
                let _ = motor.left_rear_pwm_pin.pulse_width(i);
                motor.right_rear_dir_pin.write(Level::High);
                let _ = motor.right_rear_pwm_pin.pulse_width(i);
            }
            sleep(Duration::from_secs(2));
            println!("ITERATION: {iter}");
        }
        println!("MOTORS STOPPED.......................................");

        let trig_pin = 27; // D2 (robot-hat)
        let echo_pin = 22; // D3 (robot-hat)

        let mut ultrasonic = Ultrasonic::new(trig_pin, echo_pin)?;

        for _ in 0..5 {
            let distance = ultrasonic.read();
            println!("Distance: {} cm", distance);
            // Sleep for 60 milliseconds (as per DATASHEET) --> FIX ME: consider ultrasonic.read() timing into account
            thread::sleep(Duration::from_millis(60));
        }
    */
    let rst_pin = dust::recet_mcu().expect("MCU RESET UNSUCCESSFULL [END]");
    println!("MCU RESET SUCCESSFULLY WITH PIN [{rst_pin}] [END]");

    Ok(())
}
