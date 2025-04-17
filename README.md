

# LeafHub 🪴  

#### A smarter (and easier) way to take care of your plants.

<br>

> [!WARNING]  
> This project is still in its very early growing phase. Features and the experience might change, but this README is supposed to give you a general idea of what LeafHub is supposed to become.

<br>

## 🔎 Overview

LeafHub makes your plants smart! Attach a small device to your plant and measure things like:

- Air humidity  
- Temperature
- Light levels
- Soil moisture

This data will be sent to a central server, which stores, organizes, and serves it to the user-facing interface. 
And the most important (and exciting :D) part, the user interface:

This will act like your small digital (and also kind of real) garden! You can:

- Add, arrange, and customize your plants!
- Give your plants names! (Be honest, we know you always wanted to)
- Configure which data you want to track and how you want it to be visualized!
- Utilize reminders to help your plants stay alive! (No more dead plants, no more guilt!)

Remember, the project is still very young; things might change! But in general, these are the features we want to provide for now. But the sky is the limit!

<br>

## 🧩 Components

To make this work, we provide you with this set of components:

- **Firmware**

  A flexible firmware that works with a variety of microcontrollers and sensors.

- **Backend**

  A server that communicates with devices, stores them, and serves data to the frontend.

- **Frontend**

  A pretty web dashboard for managing your plants, viewing live charts, and interacting with your plants.

<br>

## ⚙️ The Firmware

Our goal is maximum flexibility. Using MicroPython allows us to make our code more hardware independent by abstracting away
low-level hardware details you would have to deal with otherwise. There is no perfect solution; however, MicroPython implementations can vary slightly.
and each board has different LEDs and sensor pins. To address the latter, we use a Hardware Abstraction Layer (HAL):

- Small MicroPython "HAL" scripts that tell the firmware how to access onboard LEDs, GPIO pins, and sensors.
- We provide an [example template](./firmware/hal/template.py) and a [typing module](./firmware/hal/hal.py) to make this reasonably simple, in case you do have to write your own.
- In general, we want to spare you from writing these HALs, so our goal is to provide premade and tested ones for commonly used setups.

<br>

## 🌐 The Backend & Frontend

These components are more straightforward since they don’t touch hardware. We aim to make self-hosting as easy as possible:

- **Easy to set up**

  To make this process as painless as possible, our goal is to make this a pretty standard process by providing setup scripts or container configurations.

- **Onboarding Process**

  When you first set up your microcontroller, there will be a straightforward onboarding procedure to connect your device to the server.
  
The idea is that everything else works without any trouble and is an "out-of-box" experience.

<br>

## 🏁 Our Goal

We eventually plan to offer a fully cloud-hosted option. The server hosting is done by us, and we may even provide you with premade hardware so you could simply
get a LeafHub device, plug it in, and start monitoring. This will never compromise our self-hosting-friendly approach; it is simply an addition.

<br>

## 📄 License

This project is licensed under the [GNU GPLv3 license](https://choosealicense.com/licenses/gpl-3.0/).

<br>

## 🤝 Contribution

Randware loves open source! If you're interested and you'd like to help:

1. Fork this repo
2. Create a branch for your feature or fix
3. Send a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details. Your help is much appreciated ❤️
