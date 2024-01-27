![Wallpaper](wallpaper.png)

# The Developers Dashboard

_A Developer Metrics Visualization Tool_

## Introduction

There are a lot of dashboards for developers to understand tools, hardware, systems, and so on.
After years of writing software I developed the need for a dashboard about the data to lead software
writing teams.

The developer dashboard would be the attempt to make leading software writing teams simpler. To show
the key metrics about the software and to give tips for teams in dealing with new challenges.

In this first version we will be focusing on developer velocity and the burn down of projects.
Designed to integrate with ticket systems like Jira, this tool fills the gap in agile project
management and Scrum methodologies by providing insightful visualizations.

## Problem Statement

In the realm of agile development, especially within Scrum frameworks, tracking and understanding
team progress can be challenging. Popular project management tools like Jira offer extensive
functionalities but fall short in providing comprehensive insights into Developer Velocity and Burn
Down metrics. These metrics are crucial for evaluating team efficiency and project timelines, yet
they are often overlooked or underutilized due to a lack of proper visualization tools.

## Project Intent

The primary intent of this project is to empower developer teams and management with detailed,
easy-to-understand visual representations of Developer Velocity and Burn Down estimation. By extracting
data from existing ticket systems (e.g., Jira), the tool aims to:

1. Enhance transparency and understanding of individual and team performances.
2. Provide clear insights into project progress and potential bottlenecks.
3. Support data-driven decision-making for project planning and resource allocation.

## How to Use

### Prerequisites

- Access to a ticket system like Jira with API capabilities.
- Basic understanding of HTML, JavaScript, and D3.js for customizations.

### Installation and Setup

1. Clone the repository from [GitHub repository link].
2. Ensure you have [Node.js](https://nodejs.org/) installed.
3. Install dependencies: `npm install`.
4. Configure the tool to connect with your ticket system API (instructions in `config.js`).

### Running the Tool

- Start the application: `npm start`.
- Access the web interface via `http://localhost:3000`.

### Customization

- Modify the visual styles in `style.css`.
- Adjust the data-fetching logic in `dataFetcher.js` for different data sources.

## Under the Hood

### Data Fetching

- The tool interfaces with ticket systems like Jira through their API.
- It fetches relevant data points such as story points, task statuses, and completion dates.
- since every ticket system is different and systems like jira even allow for their users to customize their ticket types there is no good way to provide a unified integration for the ticket systems out there. To get started and inverse the dependency we start by creating an interface for integrations. Users can write there own endpoints and the developer dashboard will just use the given endpoint to fetch the necessary data. 

### Data Processing

- The raw data is processed to calculate Developer Velocity and Burn Down estimations.
- Developer Velocity is computed based on the amount of story points completed over specific time
  frames (day, week, month, year).
- Burn Down estimations are calculated by tracking the completion of tasks against their estimated
  timelines.

### Visualization

- D3.js is utilized to create dynamic, interactive charts for both metrics.
- The Developer Velocity section displays individual and aggregated team velocities.
- The Burn Down section visualizes task completion against estimated timelines.

## Contributing

We welcome contributions to improve this tool. Please read `CONTRIBUTING.md` for guidelines on how
to propose enhancements or report issues.
