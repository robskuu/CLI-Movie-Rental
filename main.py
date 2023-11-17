import json
import csv
import datetime as dt
import pandas as pd
import sys
import os
import time

# ANSI colors
class ans:  # txtColor_bgColor
  ENDCOLOR = "\033[0;0m"
  WHITE_RED = "\033[3;37;41m"
  YEL_BLUE = "\033[3;33;44m"
  GREEN_BLACK = "\033[3;32;40m"
  RED_BLACK = "\033[3;31;40m"
  WHITE_PURP = "\033[3;37;45m"
  NOTE = "\033[3;31;43m"
  SUCCESS = "\033[3;32;40m"
  HEADER = "\033[3;37;44m"
  
# Unicode characters
class uni:
  # Unicode character for a star inside of a circle
  STARC = "\u235F"

# Writes what happens to the log.csv file
def createLog(action, user, phone, movie=0):
  uId = str(customerID(user, phone))
  logContent = []
  if action.lower() == "return" or action.lower() == "rent":
      if action.lower() == "return":
          # Return film
          logContent = ["Film Returned", movie, user, uId, todaysDate()]
      else:
          # Rent film
          logContent = ["Film Rented", movie, user, uId, todaysDate()]

  elif action.lower() == "mcreate" or action.lower() == "mdelete":
      if action.lower() == "mcreate":
          # Add film
          logContent = ["Film Added", movie, user, uId, todaysDate()]
      else:
          # Remove film
          logContent = ["Film Removed", movie, user, uId, todaysDate()]

  elif action.lower() == "ucreate" or action.lower() == "udelete":
      if action.lower() == "ucreate":
          # Create user
          logContent = ["User Created", " ", user, uId, todaysDate()]
      else:
          # Remove user
          logContent = ["User Removed", " ", user, uId, todaysDate()]

  else:
      print("Something went wrong")

  with open("log.csv", "a", newline="") as logFile:
      csvWriter = csv.writer(logFile)
      if logContent != []:
          csvWriter.writerow(logContent)
      else:
          print("The list is empty")

# Clears the log.csv file and adds the headers
def clearLog():
  with open("log.csv", "w", newline="") as logFile:
      csvWriter = csv.writer(logFile)

      headers = ["Action", "Movie", "User", "UserId", "Date"]
      csvWriter.writerow(headers)

# Fixes file issues
def fixes():
  path = "./log.csv"
  if not os.path.isfile(path):
    clearLog()
  mData = movieData()
  cData = customerData()
  rented = []
  changeMe = []
  for user in cData:
      for movie in user["rented_movies"]:
          rented.append(movie)
  for movie in mData:
      if "ComingSoon" in movie:
          changeMe.append(movie["Title"])
      if movie["Title"] in rented:
          changeMe.append(movie["Title"])
  if changeMe != []:
      for title in changeMe:
          chAvail(title, "False")

# Returns todays date formatted to dd/mm/yy
def todaysDate():
  date = dt.datetime.now()
  dateN = date.strftime("%d/%m/%y")
  return dateN

# Returns the data from the movies.json file
def movieData():
  try:
      with open("movies.json") as mFile:
          mData = json.load(mFile)
  except FileNotFoundError:
      mData = []
  return mData

# Returns the data from the customers.json file
def customerData():
  try:
      with open("customers.json") as cFile:
          cData = json.load(cFile)
  except FileNotFoundError:
      cData = []
  return cData

# Returns the customers id based on name and phone number
def customerID(person, phone):
  data = customerData()
  phoneF = phoneFormat(phone)
  for customer in data:
      if customer["name"].lower() == person.lower() and customer["phone"] == phoneF:
          return customer["id"]
  return "Error: User not found"

# Checks if the customer exists based on the name and phone number
def customerExists(name, phone):
  data = customerData()
  phoneF = phoneFormat(phone)
  for customer in data:
      if customer["name"].lower() == name.lower() and customer["phone"] == phoneF:
          return True
  return False

# Changes the "Available" category of a movie to either "True" or False
def chAvail(name, status):
  data = movieData()
  for movie in data:
      if movie["Title"].lower() == name.lower():
          if "ComingSoon" in movie:
              movie["Available"] = "False"
          else:
              movie["Available"] = status

  with open("movies.json", "w") as file:
      json.dump(data, file, indent=4)

