# FPL Optimiser Project Guidelines

## Communication Style
Keep code suggestions concise and to the point. If you have alternative approaches, ask for clarification on requirements before suggesting them.

## Code Style Standards

### Functional and Professional
- Write concise but readable code
- Include comments that explain the process, not the obvious
- No unnecessary comments or self-congratulatory remarks
- No emojis in production code
- This is a professional working document for collaborative development

### Code Organization
- Use clear, descriptive function and variable names
- Keep functions focused on a single responsibility
- Include docstrings for functions explaining purpose, args, and returns
- Group related functionality logically

## Project Structure

This repository is organized into three main components:

### 1. Data Collection (`data/`)
Scripts for gathering complete datasets for each gameweek from the FPL API.


### 2. Optimiser (`optimiser/`)
Squad selection and optimization logic.

### 3. Dashboard (`app/`)
User interface and visualization components.

## Current Focus
Currently working on data collection layer to establish reliable, efficient data pipelines from the FPL API. 