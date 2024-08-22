# e-VOTING-CATALOG
# Electronic Voting System

## Overview

The Electronic Voting System is a command-line application designed to ensure a secure, fair, and efficient voting process. The system caters to two types of users: voters and election commission officials. It aims to maintain the integrity of the voting process by preventing unauthorized access to vote information and ensuring votes are tamper-proof. The application is built to be used in a command-line interface without any frontend, backend, or database.

## Features

- **Voter Operations:**
  - Generate a unique voter ID by providing personal details.
  - Cast a vote with a timestamp.
  - Leave feedback about the voting experience.
  
- **Election Commission Operations:**
  - View a list of registered voters with their details in a tabular format.
  - View encrypted votes and their timestamps.
  - Tally all votes.
  - Declare election results.

## Technologies

- **Python**: The primary programming language used to implement the application logic.
- **Hashlib**: Used for hashing votes to ensure data integrity.
- **PrettyTable**: Used for displaying data in a tabular format for easier readability.

## How It Works

### User Types

1. **Voter**
   - **Generate Voter ID**: Enter personal details to receive a unique voter ID. The ID is stored for future reference.
   - **Cast Vote**: Select a candidate and cast your vote, which is timestamped and encrypted for security.
   - **Leave Feedback**: Provide feedback on the voting experience.

2. **Election Commission**
   - **View Voters**: Display a list of registered voters with their details in a tabular format.
   - **View Votes**: Access encrypted vote data along with timestamps.
   - **Tally Votes**: Calculate the total votes for each candidate.
   - **Declare Results**: Finalize and announce the election results.

### Command-Line Navigation

- **Voter Menu:**
  1. Generate Voter ID
  2. Cast Vote
  3. Leave Feedback
  4. Exit

- **Election Commission Menu:**
  1. View Registered Voters
  2. View Votes
  3. Tally Votes
  4. Declare Results
  5. Exit

**Note:** Use option `0` to return to the previous menu at any point.

## Installation

1. Ensure Python is installed on your machine.
2. Install the necessary Python packages using pip:

    ```sh
    pip install prettytable
    ```

## Usage

1. **Run the Application**: Execute the script using Python:

    ```sh
    python voting_system.py
    ```

2. **Follow the Prompts**: Choose the user type (Voter or Election Commission) and follow the on-screen instructions to perform the desired operations.

## Technical Details

- **Hashing Algorithm**: SHA-256 is used to hash votes, ensuring that the vote data cannot be tampered with.
- **Timestamping**: Every vote is timestamped to maintain a record of when it was cast.
- **Data Storage**: Data is temporarily stored in memory during runtime. For persistent storage, consider integrating a database in a real-world scenario.

## Limitations

- **Temporary Storage**: Data is stored only in memory and will be lost upon exiting the application.
- **No Frontend or Backend**: This implementation does not include a graphical user interface or web-based backend.

## Contributing

If you wish to contribute to this project, please fork the repository, make your changes, and submit a pull request. Ensure that your code follows the project's style guidelines and passes all tests.

