# HexBot

  <a href="https://github.com/AidanInceer/HexBot">
    <img alt="Static Badge" src="https://img.shields.io/badge/version-1.3.0-blue">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
  <a href="#badge">
    <img alt="https://github.com/pre-commit/pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit">
  </a>
  <a href="https://github.com/AidanInceer/HexBot/actions/workflows/build.yml">
    <img src="https://github.com/AidanInceer/HexBot/actions/workflows/build.yml/badge.svg">
  </a>
  <a href="https://github.com/AidanInceer/HexBot/actions/workflows/lint.yml">
    <img src="https://github.com/AidanInceer/HexBot/actions/workflows/lint.yml/badge.svg">
  </a>
    <a href="https://github.com/AidanInceer/HexBot/actions/workflows/test.yml">
    <img src="https://github.com/AidanInceer/HexBot/actions/workflows/test.yml/badge.svg">
  </a>
  <a href="https://github.com/AidanInceer/HexBot/actions/workflows/scan.yml">
    <img src="https://github.com/AidanInceer/HexBot/actions/workflows/scan.yml/badge.svg">
  </a>
  <a href="https://sonarcloud.io/summary/new_code?id=AidanInceer_HexBot">
    <img src="https://sonarcloud.io/api/project_badges/measure?project=AidanInceer_HexBot&metric=alert_status">
  </a>
  <a href="https://sonarcloud.io/summary/new_code?id=AidanInceer_HexBot">
    <img src="https://sonarcloud.io/api/project_badges/measure?project=AidanInceer_HexBot&metric=coverage">
  </a>
  <a href="https://sonarcloud.io/summary/new_code?id=AidanInceer_HexBot">
    <img src="https://sonarcloud.io/api/project_badges/measure?project=AidanInceer_HexBot&metric=duplicated_lines_density">
  </a>
  <a href="https://sonarcloud.io/summary/new_code?id=AidanInceer_HexBot">
    <img src="https://sonarcloud.io/api/project_badges/measure?project=AidanInceer_HexBot&metric=security_rating">
  </a>
<a href="https://sonarcloud.io/summary/new_code?id=AidanInceer_HexBot">
    <img src="https://sonarcloud.io/api/project_badges/measure?project=AidanInceer_HexBot&metric=code_smells">
  </a>
<a href="https://sonarcloud.io/summary/new_code?id=AidanInceer_HexBot">
    <img src="https://sonarcloud.io/api/project_badges/measure?project=AidanInceer_HexBot&metric=bugs">
  </a>

## Introduction

Currently the board/game is displayed in the command line. However in future i would like to move this either to a website of full built out UI.

![Catan Image](./imgs/catan.png)

### Task list

- [ ] Productionize
- [ ] Basic bot functionality
- [ ] Input validation
- [ ] Neural net implementation
- [ ] Training
- [ ] UI/Web Development

## Setup

To get started with HexBot, follow these steps:

- Clone the repository:

  ```bash
  git clone https://github.com/AidanInceer/HexBot
  ```

- Install the required dependencies:

  ```bash
  pip install -r requirements.txt
  ```

- Run the application:

  ```bash
  python main.py
  ```

## Additional Configuration

You can adjust the game settings in the central configuration file `src/catan/config/config.py`. This can be used to adjust the number of players, automatic setup, bot strength and much more.