# Manages users loans
def manageFilm(name, status, cId):
  data = customerData()
  for c in data:
      if c["id"] == cId:
          isThere = True if name.title() in c["rented_movies"] else False
          if status.lower() == "add":
              if not isThere:
                  chAvail(name.title(), "False")
                  c["rented_movies"].append(name.title())
          elif status.lower() == "remove":
              if isThere:
                  chAvail(name.title(), "True")
                  c["rented_movies"].remove(name.title())
              else:
                  print("Not found")

          with open("customers.json", "w") as file:
              json.dump(data, file, indent=4)

# Prompts that the user doesn't exist and asks to create one
def promptNewUser(person, phone):
  print(ans.NOTE + "The user does not exist" + ans.ENDCOLOR)
  ch = ""
  while True:
      ch = input("Do you want to create a new user? (y/n): ")
      if ch.lower() == "y":
          manageCustomers("add", person, phone)
          return True
      else:
          print("Cancelling . . .")
          menu()

# Adds the customer to the customer.json file
def addCustomer(name, phone):
  phoneF = phoneFormat(phone)
  data = customerData()

  if not customerExists(name, phone):
      highest_id = max(item["id"] for item in data) if data else 1
      new_id = highest_id + 1
      cInfo = {
          "name": name.capitalize(),
          "phone": phoneF,
          "id": int(new_id),
          "rented_movies": [],
      }

      data.append(cInfo)

      with open("customers.json", "w") as file:
          json.dump(data, file, indent=4)

  else:
      print("The user already exists")

# Formats a phone number Ex. 0401230987 ti 040-123-0987
def phoneFormat(phone):
  phoneF = phone[:3] + "-" + phone[3:6] + "-" + phone[6:]
  return phoneF

# User creation/deletion handling
def manageCustomers(action, name, phone):
  data = customerData()
  uId = customerID(name, phone)
  phoneF = phoneFormat(phone)
  if action.lower() == "add":
      # Add User
      highest_id = max(item["id"] for item in data) if data else 1
      new_id = highest_id + 1
      cInfo = {
          "name": name.capitalize(),
          "phone": phoneF,
          "id": int(new_id),
          "rented_movies": [],
      }
      data.append(cInfo)

      with open("customers.json", "w") as file:
          json.dump(data, file, indent=4)
      print("Creating user . . .")
      for i in range(30):
          print("-" * i, end="\r")
          time.sleep(0.2)
      print("\033[K")
      print(ans.SUCCESS + "User created successfully" + ans.ENDCOLOR)
      print("\033[K")
      createLog("ucreate", name, phone)
      
  elif action.lower() == "del":
      # Remove User
      createLog("udelete", name, phone)

      # Returns the users loaned movies/series
      for customer in data:
          if customer["id"] == uId:
              for movie in customer["rented_movies"]:
                  manageFilm(movie, "remove", uId)

      # Removes the user and changes the id on all users that had a higher id
      for customer in data.copy():
          if customer["id"] == uId:
              data.remove(customer)
          if customer["id"] > uId:
              customer["id"] -= 1

      with open("customers.json", "w") as file:
          json.dump(data, file, indent=4)
      print("Removing user . . .")
      for i in range(30):
          print("-" * i, end="\r")
          time.sleep(0.15)
      print("\033[K")
      print(ans.SUCCESS + "User removed successfully" + ans.ENDCOLOR)

# Shows all the available movies and returns a list to use inside another function
def availableFilms(p=None):
  if p is None:
      os.system("cls")
      print(ans.HEADER + "Available Films" + ans.ENDCOLOR)
  data = movieData()
  available_movies = []
  moviePos = 0
  for movie in data:
      if movie["Available"] == "True":
          moviePos += 1
          available_movies.append((moviePos, movie["Title"], movie["Year"]))
          print(f"{moviePos}. {movie['Title']} ({movie['Year']})")
  if available_movies == []:
      print(f"{ans.NOTE} There are no available films at the moment. {ans.ENDCOLOR}")
  return available_movies

