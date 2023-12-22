# CLI Movie Rental

CLI Movie Rental is a user-friendly command-line application developed as a school project, designed for efficient movie management.

## Features
- **Rent Movies:** Easily rent your favorite movies from the comfort of your command line.
- **Return Movies:** Seamlessly return rented movies with a straightforward process.
- **Browse Movies:** Explore the available movie list effortlessly, finding the perfect film for your entertainment.
- **Add/Delete Movies:** Customize your catalog by adding or removing movies with a simple command.
- **Data Storage:** All data, including rented movies, is securely stored in JSON files on your local machine, ensuring easy and uncomplicated management.
- **Activity Logging:** The program automatically creates a log.csv file, logging user actions such as renting, returning, adding, or deleting movies, along with timestamps.
- **Secret Menu:** For the adventurous users, entering the number 8 in the main menu reveals a hidden menu with additional options.

## Getting Started
1. Clone the repository: `git clone https://github.com/robskuu/CLI-Movie-Rental.git`
2. Navigate to the project directory: `cd CLI-Movie-Rental`
3. Run the application: `python main.py`

## How to Use
1. Run the application: `python main.py`
2. The application will present a numbered list of options:
   - To rent a movie: Type the corresponding number and choose from the list of available movies.
   - To return a movie: Type the corresponding number and choose from the list of rented movies.
   - To browse available movies: Type the corresponding number.
   - To add a movie to the catalog: Type the corresponding number and enter the movie details.
   - To delete a movie from the catalog: Type the corresponding number and choose from the list of available movies.
   - *Pro Tip:* Enter the number 8 for an additional surprise!

Example:
```bash
1. Show available films
2. Rent a film
3. Return a film
4. Show rented films
5. Add/remove film
6. Create/remove users
7. Quit
Enter the number of your choice: 3
Choose an option: 1

Available Movies:
1. Movie A
2. Movie B
3. Movie C

Enter the number of the movie to rent: 2
