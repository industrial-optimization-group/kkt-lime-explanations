# KKT-based trade-off explanations for interactive multiobjective optimization

This repository contains the implementation of software used in the research article "Can LIME Make Interactive Multiobjective Optimization Methods Explainable?"

The repository includes two main components:

- **Backend:** Computes KKT multipliers and approximated solutions. It provides a Flask API for integration with the frontend but can also function as a standalone module.
- **Frontend:** An interactive user interface that allows users to input reference points and obtain non-dominated solutions with explanations.

## Installation

To get started, clone this repository:

```bash
git clone https://github.com/industrial-optimization-group/kkt-lime-explanations.git
```

## Backend Setup

1. Create a virtual environment for the backend
   Using Python's venv module:

```bash
python -m venv .venv
```

Or with Poetry:

```bash
poetry shell
```

2. Activate the virtual environment
   For venv:

```bash
source .venv/bin/activate
```

Or with Poetry:

```bash
poetry shell
```

3. Install dependencies
   Navigate to the tradeoff-analysis folder and install the backend code:

```bash
poetry install
```

4. Run the code
   Navigate to the explainable_moo folder and run:

```bash
python api.py
```

After this, the server should be running locally in your computer. The IP address of the server will be shown in the terminal.

## Installing the frontend

1. In a separate terminal, navigate to the XMOO-UI folder:

```bash
cd kkt-lime-explanations
cd XMOO-UI
```

2. Install Dependencies:
   Use npm, pnpm, or yarn to install the required packages:

```bash
npm install
```

(Replace npm with pnpm or yarn if using one of those package managers.)

3. Run the development server:
   Start the server for local development:

```bash
npm run dev
```

Or open the app in a browser automatically:

```bash
npm run dev -- --open
```

## Usage

1. Ensure the backend server is running.

- Activate the virtual environment and start the Flask API server from the backend directory.

2. Access the frontend application:

- Open the development server URL (default: http://localhost:3000) in a web browser.

3. Provide reference points in the frontend to generate solutions and explanations.
