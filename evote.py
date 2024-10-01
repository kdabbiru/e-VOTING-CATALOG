import random
import hashlib
import datetime
import sqlite3
from prettytable import PrettyTable

class ElectronicVotingSystem:
    def __init__(self):
        self.connection = sqlite3.connect('voting_system.db')
        self.create_tables()
        self.candidates = ["Candidate A", "Candidate B", "Candidate C"]
        self.vote_count = {candidate: 0 for candidate in self.candidates}
        self.vote_count['Not Anyone'] = 0  # Option to abstain

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS voters (
                          id INTEGER PRIMARY KEY,
                          name TEXT,
                          age INTEGER,
                          city TEXT,
                          state TEXT,
                          voter_id TEXT UNIQUE)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS votes (
                          id INTEGER PRIMARY KEY,
                          voter_id TEXT,
                          vote TEXT,
                          timestamp TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS feedbacks (
                          id INTEGER PRIMARY KEY,
                          feedback TEXT)''')
        self.connection.commit()

    def generate_voter_id(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        city = input("Enter your city: ")
        state = input("Enter your state: ")
        
        if age < 18:
            print("Sorry, you must be at least 18 years old to vote.\n")
            return

        voter_id = str(random.randint(1000, 9999))
        cursor = self.connection.cursor()
        while True:
            cursor.execute("SELECT * FROM voters WHERE voter_id = ?", (voter_id,))
            if cursor.fetchone() is None:
                break
            voter_id = str(random.randint(1000, 9999))

        cursor.execute("INSERT INTO voters (name, age, city, state, voter_id) VALUES (?, ?, ?, ?, ?)",
                       (name, age, city, state, voter_id))
        self.connection.commit()
        print(f"Your unique Voter ID is: {voter_id}\n")

    def cast_vote(self, voter_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM votes WHERE voter_id = ?", (voter_id,))
        if cursor.fetchone() is not None:
            print("You have already voted. Duplicate voting is not allowed.\n")
            return
        
        print("Candidates:")
        for idx, candidate in enumerate(self.candidates, 1):
            print(f"{idx}. {candidate}")
        print(f"{len(self.candidates) + 1}. Not Anyone")

        while True:
            try:
                choice = int(input("Enter the number corresponding to your choice: "))
                if 1 <= choice <= len(self.candidates) + 1:
                    selected_candidate = 'Not Anyone' if choice == len(self.candidates) + 1 else self.candidates[choice - 1]
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        timestamp = datetime.datetime.now().isoformat()
        encrypted_vote = self.encrypt_vote(voter_id, selected_candidate, timestamp)
        cursor.execute("INSERT INTO votes (voter_id, vote, timestamp) VALUES (?, ?, ?)",
                       (voter_id, encrypted_vote, timestamp))
        self.connection.commit()
        self.vote_count[selected_candidate] += 1
        print("Your vote has been cast successfully.\n")

    def leave_feedback(self):
        feedback = input("Please leave your feedback: ")
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO feedbacks (feedback) VALUES (?)", (feedback,))
        self.connection.commit()
        print("Thank you for your feedback!\n")

    def encrypt_vote(self, voter_id, vote, timestamp):
        data = voter_id + vote + str(timestamp)
        encrypted_data = hashlib.sha256(data.encode()).hexdigest()
        return encrypted_data

    def view_registered_voters(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, state, voter_id FROM voters")
        table = PrettyTable()
        table.field_names = ["Name", "State", "Voter ID"]
        for row in cursor.fetchall():
            table.add_row(row)
        print("Registered Voters:")
        print(table)
        print()

    def view_votes(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT voter_id, vote, timestamp FROM votes")
        print("Votes with Timestamps and Hashes:")
        for row in cursor.fetchall():
            print(f"Voter ID: {row[0]} | Time: {row[2]} | Hash: {row[1]}")
        print()

    def view_feedbacks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT feedback FROM feedbacks")
        print("Feedbacks:")
        for row in cursor.fetchall():
            print(f"- {row[0]}")
        print()

    def tally_votes(self):
        print("Vote tallying...")
        for candidate, count in self.vote_count.items():
            print(f"{candidate}: {count} votes")
        print()

    def declare_results(self):
        max_votes = max(self.vote_count.values())
        winners = [candidate for candidate, votes in self.vote_count.items() if votes == max_votes]
        print("Election Results:")
        if len(winners) > 1:
            print(f"Tie between: {', '.join(winners)} with {max_votes} votes each")
        else:
            print(f"Winner: {winners[0]} with {max_votes} votes")
        print()

    def voter_menu(self):
        while True:
            print("Voter Menu")
            print("1. Generate Voter ID")
            print("2. Cast Vote")
            print("3. Leave Feedback")
            print("0. Go to Previous Menu")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.generate_voter_id()
            elif choice == '2':
                voter_id = input("Enter your Voter ID: ")
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM voters WHERE voter_id = ?", (voter_id,))
                if cursor.fetchone() is not None:
                    self.cast_vote(voter_id)
                else:
                    print("Invalid Voter ID! Please generate a valid Voter ID first.\n")
            elif choice == '3':
                self.leave_feedback()
            elif choice == '0':
                break
            else:
                print("Invalid choice! Please try again.\n")

    def election_commission_menu(self):
        while True:
            print("Election Commission Menu")
            print("1. View Registered Voters")
            print("2. View Votes")
            print("3. View Feedbacks")
            print("4. Tally Votes")
            print("5. Declare Results")
            print("0. Go to Previous Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_registered_voters()
            elif choice == '2':
                self.view_votes()
            elif choice == '3':
                self.view_feedbacks()
            elif choice == '4':
                self.tally_votes()
            elif choice == '5':
                self.declare_results()
            elif choice == '0':
                break
            else:
                print("Invalid choice! Please try again.\n")

    def run(self):
        print("Welcome to the Electronic Voting System\n")

        while True:
            print("Login as:")
            print("1. Voter")
            print("2. Election Commission")
            print("0. Exit")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.voter_menu()
            elif choice == '2':
                self.election_commission_menu()
            elif choice == '0':
                print("Exiting the system. Thank you!")
                self.connection.close()
                break
            else:
                print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    system = ElectronicVotingSystem()
    system.run()