# Handles renting of films
def rentFunc(a=0, b=0):
  os.system("cls")
  print(ans.HEADER + "Rent a film" + ans.ENDCOLOR)
  films = availableFilms(1)
  if not films:
      print("There are no available films at the moment.")
      input("Press any key to continue")
      menu()
  else:
      while True:
          userChoice = int(input("Choose a film to rent (Enter the number): "))

          if userChoice <= 0 or userChoice > len(films):
              print("Invalid number. Choose a number from the list.")
          else:
              film_choice = films[userChoice - 1]
              print(f"You have chosen: {film_choice[1]} ({film_choice[2]})")
              break
      if a != 0 and b != 0:
          name = a
          phone = b
      else:
          name = input("Enter your name: ")
          phone = input("Enter your phone number (Ex. 1234567890): ")
      if customerExists(name, phone):
          manageFilm(film_choice[1], "add", customerID(name, phone))
          createLog("rent", name, phone, film_choice[1])
          print(
              f"{ans.SUCCESS}You have rented: {film_choice[1]} ({film_choice[2]}){ans.ENDCOLOR}"
          )
          again = input("Do you want to rent another? (y/n): ")
          if again.lower() == "y":
              rentFunc(name, phone)
          else:
              menu()
      else:
          if promptNewUser(name, phone):
              manageFilm(film_choice[1], "add", customerID(name, phone))
              createLog("rent", name, phone, film_choice[1])
              print(
                  f"{ans.SUCCESS}You have rented: {film_choice[1]} ({film_choice[2]}){ans.ENDCOLOR}"
              )
              again = input("Do you want to rent another? (y/n): ")
              if again.lower() == "y":
                  rentFunc(name, phone)
              else:
                  menu()
          else:
              menu()

# Handles returning of films
def returnFunc(a=0, b=0):
  os.system("cls")
  print(ans.HEADER + "Return a Film" + ans.ENDCOLOR)
  if a != 0 and b != 0:
      name = a
      phone = b
  else:
      name = input("Enter your name: ")
      phone = input("Enter your phone (Ex. 1234567890): ")

  if customerExists(name, phone):
      rented = listRented(customerID(name, phone))

      while True:
          uChoice = int(input("Choose a film to return (Enter the number): "))

          if uChoice <= 0 or uChoice > len(rented):
              print("Invalid number. Choose a number from the list.")
          else:
              chosenM = rented[uChoice - 1]
              print(f"You have chosen: {chosenM}")

              cId = customerID(name, phone)
              data = customerData()

              for customer in data:
                  if customer["id"] == cId:
                      if chosenM in customer["rented_movies"]:
                          manageFilm(chosenM, "remove", cId)

              chAvail(chosenM, "True")

              print(f"{ans.SUCCESS}You have returned: {chosenM}{ans.SUCCESS}")
              createLog("return", name, phone, chosenM)
              break
      if listRented(customerID(name, phone)):
          again = input("Do you want to return another? (y/n): ")
          if again.lower() == "y":
              returnFunc(name, phone)
          else:
              print("Cancelling . . .")
              menu()
      else:
          print("You have no films to return")
          input("Press any key to continue . . .")
          menu()
  else:
      if promptNewUser(name, phone):
          returnFunc(name, phone)
      else:
          menu()

# Returns the year when the movie came out
def getYear(name):
  data = movieData()
  for m in data:
      if m["Title"].lower() == name.lower():
          year = m["Year"]
          return year
  return None

# Prints out a customers rented movies
def listRented(a=0):
  os.system("cls")
  print(ans.HEADER + "Rented Movies" + ans.ENDCOLOR)
  data = customerData()
  if a == 0:
      name = input("Enter your name: ")
      phone = input("Enter your number (Ex. 1234567890):  ")
      cId = customerID(name, phone)
  else:
      cId = a

  rented = []
  rentedPos = 0
  for customer in data:
      if customer["id"] == cId:
          for movie in customer["rented_movies"]:
              rentedPos += 1
              rented.append((rentedPos, movie))
              year = getYear(movie)
              print()
              print(f"{rentedPos}. {movie} ({year})")

  if not rented:
      print("You have no rented movies.")
      input("Press any key to continue . . .")
      menu()

  return [movie for _, movie in rented]

