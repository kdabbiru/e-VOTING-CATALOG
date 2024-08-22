import random
import hashlib
import datetime
from prettytable import PrettyTable

class ElectronicVotingSystem:
    def __init__(self):
        self.voters = []
        self.votes = []
        self.feedbacks = []
        self.candidates = ["Candidate A", "Candidate B", "Candidate C"]
        self.vote_count = {candidate: 0 for candidate in self.candidates}
        self.vote_count['Not Anyone'] = 0  # Option to abstain

    def generate_voter_id(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        city = input("Enter your city: ")
        state = input("Enter your state: ")
        
        if age < 18:
            print("Sorry, you must be at least 18 years old to vote.\n")
            return

        voter_id = str(random.randint(1000, 9999))
        while any(voter['voter_id'] == voter_id for voter in self.voters):
            voter_id = str(random.randint(1000, 9999))

        voter_info = {
            'name': name,
            'age': age,
            'city': city,
            'state': state,
            'voter_id': voter_id
        }
        self.voters.append(voter_info)
        print(f"Your unique Voter ID is: {voter_id}\n")

    def cast_vote(self, voter_id):
        if any(vote['voter_id'] == voter_id for vote in self.votes):
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
                    if choice == len(self.candidates) + 1:
                        selected_candidate = 'Not Anyone'
                    else:
                        selected_candidate = self.candidates[choice - 1]
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        timestamp = datetime.datetime.now()
        encrypted_vote = self.encrypt_vote(voter_id, selected_candidate, timestamp)
        self.votes.append({
            'voter_id': voter_id,
            'vote': encrypted_vote,
            'timestamp': timestamp
        })
        self.vote_count[selected_candidate] += 1
        print("Your vote has been cast successfully.\n")

    def leave_feedback(self):
        feedback = input("Please leave your feedback: ")
        self.feedbacks.append(feedback)
        print("Thank you for your feedback!\n")

    def encrypt_vote(self, voter_id, vote, timestamp):
        data = voter_id + vote + str(timestamp)
        encrypted_data = hashlib.sha256(data.encode()).hexdigest()
        return encrypted_data

    def view_registered_voters(self):
        table = PrettyTable()
        table.field_names = ["Name", "State", "Voter ID"]
        for voter in sorted(self.voters, key=lambda x: x['voter_id']):
            table.add_row([voter['name'], voter['state'], voter['voter_id']])
        print("Registered Voters:")
        print(table)
        print()

    def view_votes(self):
        print("Votes with Timestamps and Hashes:")
        for vote in self.votes:
            print(f"Voter ID: {vote['voter_id']} | Time: {vote['timestamp']} | Hash: {vote['vote']}")
        print()

    def view_feedbacks(self):
        print("Feedbacks:")
        for feedback in self.feedbacks:
            print(f"- {feedback}")
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
                if any(voter['voter_id'] == voter_id for voter in self.voters):
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
                break
            else:
                print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    system = ElectronicVotingSystem()
    system.run()

