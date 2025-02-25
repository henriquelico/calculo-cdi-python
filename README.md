# CDI Investment Calculator

This project is a simple Python script that fetches the latest CDI (Certificado de Depósito Interbancário) rate from the Brazilian Central Bank API and calculates the estimated return on investment over a specified number of months.

## Features
- Fetches the latest CDI value from the BCB API.
- Allows configuring how much of the CDI rate is used (e.g., 100%, 105%).
- Calculates investment growth over multiple months based on compounding daily growth.
- Outputs expected final amount and percentage return.

## Installation

To use this project, you need Python 3 installed. You can install the required dependencies using:

```bash
pip install -r Requirements.txt