# Removes a film from the movies.json file
def delMovie(mn, name, phone):
  data = movieData()
  av = False
  mChoice = ""
  for idx, movie in enumerate(data):
      if movie["Title"].lower() == mn.lower() and movie["Available"] == "True":
          mChoice = movie["Title"]
          data.pop(idx)
          av = True
          break
  if av:
      createLog("mdelete", name, phone, mChoice)

      with open("movies.json", "w") as file:
          json.dump(data, file, indent=4)

# Adds a movie to the movies.json file
def addMovie(user, phone):
  os.system("cls")
  print(ans.HEADER + "Add a movie" + ans.ENDCOLOR)
  data = movieData()
  cInfo = [
      "ComingSoon (is the movie coming soon? (True/False))",
      "Title",
      "Year (when the movie came out)",
      "Rated (R, PG-13 etc.)",
      "Released (Ex. 15 Jan 2014)",
      "Runtime (in minutes, Ex. 153 min)",
      "Genre (Ex. Action, Fantasy)",
      "Director",
      "Writer",
      "Actors (Ex. James Bond, Bames Jond)",
      "Plot (1 sentence description of the plot)",
      "Language (languages spoken in it)",
      "Country (where it was recorded)",
      "Awards",
      "Poster (poster filename Ex. poster.png)",
      "Metascore (0-100 shall be a whole number)",
      "imdbRating (1.0-10.0 with 1 decimal number)",
      "imdbVotes",
      "imdbID (id on imdb, Ex. tt0499549)",
      "Type (Movie or Series)",
      "TotalSeasons (amount of seasons. If it's a movie leave empty)",
      "Available (True/False)",
      "Images (Enter image filenames separated by a ','. Ex. file1.png, file2.jpg, file3.png, file4.jpg, file5.png)",
  ]

  mInfo = {
      "ComingSoon": "",
      "Title": "",
      "Year": "",
      "Rated": "",
      "Released": "",
      "Runtime": "",
      "Genre": "",
      "Director": "",
      "Writer": "",
      "Actors": "",
      "Plot": "",
      "Language": "",
      "Country": "",
      "Awards": "",
      "Poster": "",
      "Metascore": "",
      "imdbRating": "",
      "imdbVotes": "",
      "imdbID": "",
      "Type": "",
      "TotalSeasons": "",
      "Available": "",
      "Images": ["", "", "", "", ""],
  }
  for idx, category in enumerate(mInfo):
      x = input(f"{cInfo[idx]}: ")
      if mInfo[category] in [
          "Runtime",
          "Plot",
          "Country",
          "Awards",
          "Poster",
          "imdbID",
          "Type",
          "Images",
      ]:
          mInfo[category] = x
      else:
          mInfo[category] = x.title()

  while int(mInfo["Metascore"]) < 0 or int(mInfo["Metascore"]) > 100:
      metaIn = int(input("Enter the metascore (0-100)"))
      if metaIn >= 0 and metaIn <= 100:
          mInfo["Metascore"] = str(metaIn)
          break

  while float(mInfo["imdbRating"]) < 0 or float(mInfo["imdbRating"]) > 10:
      ratingIn = float(input("Enter the imdbRating (0-10 with 1 decimal point Ex. 7.9)"))
      if ratingIn >= 0 and ratingIn <= 10:
          mInfo["imdbRating"] = str(ratingIn)
          break

  # Checks if the ComingSoon is true and corrects the available
  mInfo["Available"] = "False" if mInfo["ComingSoon"] == "True" else "True"

  # Formats the number from 1000 to 1,000
  mInfo["imdbVotes"] = f'{int(mInfo["imdbVotes"]):,}'

  # Checks if the Type is a Movie or Series
  while mInfo["Type"].lower() != "movie" and mInfo["Type"].lower() != "series":
      typed = input("Is it a Movie or Series? (Movie/Series): ")
      if typed.lower() == "movie":
          mInfo["Type"] = "Movie"
          break
      elif typed.lower() == "series":
          mInfo["Type"] = "Series"
          break

  # Removes the ComingSoon category it it is set to false
  if mInfo["ComingSoon"].lower() == "false":
      mInfo.pop("ComingSoon")
  # Removes the TotalSeasons category if the type is a movie
  if mInfo["Type"].lower() == "movie":
      mInfo.pop("TotalSeasons")

  while not mInfo["Year"][-4:].isnumeric():
      print("They year should contain 4 numbers, Ex. 2014")
      yearIn = input("What year did the movie come out: ")
      if len(yearIn) == 4 and yearIn == mInfo["Released"][-4:]:
          mInfo["Year"] = yearIn
      elif len(yearIn) == 4 and yearIn != mInfo["Released"][-4:]:
          mInfo["Released"] = mInfo["Released"][0:-4] + yearIn

  if mInfo["Year"] != mInfo["Released"][-4:]:
      print("Year and Released should be the same year.")
      yrel = input("Enter the correct release date, Ex. 5 Jan 2005: ")
      mInfo["Year"] = yrel[-4:]
      mInfo["Released"] = yrel.title()

  if mInfo["Runtime"][-3:].lower() != "min":
      mInfo["Runtime"] = mInfo["Runtime"] + " min"

  mInfo["Images"] = mInfo["Images"].split(",")

  if mInfo["Plot"][-1:] != ".":
      mInfo["Plot"] = mInfo["Plot"] + "."

  data.append(mInfo)

  createLog("mcreate", user, phone, mInfo["Title"])
  with open("movies.json", "w") as mFile:
      json.dump(data, mFile, indent=4)

  print(ans.SUCCESS + "Movie created successfully" + ans.ENDCOLOR)
  input("Press any key to continue")
  menu()

# Startmenu 
def menu():
  os.system("cls")
  print(
      f"{ans.WHITE_RED}{uni.STARC} Welcome to Robsku's text-based video rental! {uni.STARC}{ans.ENDCOLOR}"
  )
  print(
      f"{ans.YEL_BLUE}This program supports Ukraine:{ans.ENDCOLOR}"
  )
  print(
      f"{ans.RED_BLACK}1. Show available films \n2. Rent a film \n3. Return a film \n4. Show rented films \n5. Add/remove film \n6. create/remove users \n7. Quit{ans.ENDCOLOR}"
  )
  os.system("color")
  menuCh = 0
  while menuCh < 1 or menuCh > 8:
      menuCh = int(
          input(f"{ans.WHITE_PURP}Choose an option (enter the number): {ans.ENDCOLOR}")
      )
      if menuCh < 1 or menuCh > 8:
          print("The number should be between 1 and 7")
      # Show available films
      elif menuCh == 1:
          availableFilms()
          input("Press any key to continue . . .")
          menu()
      # Rent a film
      elif menuCh == 2:
          rentFunc()
      # Return a film
      elif menuCh == 3:
          returnFunc()
      # List rented movies
      elif menuCh == 4:
          listRented()
          input("Press any key to continue . . .")
          menu()
      # Add / Remove a film
      elif menuCh == 5:
          os.system("cls")
          print(ans.HEADER + "Add/Remove a Film" + ans.ENDCOLOR)
          name = input("Enter your name: ")
          phone = input("Enter your phone number (Ex. 1234567890): ")
          if not customerExists(name, phone):
              promptNewUser(name, phone)
              input("Press any key to continue . . .")
              menu()
          else:
              mh = ""
              while mh.lower() != "c" or mh.lower() != "d":
                  mh = input(
                      "Do you want to add or remove a film?\n C -Add a film\n D -Remove a film\n: "
                  )
                  if mh.lower() == "c":
                      # Add a film
                      addMovie(name, phone)
                  # Remove a film
                  elif mh.lower() == "d":
                      os.system("cls")
                      print(ans.HEADER + "Remove a film" + ans.ENDCOLOR)
                      data = movieData()
                      pos = 1
                      for movie in data:
                          print(f"{pos}. {movie['Title']} ({movie['Year']})")
                          pos += 1

                      choice = int(input("What movie? (enter the number): "))

                      delChoice = data[choice - 1]["Title"]
                      print(f"Removing: {delChoice} ({data[choice-1]['Year']})")

                      delMovie(delChoice, name, phone)
                      time.sleep(2)
                      print(ans.SUCCESS + "Film removed successfully" + ans.ENDCOLOR)
                      input("Press any key to continue . . .")
                      menu()

                  else:
                      print("Enter C or D")
      # Add / Remove users
      elif menuCh == 6:
          os.system("cls")
          print(ans.HEADER + "Add/Remove Users" + ans.ENDCOLOR)
          anv = input("C - Create User\nD - Remove User\n: ")
          if anv.lower() == "c":
              name = input("Enter your name: ")
              phone = input("Enter your phone number (Ex 1234567890): ")
              if customerExists(name, phone):
                  print("User already exists")
              else:
                  manageCustomers("add", name, phone)
                  input("Press any key to continue . . .")
                  menu()

          elif anv.lower() == "d":
              name = input("Enter your name: ")
              phone = input("Enter your phone number (Ex 1234567890): ")
              if not customerExists(name, phone):
                  print(ans.NOTE + "The user does not exist" + ans.ENDCOLOR)
                  input("Press any key to continue . . .")
                  menu()
              else:
                  sure = input("Are you sure? (y/n): ")
                  if sure.lower() == "y":
                      manageCustomers("del", name, phone)
                      input("Press any key to continue . . .")
                      menu()
                  else:
                      print("Cancelling . . .")
                      menu()
      # Quits the program
      elif menuCh == 7:
          os.system("cls")
          print(ans.HEADER + "Quit" + ans.ENDCOLOR)
          exitPrompt = input("Are you sure you want to quit? (y/n): ")
          if exitPrompt.lower() == "n":
              menu()
          else:
              print("Exiting . . .")
              time.sleep(1)
              sys.exit()
      # Opens the secret menu...
      elif menuCh == 8:
          secretMenu()

def secretMenu():
  os.system("cls")
  print(ans.HEADER + "Secret Menu" + ans.ENDCOLOR)
  while True:
      lg = input(
          "PL - Print out the log file\nCL - Clear the log file\nPU - Print out all users\nLR - Print out all rented movies\nLeave empty to go back\n: "
      )
      if lg == "":
          menu()
      elif lg.lower() == "pl":
          os.system("cls")
          print(ans.HEADER + "The Log File" + ans.ENDCOLOR)
          data = pd.read_csv("log.csv")
          if len(data) > 0:
              print(data)
          else:
              print(f"{ans.NOTE}The log file is empty{ans.ENDCOLOR}")
          input("Press any key to continue . . .")
          secretMenu()
      elif lg.lower() == "cl":
          os.system("cls")
          print(ans.HEADER + "Clear Log File" + ans.ENDCOLOR)
          print(
              f"{ans.RED_BLACK}Are you sure you want to clear the log file?\nThis action can NOT be undone!{ans.ENDCOLOR}"
          )
          chk = input("(y/n): ")
          if chk.lower() == "y":
              print("Clearing the log file . . .")
              clearLog()
          for i in range(30):
              print("-" * i, end="\r")
              time.sleep(0.2)
              print("\033[K")
              print(ans.SUCCESS + "The log file was cleared" + ans.ENDCOLOR)
              print("\033[K")
              input("Press any key to continue . . .")
              secretMenu()
          else:
              print("Cancelling . . .")
              time.sleep(1)
              secretMenu()
      elif lg.lower() == "pu":
          os.system("cls")
          print(ans.HEADER + "Users" + ans.ENDCOLOR)
          for customer in customerData():
              print(
                  f'Name: {customer["name"]}, Number: {customer["phone"].replace("-", "")}'
              )
          input("Press any key to continue . . .")
          secretMenu()
      elif lg.lower() == "lr":
          os.system("cls")
          print(ans.HEADER + "Rented Films" + ans.ENDCOLOR)
          pos = 1
          print("{:<15}{:>15}".format("Film", "Renter"))
          for customer in customerData():
              for movie in customer["rented_movies"]:
                  print(pos, "{:<15}{:>15}".format(movie, customer["name"]))
                  pos += 1

          input("Press any key to continue . . .")
          secretMenu()

if __name__ == "__main__":
  fixes()
  menu()
